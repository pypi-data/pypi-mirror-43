# # # # # # # # # # # # # # # # # # # # # # # # # #
# Base likelihood class
#
# Jonas Sukys
# Eawag, Switzerland
# jonas.sukys@eawag.ch
# All rights reserved.
# # # # # # # # # # # # # # # # # # # # # # # # # #

from ..utils.setup import setup
from ..utils.seed import Seed
from ..executors.serial import Serial

class Likelihood (object):
    
    @property
    def name (self):

        return type(self).__name__
    
    # assign required components to likelihood
    def assign (self, model, error=None, data=None, input=None):

        self.model = model
        self.error = error
        self.data = data
        self.input = input

        self.sandboxing = self.model.sandboxing
        self.task = self.model

        if not hasattr (self, 'executor'):
            self.attach (Serial ())
    
    # attach an executor
    def attach (self, executor):

        self.executor = executor
        self.executor.setup (self)
        methods = ['connect', 'call', 'resample', 'disconnect']
        self.executor.capabilities (methods)

    # setup likelihood
    def setup (self, sandbox=None, verbosity=1, seed=Seed(), informative=1):

        # standardized setup
        setup (self, sandbox, verbosity, seed, informative)
