# # # # # # # # # # # # # # # # # # # # # # # # # #
# Replicates class for multiple independent data sets
#
# Jonas Sukys
# Eawag, Switzerland
# jonas.sukys@eawag.ch
# All rights reserved.
# # # # # # # # # # # # # # # # # # # # # # # # # #

import numpy
from copy import deepcopy as copy

from .likelihood import Likelihood
from ..executors.serial import Serial

class Replicates (Likelihood):

    # constructor
    def __init__(self, log=1, sort=1):

        self.log = log
        self.sort = sort

        # initially likelihoods are not created
        self.likelihoods = None
    
    # assign required components to likelihood
    def assign (self, likelihood, datasets, inputsets=None):

        self.likelihood = likelihood
        self.datasets = datasets
        self.inputsets = inputsets

        self.task = self.likelihood
        self.sandboxing = self.likelihood.sandboxing

        if not hasattr (self, 'executor'):
            self.attach (Serial ())
    
    # attach an executor
    def attach (self, executor):

        self.executor = executor
        self.executor.setup (self)
        self.executor.capabilities (['map', 'report'])

    # evaluate likelihoods of the specified parameters for all replicates and combine them
    def __call__ (self, parameters):

        # verbose output
        if self.verbosity:
            print ("Replicates parameters:")
            print (parameters)

        # create likelihoods by combining with each data in the dataset
        if self.likelihoods is None:
            self.likelihoods = {}
            for name, data in self.datasets.items ():
                self.likelihoods [name] = copy (self.likelihood)
                self.likelihoods [name] .data = data
                if self.inputsets is not None:
                    self.likelihoods [name] .input = self.inputsets [name]
        
        # setup likelihoods
        for index, (name, likelihood) in enumerate (self.likelihoods.items ()):
            label = 'R-%s' % name
            sandbox = self.sandbox.spawn (label)
            seed = self.seed.spawn (index, name=label)
            likelihood.setup (sandbox, self.verbosity - 1, seed=seed, informative=self.informative)
        
        # sort likelihoods according to the lenght of the associated dataset
        if self.sort:
            lengths = [ len (likelihood.data) for likelihood in self.likelihoods.values () ]
            ordering = numpy.argsort (lengths) [::-1]
            keys = numpy.array ([ key for key in self.likelihoods.keys () ]) [ordering]
            likelihoods = [ self.likelihoods [key] for key in keys ]
            if self.verbosity:
                print ("Using ordered likelihoods:")
                print (" -> order: ", keys)
        else:
            keys = self.likelihoods.keys ()
            likelihoods = self.likelihoods.values ()

        # schedule likelihood evaluations
        results, timings = self.executor.map (likelihoods, None, parameters)

        # append executor timing
        timing = self.executor.report()

        # get results
        evaluations = {}
        infos = {}
        for index, name in enumerate (keys):
            evaluations [name], infos [name] = results [index]

        # compute estimated (log-)likelihood as the product of estimates from all replicates
        evaluations_array = numpy.array (list(evaluations.values()))
        nans = numpy.isnan (evaluations_array)
        if any (nans):
            mean = numpy.nanmean (evaluations_array)
            if self.verbosity:
                print (" :: WARNING: NaN estimates in the Replicates likelihood:")
                print (evaluations)
                print ("  : -> setting NaN estimates to the mean %1.1e of the non-NaN estimates." % mean)
            evaluations_array = numpy.where (nans, mean, evaluations_array)
        if self.log:
            if not self.likelihood.log:
                evaluations_array = numpy.log (evaluations_array)
            evaluation = numpy.sum (evaluations_array)
        else:
            if self.likelihood.log:
                evaluations_array = numpy.exp (evaluations_array)
            evaluation = numpy.prod (evaluations_array)

        # information
        if self.informative:
            infos = {
                "evaluations": evaluations,
                "infos": infos,
                'timing': timing,
                'timings': timings,
            }
        else:
            infos = None

        # return estimated likelihood, its info
        return evaluation, infos
