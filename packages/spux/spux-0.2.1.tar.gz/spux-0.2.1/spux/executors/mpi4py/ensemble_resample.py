# # # # # # # # # # # # # # # # # # # # # # # # # #
# Resample routine for the contract of the Mpi4pyEnsemble executor class
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

from ...utils.timing import Timing

def universe_address ():

    address = MPI.COMM_WORLD.Get_rank ()
    return address

# resample (detele and replicate) particles and balance ensembles according to the specified 'routing'
# REMARK: only particles provided in 'routing' are kept - non-routed particles are removed
def resample (ensemble, routing, peers):

    particles = ensemble.particles
    task = ensemble.task
    prepare = ensemble.prepare
    address = ensemble.root [-1] ['address']
    serialization = task.serialization

    # Communication/computation overlap at the expense of memory usage:
    # 0. check if routing makes sense
    # 1. launch all isend/irecv for particle exchange according to routing
    # (TODO: add clean up, document a-priori particle size communications)
    # 2. replicate local particles into resampled ensemble
    # 3. store and replicate received remote particles into resampled ensemble
    # 4. wait for all local particles to be sent

    # counter of particles (for each index - index is here id particle)
    keep_counters = {}  # with this ensemble as both source and destination
    send_counters = {}  # with this ensemble as source
    recv_counters = {}  # with this ensemble as destination

    # commnunication requests
    send_requests = {}
    recv_requests = {}

    # available task states for required indices
    states = {}

    # initialize send/recv counters and send/recv requests
    for index, source, destination, reindex in routing:
        keep_counters [index] = []  # format: keep_counters [index]
        send_counters [index] = {}  # format: send_counters [index] [destination]
        recv_counters [index] = []  # format: recv_counters [index]
        send_requests [index] = {}  # format: send_requests [index] [destination]
        recv_requests [index] = {}  # format: recv_requests [index] [source]

    # timer for replicate (save/copy/load) routines
    timing = Timing ()
 
    # 0. check if routing makes sense
    for index, source, destination, reindex in routing:
        if source == address and index not in particles:
            values = (str((index, source, destination, reindex)), particles.keys (), ensemble.root)
            print (' :: ERROR: invalid routing %s in resample() with indices %s and root %s' % values)
            peers.Abort ()

    # 1. launch all isend/irecv for particle exchange according to routing
    for index, source, destination, reindex in routing:

        # if particle exists locally
        if source == address:

            # keep particles with local ensemble as destination
            if destination == address:
                keep_counters[index] += [reindex]
                continue

            # send out particles with remote ensemble as destination
            if destination != address:

                # only once per each index and destination
                if destination not in send_counters[index]:

                    # save particle state
                    send_counters[index][destination] = 1
                    if index not in states:
                        timing.start ('replicate')
                        states[index] = particles[index].save ()
                        timing.time ('replicate')

                    # use pickle to directly send state
                    if serialization == 'pickle':
                        send_requests[index][destination] = peers.isend (states [index], dest=destination, tag=index)

                    # for states as binary arrays, send the particle size first
                    elif serialization == 'binary':
                        size = len(states[index])
                        send_requests[index][destination] = peers.isend(
                            size, dest=destination, tag=index
                        )

                    # report unsupported serialization types
                    else:
                        print("Ensemble %d: invalid serialization:" % address)

                else:
                    
                    send_counters[index][destination] += 1

                continue

        # if particle already exists, but in a remote ensemble, request it
        if source != address and destination == address:

            # only once per each index - i.e. receive only once a
            # specific particle (or its size)
            if recv_counters[index] == []:
                recv_requests[index][source] = peers.irecv (source=source, tag=index)
            recv_counters[index] += [reindex]
            continue

        # report a problem in routing - why not fatal?
        print("Fatal. Ensemble %d: invalid particle routing:" % address)
        print( "index %d, source %s, destination %s." % (index, str(source), str(destination)) )
        print("This is a bug.")
        peers.Abort()

    # for states as binary arrays, process particle sizes and initialize actual sends and recvs
    if serialization == "binary":

        # store received remote particle sizes and initiate asynchronous particle recvs
        for index, requests in recv_requests.items():
            for source, request in requests.items():
                size = request.wait()
                states [index] = task.state (size)
                recv_requests [index][source] = peers.Irecv(
                    [states [index], size, MPI.BYTE], source=source, tag=index
                )

        # initiate asynchronous particle sends to all destinations
        # TODO: use MPI.Request.waitany () to improve this
        for index, requests in send_requests.items():
            for destination, request in requests.items():
                request.wait()
                size = len(states[index])
                send_requests [index][destination] = peers.Isend ([states [index], size, MPI.BYTE], dest=destination, tag=index)

    # new ensemble of resampled particles
    resampled = {}

    # 2. replicate local particles according to 'keep_counters'
    timing.start ('replicate')
    for index, reindices in keep_counters.items():
        if len(reindices) > 0:
            reindex = reindices [0]
            resampled [reindex] = particles [index]
            prepare (reindex, resampled [reindex])
        if len(reindices) > 1:
            if index not in states:
                states[index] = particles[index].save ()
            for reindex in reindices[1:]:
                resampled [reindex] = copy (task)
                prepare (reindex, resampled [reindex])
                resampled [reindex] .load (states [index])
                prepare (reindex, resampled [reindex])
    timing.time ('replicate')

    # 3. store received remote particles and replicate according to 'recv_counters'
    # TODO: use MPI.Request.waitany () to improve this
    for index, requests in recv_requests.items():
        for source, request in requests.items():
            if serialization == "pickle":
                states[index] = request.wait ()
            else:
                request.Wait ()
            timing.start ('replicate')
            reindex = recv_counters [index][0]
            resampled [reindex] = copy (task)
            prepare (reindex, resampled [reindex])
            resampled [reindex] .load (states[index])
            prepare (reindex, resampled [reindex])
            if len(recv_counters[index]) > 1:
                for reindex in recv_counters[index][1:]:
                    resampled [reindex] = copy (task)
                    prepare (reindex, resampled [reindex])
                    resampled [reindex] .load (states[index])
                    prepare (reindex, resampled [reindex])
            timing.time ('replicate')

    # 4. wait for all particles to be sent
    # TODO: use MPI.Request.waitall () to avoid too many loops
    for index, requests in send_requests.items():
        for request in requests.values():
            if serialization == "pickle":
                request.wait()
            else:
                request.Wait()
    
    # finalize all extinct particles
    extinct = set (ensemble.particles.keys ()) - set (keep_counters.keys ())
    for index in extinct:
        ensemble.particles [index] .exit ()
    
    # replace particles
    ensemble.particles = resampled

    # return timing
    return timing
