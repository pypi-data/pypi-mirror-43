# # # # # # # # # # # # # # # # # # # # # # # # # #
# Ensemble class
# For particle filtering based on
# Kattwinkel & Reichert, EMS 2017.
#
# Jonas Sukys
# Eawag, Switzerland
# jonas.sukys@eawag.ch
# All rights reserved.
# # # # # # # # # # # # # # # # # # # # # # # # # #

from copy import deepcopy as copy

from ..utils.setup import setup
from ..utils.seed import Seed
from ..io.format import compactify

class Ensemble (object):

    @property
    def name (self):

        return type(self).__name__

    # constructor requires dynamical system 'model' including its 'input' and 'parameters', and the 'error' distribution for prediction validation
    def __init__(self, model, input, parameters, error, log=1):

        self.model = model
        self.input = input
        self.parameters = parameters
        self.error = error
        self.log = log

        self.sandboxing = model.sandboxing

        # seeds for iterations
        self.seeds = {}

        self.task = self.model

    # setup ensemble
    def setup (self, sandbox=None, verbosity=1, seed=Seed(), informative=1):

        # standardized setup
        setup (self, sandbox, verbosity, seed, informative)
    
    # prepare particles sandboxes and seeds
    def prepare (self, index, particle):
       
        sandbox = self.sandbox.spawn ("P%04d" % index) if self.sandboxing else None
        seed = self.seeds [self.iteration] .spawn (index, name='PF index')
        particle.setup (sandbox, self.verbosity - 1, seed=seed, informative=self.informative)
    
    # initialize ensemble
    def init (self, indices):

        if self.verbosity:
            print("Ensemble init with root", compactify (self.root))

        # set iteration
        self.iteration = 0
       
        # set iteration seed
        self.seeds [self.iteration] = self.seed.spawn (self.iteration, name='PF iteration')

        # construct particles and sandboxes
        self.particles = {}
        for index in indices:
            self.particles [index] = copy (self.model)
            self.prepare (index, self.particles [index])

        # initialize particles with specified parameters
        for index, particle in self.particles.items ():
            particle.init (self.input, self.parameters)

    # advance ensemble state to next iteration
    def advance (self):

        if self.verbosity:
            print("Ensemble advance with root", compactify (self.root))
        
        # set iteration
        self.iteration += 1

        # set iteration seed
        self.seeds [self.iteration] = self.seed.spawn (self.iteration, name='PF iteration')

    # run all particles in ensemble up to the specified time
    def run (self, time):

        self.time = time

        if self.verbosity:
            print("Ensemble run with root", compactify (self.root))

        self.predictions = {}
        for index, particle in self.particles.items ():
            self.predictions [index] = particle.run (time)

        return self.predictions

    # compute errors for all particles in ensemble
    def errors (self, data):

        if self.verbosity:
            print("Ensemble errors with root", compactify (self.root))
        
        # transform data if error requires so
        if hasattr (self.error, 'transform'):
            data = self.error.transform (data, self.parameters)

        errors = {}
        for index, particle in self.particles.items():
            labels = self.predictions [index] .keys()
            distribution = self.error.distribution (self.predictions [index], self.parameters)
            if self.log:
                errors [index] = distribution.logpdf (data [labels])
            else:
                errors [index] = distribution.pdf (data [labels])
        
        return errors

    # cleanup
    def exit(self):

        if self.verbosity:
            print("Ensemble exit with root", compactify (self.root))

        for index, particle in self.particles.items():
            particle.exit()
