# # # # # # # # # # # # # # # # # # # # # # # # # #
# Mpi4pyWrapper executor class using mpi4py bindings and MPI backend for distributed memory paralellization
#
# Marco Bacci
# Eawag, Switzerland
# jonas.sukys@eawag.ch
# All rights reserved.
# # # # # # # # # # # # # # # # # # # # # # # # # #

# TODO: WORK IN PROGRESS

from mpi4py import MPI
import cloudpickle
MPI.pickle.__init__ (cloudpickle.dumps, cloudpickle.loads)

from ..executor import Executor

from .connectors.spawn import Spawn

#from ...utils.timing import Timing

class Mpi4pyWrapper (Executor):

    manager = 1

    @staticmethod
    def address (peers):

        return peers.Get_rank ()
    
    @staticmethod
    def universe_address ():

        address = MPI.COMM_WORLD.Get_rank ()
        return address

    def __init__ (self, workers, connector=Spawn()):

        self.workers = workers
        self.connector = connector.connect

    def info (self):

        thread = MPI.Query_thread()
        if thread == MPI.THREAD_MULTIPLE:
            return 'multiple threads support'
        elif thread == MPI.THREAD_SERIALIZED:
            return 'multiple threads support (serialized)'
        else:
            return 'NO support for multiple threads'
    
    # abort
    def abort (self):
        
        MPI.Abort ()