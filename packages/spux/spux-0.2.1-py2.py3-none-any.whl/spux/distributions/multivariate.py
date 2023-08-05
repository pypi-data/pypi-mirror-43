# # # # # # # # # # # # # # # # # # # # # # # # # #
# Wrapper class for multivariate distributions from scipy.stats
# For a review of wrap'able distributions, see the multivariate section in:
# https://docs.scipy.org/doc/scipy/reference/stats.html
#
# Jonas Sukys
# Eawag, Switzerland
# jonas.sukys@eawag.ch
# All rights reserved.
# # # # # # # # # # # # # # # # # # # # # # # # # #

import pandas

from .distribution import Distribution

class Multivariate (Distribution):

  def __init__ (self, distribution, labels):
    
    self.distribution = distribution
    self.labels = labels
  
  # evaluate a joint PDF
  # 'parameters' is assumed to be of a pandas.DataFrame type
  def pdf (self, parameters):
    
    ordered = [ parameters [label] for label in self.labels ]
    return self.distribution.pdf (ordered)

  # evaluate a joint log-PDF
  # 'parameters' is assumed to be of a pandas.DataFrame type
  def logpdf (self, parameters):
    
    ordered = [ parameters [label] for label in self.labels ]
    return self.distribution.logpdf (ordered)

  # draw a random parameter vector using the provided RNG engine
  # 'offset' is assumed to be of a pandas.DataFrame type
  def draw (self, rng, offset = None):
    
    parameters = self.distribution.rvs (random_state = rng)
    parameters = { label : parameters [index] for index, label in enumerate (self.labels) }
    parameters = pandas.DataFrame.from_dict (parameters)
    if offset:
      parameters += offset
    return parameters
