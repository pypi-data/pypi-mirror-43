
import numpy

import numba
OrnsteinUhlenbeck_numba_spec = [
    ('tau', numba.float64),
    ('t', numba.float64),
    ('xi', numba.float64),
]

class OrnsteinUhlenbeck (object):

    def __init__ (self, tau):

        self.tau = tau

    def init (self, t, xi):

        self.t = t
        self.xi = xi
    
    def evaluate (self, t, seed):
        
        if t < self.t:
            assert t >= self.t, ' :: ERROR: OU process assumes evaluation of increasing time sequence, and not %f < %f, unless prepare (...) was called' % (t, self.t)
        if t == self.t:
            return self.xi
        dt = t - self.t
        V = 1.0 - numpy.exp (-2 * dt / self.tau)
        E = self.xi * numpy.exp (-dt / self.tau)
        rng = numpy.random.RandomState (seed=seed)
        self.xi = rng.normal (loc=E, scale=numpy.sqrt (V))
        self.t = t
        return numpy.float64 (self.xi)

# legacy class with prepare () for integrators that make steps back in time
# class OrnsteinUhlenbeck (object):

#     def __init__ (self, tau):

#         self.tau = tau

#     def setup (self, rng):

#         self.rng = rng
#         self.prepared = 0

#     def init (self, t, xi):

#         self.t = t
#         self.xi = xi
#         self.prepared = 0
    
#     def prepare (self, t, dt):
        
#         self.times = numpy.arange (self.t, t + dt, dt)
#         self.times [-1] = t
#         self.samples = numpy.empty (len (self.times))
#         for index, time in enumerate (self.times):
#             self.samples [index] = self (time)
#         self.prepared = 1
    
#     def __call__ (self, t, dt=None):
        
#         if t < self.t:
#             if not self.prepared:
#                 assert t >= self.t, ' :: ERROR: OU process assumes evaluation of increasing time sequence, and not %f < %f, unless prepare (...) was called' % (t, self.t)
#             else:
#                 return numpy.interp (t, self.times, self.samples)
#         if t == self.t:
#             return self.xi
#         if dt is None:
#             dt = t - self.t
#             times = [t]
#         else:
#             times = numpy.arange (self.t + dt, t, dt)
#         V = 1.0 - numpy.exp (-2 * dt / self.tau)
#         for time in times:
#             # TODO: E can be moved outside the for-loop, with a posterior adjustments
#             E = self.xi * numpy.exp (-dt / self.tau)
#             self.xi = self.rng.normal (loc=E, scale=numpy.sqrt (V))
#             self.t = t
#             #increments = distribution.rvs (len (times))
#         #noise = numpy.cumsum (increments)
#         #self.xi += noise [-1]
#         #self.t = times [-1]
#         return self.xi
