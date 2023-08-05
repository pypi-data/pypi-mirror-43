# # # # # # # # # # # # # # # # # # # # # # # # # #
# Base class for distributions
#
# Jonas Sukys
# Eawag, Switzerland
# jonas.sukys@eawag.ch
# All rights reserved.
# # # # # # # # # # # # # # # # # # # # # # # # # #

import pandas

class Distribution (object):

  # evaluate a joint PDF of the distribution
  # 'parameters' is assumed to be of a pandas.DataFrame type
  def pdf (self, parameters):

    return float ('nan')

  # evaluate a joint log-PDF of the distribution
  # 'parameters' is assumed to be of a pandas.DataFrame type
  def logpdf (self, parameters):

    return float ('nan')

  # return intervals (for each parameter) for the specified centered probability mass
  def intervals (self, alpha):

    return { 'parameter' : [float ('nan'), float ('nan')] }

  # draw a random vector using the provided RNG engine
  # 'offset' is assumed to be of a pandas.DataFrame type
  def draw (self, rng, offset = None):

    parameters = { 'parameter' : float ('nan') }
    parameters = pandas.DataFrame (parameters, index=range(1))
    if offset is not None:
      parameters += offset
    return parameters
