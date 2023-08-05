# # # # # # # # # # # # # # # # # # # # # # # # # #
# Executor class using serial execution (no parallelization)
#
# Jonas Sukys
# Eawag, Switzerland
# jonas.sukys@eawag.ch
# All rights reserved.
# # # # # # # # # # # # # # # # # # # # # # # # # #

import copy
from collections import Iterable

from .executor import Executor
from ..utils.timing import Timing

class Serial (Executor):

    manager = 0
    workers = 1

    @staticmethod
    def address (peers):
        
        address = 0
        return address
    
    @staticmethod
    def universe_address ():

        address = None
        return address

    def bootup (self):

        # bind task
        self.taskroot = self.task.rootcall (peers=None)

        # init task executor
        if hasattr (self.task, 'executor'):
            self.taskport = self.task.executor.init (peers=None)
        else:
            self.taskport = None
        
        # serial executor simply forwards taskport onwards to other executors
        return self.taskport
    
    def shutdown (self):
        
        if hasattr (self.task, 'executor'):
            self.task.executor.exit ()

    def map (self, functions, parameters=None, *args):

        # setup timing
        self.timing = Timing ()

        # determine operational mode
        if parameters is not None:
            if isinstance (functions, Iterable):
                assert len (parameters) == len (functions)
                mode = 'MFMP' # multiple functions with multiple parameters
            else:
                mode = 'SFMP' # single function with multiple parameters
        else:
            mode = 'MFNP' # multiple functions with no parameters (should be specified in 'args')
        
        # prepare tasks according to the operational mode
        if mode == 'SFMP':
            function = functions
            self.prepare (function)
            function.root = self.taskroot
            if hasattr (function, 'executor'):
                function.executor.bind (self.taskroot, self.taskport)
            self.timing.start ('task')
            results = [ None ] * len (parameters)
            for index, ps in enumerate (parameters):
                results [index] = function (ps, *args)
            self.timing.time ('task')
        if mode == 'MFNP':
            for function in functions:
                self.prepare (function)
                function.root = self.taskroot
                if hasattr (function, 'executor'):
                    function.executor.bind (self.taskroot, self.taskport)
            self.timing.start ('task')
            results = [ None ] * len (functions)
            for index, function in enumerate (functions):
                results [index] = function (*args)
            self.timing.time ('task')
        if mode == 'MFMP':
            for function in functions:
                self.prepare (function)
                function.root = self.taskroot
                if hasattr (function, 'executor'):
                    function.executor.bind (self.taskroot, self.taskport)
            self.timing.start ('task')
            results = [ None ] * len (parameters)
            for index, function in enumerate (functions):
                results [index] = function (parameters [index], *args)
            self.timing.time ('task')

        timings = [self.timing]
        return results, timings
    
    def connect (self, ensemble, indices):

        self.timing = Timing ()
        self.ensemble = ensemble

        # prepare ensemble
        self.prepare (self.ensemble)
        
        # bind ensemble
        self.ensemble.root = self.taskroot

        # bind ensemble task
        self.ensemble.task.root = self.taskroot

        # bind ensemble task executor
        if hasattr (self.ensemble.task, 'executor'):
           self.ensemble.task.executor.bind (self.taskroot, self.taskport)

        # init ensemble
        self.timing.start ('init')
        self.ensemble.init (indices)
        self.timing.start ('init')
    
    # disconnect task ensemble
    def disconnect (self):
        
        self.ensemble.exit ()
        return []
    
    # report performance
    def report (self):

        return self.timing

    # execute ensemble method with specified args and return results
    def call (self, method, args=[], flatten=0, results=1):
        
        self.timing.start (method)
        call = getattr (self.ensemble, method)
        results = call (*args)
        self.timing.time (method)
        if results:
            return results
        else:
            return
    
    # resample (delete and replicate) tasks according to the specified indices
    def resample (self, indices):
        
        self.timing.start ('resample')

        # counter of particles (for each index - index is here id particle)
        keep_counters = {}

        # compute counts
        for index in indices:
            keep_counters [index] = []
        
        # count particles for each index
        for reindex, index in enumerate (indices):
            keep_counters [index] += [reindex]

        # new ensemble of resampled particles
        resampled = {}

        # replicate local particles according to 'keep_counters'
        for index, reindices in keep_counters.items():
            if len (reindices) > 0:
                reindex = reindices [0]
                resampled [reindex] = self.ensemble.particles [index]
                self.ensemble.prepare (reindex, resampled [reindex])
            if len (reindices) > 1:
                state = self.ensemble.particles[index].save ()
                for reindex in reindices [1:]:
                    resampled [reindex] = copy.deepcopy (self.ensemble.task)
                    self.ensemble.prepare (reindex, resampled [reindex])
                    resampled [reindex] .load (state)
                    self.ensemble.prepare (reindex, resampled [reindex])

        # finalize all extinct particles
        extinct = set (self.ensemble.particles.keys ()) - set (keep_counters.keys ())
        for index in extinct:
            self.ensemble.particles [index] .exit ()
 
        # replace particles
        self.ensemble.particles = resampled

        self.timing.time ('resample')
        
        # TODO: traffic should be estimated from ensembles and indices ('copy' part at least?)
        return None
    
    # abort
    def abort (self):
        
        import sys
        sys.exit ()