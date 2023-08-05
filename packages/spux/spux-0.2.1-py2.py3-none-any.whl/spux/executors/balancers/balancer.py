# # # # # # # # # # # # # # # # # # # # # # # # # #
# Balancer base class
#
# Jonas Sukys
# Eawag, Switzerland
# jonas.sukys@eawag.ch
# All rights reserved.
# # # # # # # # # # # # # # # # # # # # # # # # # #

import sys
import math
import numpy

class Balancer (object):

    verbosity = 0

    # compute traffic from routings
    def traffic(self, routings, count):

        moves = [{} for address, routing in enumerate(routings)]
        costs = [{} for address, routing in enumerate(routings)]
        copys = [{} for address, routing in enumerate(routings)]

        inits = [0 for address, routing in enumerate(routings)]
        kills = [0 for address, routing in enumerate(routings)]

        # address is the id of the ensemble "routing", i.e, of a potential # worker deputed to process that ensemble in next round
        for address, routing in enumerate(routings):

            # index is particle id of those particles that have survived
            # counter = reindex: new id of particle "index" in next ensemble
            for index, source, destination, counter in routing:
                #print(address,index)
                moves[address][index] = 0
                costs[address][index] = 0
                copys[address][index] = 0

        for address, routing in enumerate(routings):
            for index, source, destination, counter in routing:
                # when does this (no source for particle?) evaluate True?
                if source is None:
                    sys.exit("--- Wasn't 'source is None' impossible? ---")
                    inits[address] += 1
                    continue
                # I think that this and the above will never happen due to
                # the way routings is constructed
                if destination is None:
                    sys.exit("--- Wasn't 'dest is None' impossible? ---")
                    kills[address] += 1
                    continue
                # current and future ensemble for this particle are =
                if destination == address:
                    # this skips routings[address] constructed in the 2nd
                    # part of RoundRobin.routings routings[source] += ...
                    # I think, cause there destination != address = source

                    if source == address:
                        # self thing - this info was alredy there from
                        # first part of RoundRobin.routings, I'd say
                        copys[address][index] += 1
                        continue

                    # I think it enters here only for the routings[address]
                    # that are the ones built in destination != source: of
                    # RoundRobin.routings
                    if source != address:
                        # ensemble "address" will have to get particle from
                        # ensemble "source": this info was already there in
                        # the second part of RoundRobin.routings when
                        # destination != source I'd say

                        # if particle has not been moved yet, move it
                        # do we risk overloading of ensembles with too many
                        # particles, i.e., an ensemble with more particles
                        # than limit? - prolly not, if this is a move to.
                        if moves[address][index] == 0:
                            moves[address][index] += 1
                            costs[address][index] += math.fabs(source - destination)
                            continue

                        # particles are moved only once, then copied
                        # locally. This is not an elif - it executes
                        # even when the above executes
                        if moves[address][index] == 1:
                            copys[address][index] += 1
                            continue

        # first copy is not performed - ok due to lack of elif I'd say
        for address, copy in enumerate(copys):
            for index in copy:
                if copy[index] > 0:
                    copy[index] -= 1

        moves_total = numpy.sum(
            [
                numpy.sum(list(moves[address].values()))
                for address, routing in enumerate(routings)
            ]
        )
        costs_total = numpy.sum(
            [
                numpy.sum(list(costs[address].values()))
                for address, routing in enumerate(routings)
            ]
        )
        copys_total = numpy.sum(
            [
                numpy.sum(list(copys[address].values()))
                for address, routing in enumerate(routings)
            ]
        )

        return {
            "init": numpy.sum(inits) / float(count),
            "move": moves_total / float(count),
            "cost": costs_total / float(count),
            "copy": copys_total / float(count),
            "kill": numpy.sum(kills) / float(count),
        }
