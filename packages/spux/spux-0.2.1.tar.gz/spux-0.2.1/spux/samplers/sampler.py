# # # # # # # # # # # # # # # # # # # # # # # # # #
# Base sampler class
#
# Jonas Sukys
# Eawag, Switzerland
# jonas.sukys@eawag.ch
# All rights reserved.
# # # # # # # # # # # # # # # # # # # # # # # # # #

import pandas
import os
import cProfile

from ..utils.timer import Timer
from ..utils.sandbox import Sandbox
from ..utils.setup import setup
from ..utils.seed import Seed
from ..executors.serial import Serial
from ..utils.progress import Progress
from ..io.checkpointer import Checkpointer
from ..io import dumper

class Sampler(object):

    @property
    def name (self):

        return type(self).__name__
    
    # assign required components to sampler
    def assign (self, likelihood, prior=None):

        self.likelihood = likelihood
        self.prior = prior

        self.sandboxing = self.likelihood.sandboxing
        self.task = self.likelihood

        if not hasattr (self, 'executor'):
            self.attach (Serial ())
    
    # attach an executor
    def attach (self, executor):

        self.executor = executor
        self.executor.setup (self)
        self.executor.capabilities (['map', 'report'])

    # setup sampler
    def setup (self, sandbox=Sandbox(), verbosity=1, seed=Seed(), index=0, trace=0, outputdir='output', informative=1):

        # standardized setup
        setup (self, sandbox, verbosity, seed, informative)

        # setup and report index
        self.index = index
        if self.verbosity and index > 0:
            print ("Sampler index:", index)

        # setup trace
        self.trace = trace

        # setup outputdir
        self.outputdir = outputdir
        fresh = (self.index == 0)
        dumper.mkdir (self.outputdir, fresh)

        # set infos logging flag
        self.informative = informative

    # online sampling (Python generator) with progress tracking and periodic saving
    # iteratively yielding results for each sample (or ensemble of samples)
    def generator (self, size=1):

        # initialize progress bar
        if self.verbosity == 1:
            progress = Progress (prefix="Sampling: ", steps=size, length=40)
            progress.init ()
        elif self.verbosity >= 2:
            print ("Drawing %d samples..." % size)

        # initialize sample count
        count = 0

        # sample iteratively
        while count < size:

            # set label for current index
            label = "S%05d" % self.index

            # spawn a sandbox for current index
            sandbox = self.sandbox.spawn (label)

            # spawn a seed for current index
            seed = self.seed.spawn (self.index, name=label)

            # draw a random sample from posterior
            parameters, infos = self.draw (sandbox, seed)

            # increment count
            count += len (parameters)

            # update progress
            if self.verbosity == 1:
                progress.update (count)
            elif self.verbosity >= 2:
                print("Sample(s) %d/%d" % (count, size))

            # cleanup sample-specific sandbox
            if not self.trace:
                sandbox.clean ()

            # yield results as a generator for additional external processing
            yield parameters, infos

            # increment index
            self.index += 1

        if self.verbosity == 1:
            progress.finalize ()

    # save samples and infos and free the memory
    def flush (self, samples, infos, timestamp):

        # format suffix
        suffix = '%05d-%s' % (self.index, timestamp)

        # CSV export of samples
        samples.to_csv (os.path.join (self.outputdir, 'samples-%s.csv' % suffix))

        # binary export of samples
        dumper.dump (samples, name='samples-%s.dat' % suffix, directory=self.outputdir)

        # binary export of infos
        if self.informative:
            dumper.dump (infos, name='infos-%s.dat' % suffix, directory=self.outputdir)

        # free memory
        samples = None
        infos = None

    # returns pandas dataframe with the requested number of parameter samples from
    # posterior distribution
    def __call__ (self, size=1, checkpointer=Checkpointer(600), profile=0):

        # initialize profile
        if profile:
            profile = cProfile.Profile ()
            profile.enable ()

        # initialize checkpointer
        if checkpointer is not None:
            checkpointer.init (self.verbosity >= 2)

        # initialize timer
        timer = Timer ()

        # initialize samples and infos
        samples = None
        infos = None

        # process all generated parameters
        for (parameters, info) in self.generator (size):

            # store samples
            if samples is None and infos is None:
                samples = pandas.DataFrame (parameters.copy (deep=1))
                if self.informative:
                    infos = [info]
            else:
                samples = samples.append (parameters, ignore_index=1, sort=True)
                if self.informative:
                    infos += [info]

            # save samples and infos at periodical checkpoints
            if checkpointer is not None:
                timestamp = checkpointer.check ()
                if timestamp is not None:
                    timer.start ()
                    self.flush (samples, infos, timestamp)
                    print ('Checkpointer took: ', timer.current ())

        # final checkpoint
        if checkpointer is not None and samples is not None and infos is not None:
            timestamp = checkpointer.check (force=1)
            timer.start ()
            self.flush (samples, infos, timestamp)
            print ('Checkpointer took: ', timer.current ())

        # dump profile
        if profile:
            profile.disable ()
            profile.create_stats ()
            profile.dump_stats (os.path.join (self.outputdir, 'profile.pstats'))

        return samples, infos
