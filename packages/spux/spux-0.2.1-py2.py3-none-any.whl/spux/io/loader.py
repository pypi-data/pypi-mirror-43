# # # # # # # # # # # # # # # # # # # # # # # # # #
# Cloudpickle-based loader class
#
# Jonas Sukys
# Eawag, Switzerland
# jonas.sukys@eawag.ch
# All rights reserved.
# # # # # # # # # # # # # # # # # # # # # # # # # #

import cloudpickle
import os
import glob

def load (name="dump.dat", directory="output"):

    path = os.path.join (directory, name)
    paths = sorted (glob.glob (path))
    for path in paths:
        with open (path, "rb") as f:
            yield cloudpickle.load (f)
