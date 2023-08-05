
import numpy

# convert dict with integer keys to numpy array - assume user plays nice
def numpyfy (dictionary):
  
  values = [ dictionary [key] for key in range (len (dictionary)) ]
  return numpy.array (values)
