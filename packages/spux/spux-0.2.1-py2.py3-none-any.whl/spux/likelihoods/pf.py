# # # # # # # # # # # # # # # # # # # # # # # # # #
# Particle Filtering likelihood class
# Particle filtering based on
# Kattwinkel & Reichert, EMS 2017.
# Implementation described in
# Sukys & Kattwinkel, Proceedings of ParCo 2017,
# Advanced Parallel Computing, IOS Press, 2018.
#
# Jonas Sukys
# Eawag, Switzerland
# jonas.sukys@eawag.ch
# All rights reserved.
# # # # # # # # # # # # # # # # # # # # # # # # # #

import numpy

from ..utils.timing import Timing
from ..utils.transforms import numpyfy
from .likelihood import Likelihood
from .pf_ensemble import Ensemble

class PF (Likelihood):

    # constructor
    def __init__ (self, particles=100, log=1):

        self.particles = particles
        self.log = log

    # redraw particles based on errors
    def redraw (self, indices, errors):

        # compute probabilities for discrete distribution
        if numpy.sum (errors) != 0:
            probabilities = errors / numpy.sum (errors)
        else:
            if self.verbosity:
                print(" :: WARNING: All particle errors are zero")
            probabilities = 1.0 / len(indices) * numpy.ones(len(indices))

        # sample from discrete distribution
        choice = self.rng.choice (indices, size=self.particles, p=probabilities)

        # compute redraw rate
        redraw = len(set(choice)) / float(len(indices))

        return choice, redraw

    # evaluate/approximate likelihood of the specified parameters
    def __call__ (self, parameters):

        # verbose output
        if self.verbosity >= 2:
            print ("PF parameters:")
            print (parameters)

        # start global timer
        timing = Timing ()
        timing.start ('evaluate')

        # construct ensemble task
        ensemble = Ensemble (self.model, self.input, parameters, self.error, log=0)

        # setup ensemble
        ensemble.setup (self.sandbox, self.verbosity - 2, seed=self.seed, informative=self.informative)

        # initialize task indices from the specified number of tasks
        indices = [index for index in range (self.particles)]
        if self.verbosity >= 2:
            print("Initial indices:", indices)

        # initialize task ensemble in executor
        self.executor.connect (ensemble, indices)
        
        # initialize predictions container
        predictions = { 'prior' : {}, 'posterior' : {} }

        # initialize errors containter
        errors = {}

        # initialize estimates container
        estimates = {}

        # initialize quality control container
        variances = {}

        # initialize container for resampled indices
        # TODO: this should contain routing information to track partile trajectories for MAP
        resamples = {}

        # initialize traffic measurements container
        traffic = {}

        # initialize particle redraw rate measurements container
        redraw = {}

        # iterate over all data snapshots (times)
        for snapshot in self.data.index:

            if self.verbosity:
                print("Snapshot", snapshot)
            
            # run particles (models)
            if self.verbosity >= 2:
                print("Running particles (%s models)..." % self.task.name)
            predictions ['prior'] [snapshot] = self.executor.call ('run', args = [snapshot], flatten=1)

            # compute errors
            if self.verbosity >= 2:
                print("Computing errors...")
            errors [snapshot] = numpyfy (self.executor.call ('errors', args = [self.data.loc [snapshot]], flatten=1))
            
            # reset indices
            indices = numpy.arange (self.particles)
            
            if self.verbosity >= 2:
                print("Errors", errors)

            # compute (log-)error estimates for the current snapshot
            mean = numpy.mean (errors [snapshot])
            if self.log:
                if numpy.isnan (mean):
                    logmean = float ('nan')
                else:
                    if mean == 0:
                        logmean = float ('-inf')
                    else:
                        logmean = numpy.log (mean)
            estimates [snapshot] = logmean if self.log else mean
            if self.verbosity:
                print ("Estimated %slikelihood at snapshot %s: %1.1e" % ('log-' if self.log else '', str (snapshot), estimates [snapshot]))
            
            # if estimator failed - no further filtering is possible
            if numpy.isnan (estimates [snapshot]):
                if self.verbosity:
                    print (" :: WARNING: NaN estimate in the PF likelihood.")
                    print ("  : -> stopping here and returning the infos as they are.")
                break

            # estimate variance of the (log-)likelihood estimates for the current snapshot,
            # using 1st order Taylor approximation for the log-likelihood case:
            # https://stats.stackexchange.com/questions/57715/expected-value-and-variance-of-loga#57766
            if errors [snapshot] .size > 1 and mean != 0:
                variance = numpy.var (errors [snapshot], ddof=1) / errors [snapshot] .size
                if numpy.isnan (variance):
                    variances [snapshot] = float ("nan")
                else:
                    if variance != 0:
                        variances [snapshot] = variance / (mean ** 2)
                    else:
                        variances [snapshot] = 0
                if self.verbosity:
                    print ("Estimated log-likelihood variance at snapshot %s: %1.1e" % (str (snapshot), variances [snapshot]))
            else:
                variances [snapshot] = float ("nan")
            
            # redraw particles based on errors
            indices, redraw [snapshot] = self.redraw (indices, errors [snapshot])
            if self.verbosity >= 2:
                # indices contain the list of future particles, their ids
                print("Redrawn indices", indices)
            
            # store resamples indices
            resamples [snapshot] = indices
            
            # redraw predictions as well
            predictions ['posterior'] [snapshot] = [ predictions ['prior'] [snapshot] [index] for index in indices ]

            # advance ensemble state to next iteration (do not gather results)
            self.executor.call ('advance', results=0)

            # resample (delete and replicate) particles and balance ensembles in the executor and record resulting traffic
            traffic [snapshot] = self.executor.resample (indices)

        # finalize task ensemble in executor
        timings = self.executor.disconnect ()

        # append executor timing
        timing += self.executor.report ()

        # compute estimated (log-)likelihood as the product of estimates from all snapshots
        if self.log:
            estimate = numpy.sum (list (estimates.values()))
        else:
            estimate = numpy.prod (list (estimates.values()))
        
        # compute estimated variance of the estimated log-likelihood
        variance = numpy.sum (list (variances.values()))

        if self.verbosity:
            print ("Estimated %slikelihood: %1.1e" % ('log-' if self.log else '', estimate))
            print ("Estimated variance of log-likelihood: %1.1e" % variance)

        # measure evaluation runtime and timestamp
        timing.time ('evaluate')

        # information includes redraw rate, estimated likelihood quality, used up
        # communication traffic, and timing
        if self.informative:
            infos = {
                "predictions": predictions,
                "errors" : errors,
                "estimates": estimates,
                "variance": variance,
                "variances": variances,
                "resamples": resamples,
                "redraw": redraw,
                "traffic": traffic,
                "timing": timing,
                'timings': timings,
            }
        else:
            infos = None

        # return estimated likelihood and its info
        return estimate, infos
