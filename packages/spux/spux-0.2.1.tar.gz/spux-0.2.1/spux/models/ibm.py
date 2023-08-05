# # # # # # # # # # # # # # # # # # # # # # # # # #
# Individual Based Model class
# Based on: Kattwinkel & Reichert, EMS 2017.
#
# Jonas Sukys
# Eawag, Switzerland
# jonas.sukys@eawag.ch
# All rights reserved.
# # # # # # # # # # # # # # # # # # # # # # # # # #

import os, re

import numpy

from spux.models.model import Model

from spux.drivers import java
from spux.io import parameters as txt
from spux.utils.seed import Seed
from spux.utils.sandbox import Sandbox
from spux.utils.annotate import annotate

class IBM (Model): #(object)

    # construct IBM for the specified 'config'
    def __init__(
        self,
        config,
        classpath=None,
        inputpath=None,
        jvmpath=None,
        jvmargs="-Xmx1G",
        serialization="binary",
    ):

        #find name of input files
        fullfile = os.path.join('input/input/',config)
        if not os.path.isfile(fullfile):
          fullfile = config #for tests - still not enough
        #
        keys = ["fNameInputUniParam","fNameInputTaxParam","fNameInputTaxNames"]
        self.infls = []
        with open (fullfile, 'r') as fl:
            for line in fl:
                if re.match(keys[0],line) or re.match(keys[1],line):
                    self.infls.append( ((line.split(':')[1]).strip('\n')).strip('\t') )
                elif re.match(keys[2],line):
                    specsfl = ( (line.split(':')[1]).strip('\n') ).strip('\t')

        #get name of species (labels)
        fullfile = os.path.join('input/input/',specsfl)
        if not os.path.isfile(fullfile):
            fullfile = os.path.join('IBM/input/input/',specsfl) #for tests - still not enough
        with open(fullfile, 'r') as fl:
            next(fl)
            self.species = [ line.strip('\n') for line in fl ]

        self.config = config

        # Java Virtual Machine arguments
        self.jvmpath = jvmpath
        self.classpath = classpath
        self.jvmargs = jvmargs

        self.inputpath = inputpath
        self.serialization = serialization

        # initially neither interface nor model do exist
        self.interface = None
        self.model = None

        # sandboxing
        self.sandboxing = 1

    # setup driver
    def driver (self):

        # start Java Virtual Machine
        if self.verbosity:
            print("IBM %s: setup -> driver" % self.sandbox())

        driver = java.Java (jvmpath=self.jvmpath, classpath=self.classpath, jvmargs=self.jvmargs)

        # get model class
        if self.verbosity:
            print("IBM %s: setup -> model" % self.sandbox())
        self.Model = driver.get_class("mesoModel.TheModel")

        # construct ModelWriterReader object for later save/load
        if self.verbosity:
            print("IBM %s: setup -> interface" % self.sandbox())
        Interface = driver.get_class("mesoModel.ModelWriterReader")
        self.interface = Interface()

    def setup (self, sandbox=Sandbox(), verbosity=1, seed=Seed(), informative=1):

        # base class 'setup (...)' method
        Model.setup (self, sandbox, verbosity, seed, informative)

        # if interface does not exist
        if self.interface is None:

            # setup driver
            self.driver ()

        # if model exists - the java model
        if self.model is not None:

            # set path
            if self.verbosity:
                print("IBM %s: setup -> setPaths ()" % self.sandbox())
            self.model.setPaths (self.sandbox())

            # set seed
            if self.verbosity:
                print("IBM %s: setup -> reinitiliazeModel ()" % self.sandbox())

            # pass array of seeds to Java source code
            self.model.reinitializeModel (self.seed ())

    # initialize IBM using specified 'input' and 'parameters'
    def init (self, input, parameters):

        # print("self: %s" %(self)) # ibm.IBM
        if self.verbosity:
            print("IBM %s: init parameters:" % self.sandbox())
            print(parameters)

        # base class 'init (...)' method
        Model.init (self, input, parameters)

        # copy all required input files
        self.sandbox.copyin (self.inputpath)

        path = os.path.join(self.sandbox(), "input")

        #update parameter values in model input filr
        for filename in self.infls:
            inputfile = os.path.join(path, filename)
            available = txt.load(inputfile)
            for label, value in parameters.items():
                if label in available:
                    available [label] = [value] [0]
            txt.save(available, inputfile, delimiter="\t")

        # construct model object - set self.model to the java Model
        if self.verbosity:
            print("IBM %s: init -> model" % self.sandbox())
        self.model = self.Model (self.seed ())

        # set path
        if self.verbosity:
            print("IBM %s: init -> setPaths ()" % self.sandbox())
        self.model.setPaths (self.sandbox())

        # run model initialization for the specified 'config'
        if self.verbosity:
            print("IBM %s: init -> initModel ()" % self.sandbox())
        self.config

        try:
            self.model.initModel ([self.config])
        except:
            raise ValueError("Caught the runtime exception on java.")

        # simulation initialization
        if self.verbosity:
            print("IBM %s: init -> initSimulation ()" % self.sandbox())

        self.model.initSimulation()

        if self.verbosity:
            print("IBM %s: init -> runSimulationInitExtPartFiltering ()" % self.sandbox())
        self.model.runSimulationInitExtPartFiltering()

    # run IBM up to specified time and return the prediction
    def run (self, time):

        # base class 'init ()' method
        Model.run (self, time)

        # run model up to specified time
        self.model.runModelExtPartFiltering(int(time))

        # get model output
        observation = self.model.observe()
        observation = numpy.array (observation)
        sums = numpy.sum (observation, axis=0)

        labels = self.species

        return annotate(sums,labels,time)

    # save current model state
    def save (self):

        # TODO: have a separate Java serializer JAR instead of 'model.interface.writeModelByteArray (...)' OR write it in jpype directly?

        if self.serialization == "binary":
            buffer_ = self.interface.writeModelByteArray (self.model)
            state = java.Java.save(buffer_)

        # - name of the file where state was saved (slow)
        if self.serialization == "pickle":
            state = os.path.join (self.sandbox(), "state.dat")
            self.interface.writeModel (state, self.model)

        if self.verbosity:
            print("IBM: save", self.sandbox())

        return state

    # load specified model state
    def load (self, state):

        # TODO: have a separate Java serializer JAR instead of 'model.interface.loadModelByteArray (...)' OR write it in jpype directly?

        if self.verbosity:
            print("IBM: load", state, self.sandbox())

        # TODO: should we also call a self.sandbox.copyin (state) to copy in needed files? At least we should call self.sandbox.copyin (self.inputpath)?

        # - binary array representing serialize model state (fast)
        if self.serialization == "binary":
            buffer_ = java.Java.load(state)
            self.model = self.interface.loadModelByteArray(buffer_)

        # - name of the file where state was saved (slow)
        if self.serialization == "pickle":
            self.model = self.interface.loadModel(state)

    # construct a data container for model state with a specified size
    def state (self, size):

        # TODO: have a separate java model class with an appropriate routine here?

        return numpy.empty (size, dtype="uint8")

    # cleanup
    def exit (self):

        # base class 'exit ()' method
        Model.exit (self)

        if self.serialization == "pickle":
            state = os.path.join(self.sandbox(), "state.dat")
            if os.path.exists(state):
                os.remove(state)
