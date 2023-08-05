# # # # # # # # # # # # # # # # # # # # # # # # # #
# Connector class for subdivision of MPI.COMM_WORLD into manager and workers
# using mpi4py bindings and MPI backend for distributed memory paralellization
# Legacy version of the 'Split' connector, avoiding the use of Accept/Connect
#
# Marco Bacci
# Eawag, Switzerland
# marco.bacci@eawag.ch
# All rights reserved.
# # # # # # # # # # # # # # # # # # # # # # # # # #

from mpi4py import MPI

def universe_address ():

    address = MPI.COMM_WORLD.Get_rank ()
    return address

# def Create_intercomm(self,
#                          int local_leader,
#                          Intracomm peer_comm,
#                          int remote_leader,
#                          int tag=0):