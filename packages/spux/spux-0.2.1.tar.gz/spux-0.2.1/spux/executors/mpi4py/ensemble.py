# # # # # # # # # # # # # # # # # # # # # # # # # #
# Executor class using mpi4py bindings and MPI backend for distributed memory paralellization
#
# Jonas Sukys
# Eawag, Switzerland
# jonas.sukys@eawag.ch

# All rights reserved.
# # # # # # # # # # # # # # # # # # # # # # # # # #

from mpi4py import MPI
import cloudpickle
MPI.pickle.__init__ (cloudpickle.dumps, cloudpickle.loads)

from copy import deepcopy as copy
import sys

from ..executor import Executor
from .ensemble_contract import INIT, CALL, RESA, DONE, EXIT, Instruction, contract

from ..balancers.adaptive import Adaptive
from .connectors.spawn import Spawn

from ...utils.timing import Timing

class Mpi4pyEnsemble (Executor):

    manager = 1

    @staticmethod
    def address (peers):

        return peers.Get_rank ()
    
    @staticmethod
    def universe_address ():

        address = MPI.COMM_WORLD.Get_rank ()
        return address

    def __init__ (self, workers=None, balancer=Adaptive(), connector=Spawn()):

        self.workers = workers
        self.balancer = balancer
        self.connector = connector.connect

        self.balancer.verbosity = self.verbosity - 1 if self.verbosity > 0 else 0

    def info (self):

        thread = MPI.Query_thread()
        if thread == MPI.THREAD_MULTIPLE:
            return 'multiple threads support'
        elif thread == MPI.THREAD_SERIALIZED:
            return 'multiple threads support (serialized)'
        else:
            return 'NO support for multiple threads'

    def bootup (self):

        # get an inter-communicator to worker pool
        workers = self.connector (contract, self.resources () [0], self.root, self.verbosity)

        # open a port for workers to connect to
        port = MPI.Open_port ()

        # broadcast port and task template to workers
        workers.bcast ((port, self.task), root=MPI.ROOT)

        # disconnect from workers
        workers.Disconnect ()
        workers = None

        return port

    def shutdown (self):

        workers = MPI.COMM_SELF.Accept (self.port)
        instruction = Instruction (EXIT)
        workers.Bcast (instruction.list, root=MPI.ROOT)
        workers.Disconnect ()
        workers = None
        MPI.Close_port (self.port)

    # set task ensemble for execution
    def connect (self, ensemble, indices):

        self.workers_comm = MPI.COMM_SELF.Accept (self.port)

        self.timing = Timing ()

        instruction = Instruction (INIT)
        self.workers_comm.Bcast (instruction.list, root=MPI.ROOT)

        # prepare and broadcast ensemble
        self.prepare (ensemble)
        self.workers_comm.bcast (ensemble, root=MPI.ROOT)

        # set balancer verbosity
        self.balancer.verbosity = self.verbosity - 1 if self.verbosity > 0 else 0

        # distribute task indices to workers
        self.ensembles = self.balancer.ensembles (indices, self.workers)
        if self.verbosity >= 2:
            print("connect ensembles (before scatter):", self.ensembles)

        # scatter task ensembles to workers (must make a copy, because after scatter ensemble is invalid!)
        if self.verbosity >= 2:
            print ("connect ensembles (before scatter):", self.ensembles)
            sys.stdout.flush()
        self.workers_comm.scatter (copy (self.ensembles), root=MPI.ROOT)
        if self.verbosity >= 2:
            print ("connect ensembles (after scatter):", self.ensembles)
            sys.stdout.flush()

        # time init sync overhead
        self.timing.start ('wait')
        self.workers_comm.Barrier ()
        self.timing.time ('wait')

    # disconnect task ensemble
    def disconnect (self):

        instruction = Instruction (DONE)
        self.workers_comm.Bcast (instruction.list, root=MPI.ROOT)

        # gather worker timings
        timings = self.workers_comm.gather (None, root=MPI.ROOT)

        self.workers_comm.Disconnect ()
        self.workers_comm = None

        if self.verbosity >= 2:
            print("Ensemble executor disconnect")

        return timings

    # report performance
    def report (self):

        return self.timing

    # execute ensemble method with specified args and return results (if wait=1)
    def call (self, method, args=[], flatten=0, results=1):
        
        instruction = Instruction (CALL)
        self.workers_comm.Bcast (instruction.list, root=MPI.ROOT)
        self.workers_comm.bcast ({'method' : method, 'args' : args, 'results' : results}, root=MPI.ROOT)

        # if there are no results to wait for, return
        if not results:
            return
        
        # else, wait for the results and process them
        self.timing.start ('wait')
        results = self.workers_comm.gather (None, root=MPI.ROOT)
        self.timing.time ('wait')
        if flatten and all (results):
            results = { key : value for result in results for key, value in result.items() }

        if any(result is None for result in results):
            if not all(result is None for result in results):
                print("Fatal. Got some None results but not all of them in call of ensemble.py. This is a bug.")
                sys.stdout.flush()
                self.workers_comm.Abort()

        return results

    # resample (delete and replicate) tasks and balance ensembles
    def resample (self, indices):

        # compute new task ensembles and their routings from current task
        # ensembles
        if self.verbosity >= 2:
            print("Resample: current ensembles:", self.ensembles)
        self.ensembles, routings = self.balancer.routings (self.ensembles, indices)
        if self.verbosity >= 2:
            print("Resample: future ensembles:", self.ensembles)
        if self.verbosity >= 2:
            print("Resample: routings", routings)

        # measure traffic
        traffic = self.balancer.traffic (routings, len(indices))

        # send instruction to start the task resampling and ensemble balancing process
        instruction = Instruction (RESA)
        self.workers_comm.Bcast (instruction.list, root=MPI.ROOT)

        # scatter routings
        self.timing.start ('routings')
        self.workers_comm.scatter (routings, root=MPI.ROOT)
        self.timing.time ('routings')

        # gather timings
        self.timing.start ('wait')
        self.workers_comm.Barrier ()
        self.timing.time ('wait')

        return traffic
    
    # abort
    def abort (self):
        
        MPI.Abort ()