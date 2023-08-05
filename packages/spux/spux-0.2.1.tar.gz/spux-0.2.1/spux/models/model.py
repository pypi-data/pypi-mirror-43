# # # # # # # # # # # # # # # # # # # # # # # # # #
# Base model class
# All class methods can be extended by inheriting and overwriting
#
# Jonas Sukys
# Eawag, Switzerland
# jonas.sukys@eawag.ch
# All rights reserved.
# # # # # # # # # # # # # # # # # # # # # # # # # #

import cloudpickle

from ..utils.setup import setup
from ..utils.sandbox import Sandbox
from ..utils.seed import Seed

# List of Model class variables (identical for all instances)
# that could be modified in the custom constructor of the this inherited base class
# self.sandboxing - enable (set to 1), the default option, or disable (set to 0) sandboxing (see below for self.sandbox () usage)
# self.serialization:
#  - 'binary' : [default] fast - uses bytes vector for a state (consider using 'cloudpickle.dumps' / 'cloudpickle.loads')
#  - 'pickle' : slow - uses any generick pickle'able object for a state (try to avoid at all costs)

# List of Model instance varialbles (different for each instance) set by 'setup ()' and available in all other methods:
# self.sandbox () - path to an isolated sandbox directory (if self.sandboxing == 1)
# self.verbosity - a integer indicating verbosity level for 'print ()' intensity management
# self.seed () - a list containing all hierarchical seeds
# self.seed.cumulative () - a (large) integer seed obtained by combining all hierarchical seeds
# self.rng - numpy.random.RandomState (self.seed ()) object for use as 'random_state' in the scipy.stats distributions

class Model (object):

    # sandboxing enabled by default
    sandboxing = 1

    # binary serialization by default
    serialization = 'binary'

    @property
    def name (self):

        return type(self).__name__
    
    # attach an executor
    def attach (self, executor):

        self.executor = executor
        self.executor.setup (self)

    # setup model using specified 'sandbox', 'verbosity' and 'seed'
    # setup is called before 'init (...)' and before/after (i.e. two identical calls to allow flexibility in models) 'load (...)'
    def setup (self, sandbox=Sandbox(), verbosity=1, seed=Seed(), informative=1):
        
        setup (self, sandbox, verbosity, seed, informative)
        
        # OPTIONAL: inherit this base class and write a custom 'setup (...)' method
        # you can additionally execute base method by 'Model.setup (self, sandbox, verbosity, seed)'
        
        # ADVICE: create here all needed dynamical links to your model (loaded DLLs, Java Virtual Machine, etc.)
        # RATIONALE: 'model.load (...)' could be called immediately after 'model.setup (...)',
        # i.e. without calling model.init (...) or model.run (...) beforehand

    # initialize model using specified 'input' and 'parameters'
    def init (self, input, parameters):

        if self.verbosity:
            print ("%s model in sandbox %s: init input and parameters:" % (self.name, self.sandbox()))
            print (input)
            print (parameters)
        
        # inherit this base class and write a custom 'init (...)' method
        # you can additionally execute base method by
        # 'Model.init (self, input, parameters)'

        # if sandboxing is enabled, one could copy in all needed files
        # from a specified self.inputpath (to be set in constructor) using
        # 'self.sandbox.copyin (self.inputpath)'

    # run model up to specified 'time' and return the prediction
    def run (self, time):

        if self.verbosity:
            print("%s model in sandbox %s: run" % (self.name, self.sandbox()))
        
        # inherit this base class and write a custom 'run (...)' method
        # you can additionally execute base method by 'Model.run (self, time)'

        # to return annotated results, use 'annotate' from spux.utils.annotate, e.g.
        # return annotate (y, ['y'], time)

    # finalize model
    def exit (self):

        if self.verbosity:
            print("%s model in sandbox %s: exit" % (self.name, self.sandbox()))
        
        # OPTIONAL: inherit this base class and write a custom 'exit (...)' method
        # you can additionally execute base method by 'Model.exit (self)'

    # save current model into its state
    # this is a fully functional method for pure Python models
    # OPTIONAL: inherit this base class and write a custon 'save (...)' method for other models
    # you can use helper routines in spux/drivers/ - check their sample usage in examples/
    def save (self):
        
        if self.verbosity:
            print ("%s model in sandbox %s: save" % (self.name, self.sandbox()))

        state = cloudpickle.dumps (self.__dict__)
        return state

    # load specified model from its state
    # this is a fully functional method for pure Python models
    # OPTIONAL: inherit this base class and write a custon 'load (...)' method for other models
    # you can use helper routines in spux/drivers/ - check their sample usage in examples/
    def load (self, state):
        
        if self.verbosity:
            print("%s model in sandbox %s: load" % (self.name, self.sandbox()))
        
        self.__dict__ = cloudpickle.loads (state)
    
    # construct a data container for model state with a specified size
    # this is a functional method for pure Python models
    # OPTIONAL: inherit this base class and write a custon 'state (...)' method for other models
    # you can use helper routines in spux/drivers/ - check their sample usage in examples/
    def state (self, size):

        return bytearray (size)
