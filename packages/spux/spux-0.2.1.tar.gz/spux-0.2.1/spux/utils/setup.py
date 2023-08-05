# process setup
import numpy
from .sandbox import Sandbox
def setup (instance, sandbox, verbosity, seed, informative):
  
  # set sandbox
  if sandbox is not None:
      instance.sandbox = sandbox
  else:
      instance.sandbox = Sandbox (path=None)

  # set verbosity
  instance.verbosity = verbosity if verbosity >= 0 else 0

  # set seed and rng
  if seed is not None:
      instance.seed = seed
      instance.rng = numpy.random.RandomState (instance.seed ())
  
  # set informativity
  instance.informative = informative

  # report
  if instance.verbosity:
      print ("%s verbosity: %s" % (instance.name, instance.verbosity))
      if hasattr (instance, 'sandboxing') and instance.sandboxing:
        print ("%s sandbox: %s" % (instance.name, instance.sandbox))
      if hasattr (instance, 'seed') and instance.seed is not None:
        print ("%s seed: %s" % (instance.name, instance.seed))
      if hasattr (instance, 'infos'):
        print ("%s informative: %s" % (instance.name, instance.informative))
