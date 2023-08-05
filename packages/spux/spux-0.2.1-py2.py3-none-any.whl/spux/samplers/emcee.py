# # # # # # # # # # # # # # # # # # # # # # # # # #
# Markov chain Monter Carlo (affine-invariant ensemble) sampler class
# Foreman-Mackey, Hogg, Lang & Goodman
# "emcee: The MCMC Hammer"
# PASP, 2012.
#
# Jonas Sukys
# Eawag, Switzerland
# jonas.sukys@eawag.ch
# All rights reserved.
# # # # # # # # # # # # # # # # # # # # # # # # # #
from __future__ import absolute_import  # Fixes emcee modules names conflict

import numpy
import pandas
from copy import deepcopy as copy

from .sampler import Sampler
from ..utils.timing import Timing

class EMCEE (Sampler):

    def __init__(self, chains, a=2.0, attempts=100):

        self.chains = chains
        self.a = a
        self.attempts = attempts

    # init chain
    def init (self, initial=None, reinit=0):

        # additional routines for the first init
        if not reinit:

            # setup likelihoods for each chain
            self.likelihoods = [ copy (self.likelihood) for index in range (self.chains) ]

        # if initial parameters are not specified, draw them from the prior distribution

        if initial is None:
          self.parameters = pandas.DataFrame (index=range(0), columns=self.prior.labels)
          for index in range (self.chains):
            parameters = self.prior.draw (rng=self.rng)
            self.parameters = self.parameters.append (parameters, ignore_index=1, sort=True)

        # else, if only one set of parameters is specified, replicate it
        elif not isinstance (initial, pandas.DataFrame):
            self.parameters = pandas.DataFrame (initial, index=range(1))
            self.parameters = pandas.DataFrame (numpy.repeat (self.parameters.values, self.chains, axis=0), index=range(self.chains), columns=self.parameters.keys())

        # else, if all parameteres are specified, use them
        else:
            self.parameters = initial

        # store keys for later wrapping
        self.labels = self.parameters.keys()

        # store parameter dimensions - how many paramters to be inferred
        self.dimensions = len (self.labels)

        if self.verbosity >= 2:
            print("Initial samples:")
            print(self.parameters)

        # reset status
        self.initialized = 0

    # evaluate likelihoods and priors of the proposed parameters
    def evaluate (self, qs):

        # get indices to be evaluated
        indices = qs.index.values

        # evaluate priors
        ps = numpy.array ([ self.prior.logpdf (parameters) if self.prior else 0.0 for index, parameters in qs.iterrows () ])

        # skip likelihood evaluation for parameters with zero prior
        keep = numpy.where (ps != float ('-inf')) [0] #numpy.array(numpy.where (ps != float('-inf')))
        skip = numpy.where (ps == float ('-inf')) [0] #numpy.array(numpy.where (ps == float('-inf')))

        # evaluate the respective likelihoods (according to the specified indices)
        Ls = numpy.full (len(qs), float ('-inf'))
        likelihoods = [ self.likelihoods [ indices [index] ] for index in keep ]
        parameters = [ parameters for index, parameters in qs.iloc[keep].iterrows () ]
        results, timings = self.executor.map (likelihoods, parameters)

        # extract estimates and infos
        infos = [ None ] * len(qs)
        for i, result in enumerate (results):
            Ls [keep[i]], infos [keep[i]] = result
        # TODO: fix this or remove
        #Ls [proc], infos [proc] = zip (*results)

        # get executor timing
        timing = self.executor.report ()

        # compute Ls + ps
        Lps = Ls + ps

        # set skipped likelihoods to 'NaN's (after computing Lps)
        Ls [skip] = float ('nan')

        return Lps, ps, Ls, infos, timing, timings

    # returned packed results
    def results (self):
        
        if self.informative:
            infos = {
                'parameters' : self.parameters,
                'proposes' : self.proposes,
                'priors' : self.ps,
                'likelihoods' : self.Ls,
                'infos' : self.infos,
                'accepts' : self.accepts,
                'timing' : self.timing,
                'timings' : self.timings,
            }
        else:
            infos = None
        return self.parameters, infos

    # routine adapted from EMCEE
    def stretch (self, p0, p1, lnprob0):

        s = numpy.atleast_2d(p0.values)
        Ns = len(s)
        c = numpy.atleast_2d(p1.values)
        Nc = len(c)

        zz = ((self.a - 1.) * self.rng.rand(Ns) + 1) ** 2. / self.a
        rint = self.rng.randint(Nc, size=(Ns,))
        proposes = pandas.DataFrame (c[rint] - zz[:, numpy.newaxis] * (c[rint] - s), columns=self.labels, index=p0.index)
        Lps, ps, Ls, infos, timing, timings = self.evaluate (proposes)

        lnpdiff = (self.dimensions - 1.) * numpy.log(zz) + Lps - lnprob0
        accepts = (lnpdiff > numpy.log(self.rng.rand(len(lnpdiff))))

        return proposes, Lps, ps, Ls, infos, accepts, timing, timings

    # routine adapted from EMCEE
    # TODO: report an error or at least issue a warning if self.chains < 2 * self.executor.workers
    # TODO: think if it is not possible to call self.executor.map() only once - this would help with the balancing
    def propose (self):

        self.timing = Timing ()
        self.timings = [Timing () for worker in range (self.executor.workers)]
        self.proposes = pandas.DataFrame (index=range(self.chains), columns=self.labels)
        self.ps = numpy.zeros (self.chains)
        self.Ls = numpy.zeros (self.chains)
        self.infos = [None for chain in range(self.chains)]
        self.accepts = numpy.zeros (self.chains)
        half = self.chains // 2
        first, second = numpy.arange (0, half), numpy.arange (half, self.chains)
        for S0, S1 in [(first, second), (second, first)]:
            proposes, Lps, ps, Ls, infos, accepts, timing, timings = self.stretch (self.parameters.iloc [S0], self.parameters.iloc [S1], self.Lps [S0])
            self.proposes.iloc[S0] = proposes
            self.ps[S0] = ps
            self.Ls[S0] = Ls
            for index, info in enumerate (infos):
                self.infos [S0[index]] = info
            self.accepts[S0] = accepts
            self.Lps[S0[accepts]] = Lps [accepts]
            self.parameters.values[S0[accepts]] = proposes.values [accepts]
            self.timing += timing
            for worker, timing in enumerate (self.timings):
                timing += timings [worker]

    # draw samples from posterior distribution
    def draw (self, sandbox, seed):

        # setup likelihoods
        for index, likelihood in enumerate (self.likelihoods):
            label = 'C%05d' % index
            chain_sandbox = sandbox.spawn (label)
            chain_seed = seed.spawn (index, name=label)
            likelihood.setup (chain_sandbox, self.verbosity - 2, seed=chain_seed, informative=self.informative)

        # treat 'initial' parameters as the first sample
        if not self.initialized:

            if self.verbosity >= 3:
                print ('EMCEE: draw (initialize)')

            # attempt to evaluate likelihood of the initial parameters, with a redraw if needed
            for attempt in range (self.attempts):

                # all initial samples are proposed
                self.proposes = self.parameters

                # evaluate likelihood and prior of the initial parameters
                self.Lps, self.ps, self.Ls, self.infos, self.timing, self.timings = self.evaluate (self.proposes)

                # check if at least one likelihood is valid
                if not all (self.Lps == float ("-inf")):
                    break

                # otherwise, attempt to redraw prior samples
                else:

                    # if this is the final attempt, crash
                    if attempt == self.attempts - 1:
                        print (" :: Fatal: Unable to find initial parameters with non-zero likelihoods.")
                        print ("  : -> You may try to change seed and/or give explicit initial parameters.")
                        self.executor.abort ()

                    # otherwise, attempt to redraw prior samples
                    print (" :: Warning: The likelihoods of all initial parameters are zero.")
                    print ("  : -> Re-drawing initial parameters from prior (attempt: %d/%d)" % (attempt, self.attempts))
                    self.init (initial=None, reinit=1)

            # all initial samples are accepted
            self.accepts = numpy.ones ((self.chains,))

            # all initial parameters are accepted
            self.parameters = self.proposes

            # update status
            self.initialized = 1

            return self.results ()

        if self.verbosity >= 3:
            print ('EMCEE: draw (sample)')

        # get new parameters
        self.propose ()

        return self.results ()
