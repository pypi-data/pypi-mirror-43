# # # # # # # # # # # # # # # # # # # # # # # # # #
# Connector class for spawning workers directly from the manager at the OS level
# using mpi4py bindings and MPI backend for distributed memory paralellization
#
# Jonas Sukys
# Eawag, Switzerland
# jonas.sukys@eawag.ch
# All rights reserved.
# # # # # # # # # # # # # # # # # # # # # # # # # #

from mpi4py import MPI
import os
import sys

class Spawn (object):

    # connect manager with the number of requested workers by returning the inter-communicator
    @staticmethod
    def connect (contract, resource, root=0, verbosity=0):
        
        directory, filename = os.path.split (os.path.realpath (__file__))
        worker = os.path.join (directory, "worker.py")
        info = MPI.Info.Create ()
        info.Set ('wdir', os.getcwd ())
        if verbosity:
           print ("Spawning workers:", resource ['workers'])
        workers = MPI.COMM_SELF.Spawn (sys.executable, args=[worker], maxprocs=resource ['workers'], info=info)
        workers.bcast (contract, root=MPI.ROOT)
        return workers

    def barrier (self):

        return None
    
    def init (self, resources):

        return None
