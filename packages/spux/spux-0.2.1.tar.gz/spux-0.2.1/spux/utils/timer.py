# # # # # # # # # # # # # # # # # # # # # # # # # #
# Timer class
#
# Jonas Sukys
# Eawag, Switzerland
# jonas.sukys@eawag.ch
# All rights reserved.
# # # # # # # # # # # # # # # # # # # # # # # # # #

import timeit

class Timer(object):

    def __init__(self):

        self.total = 0.0

    def current(self):

        return timeit.default_timer() - self.time

    def pause(self):

        self.total += self.current()

    def start(self):

        self.time = timeit.default_timer()

    def timestamp(self):

        return (self.time, timeit.default_timer())
