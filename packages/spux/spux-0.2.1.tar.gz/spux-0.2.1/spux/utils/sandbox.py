# # # # # # # # # # # # # # # # # # # # # # # # # #
# Sandbox class
#
# Jonas Sukys
# Eawag, Switzerland
# jonas.sukys@eawag.ch
# All rights reserved.
# # # # # # # # # # # # # # # # # # # # # # # # # #

import os
import sys
import shutil
import errno

class Sandbox (object):

    # constructor
    def __init__ (self, path='sandbox', target=None):

        self.target = target
        if target is None:
          self.path = path
          if path and not os.path.exists (path):
            os.makedirs(path, exist_ok=True)
        else:
          self.path = target if path is not None else None
          if path:
            if not os.path.exists (target):
              os.makedirs (target, exist_ok=True)
            try:
                os.symlink (target, path)
            except OSError as e:
                if e.errno == errno.EEXIST:
                    os.remove(path)
                    os.symlink(target, path)
                else:
                    raise e
          else:
            print (" :: ERROR: In sandbox, please specify a name for the symlink as path or set target to None and path to your working directory path.")
            sys.exit ()

    # get sandbox path
    def __call__ (self):

        return self.path

    # get sandbox description
    def __str__ (self):

        return '%s%s' % (self.path, (' -> %s' % self.target) if self.target is not None else '')

    # spawn new sandbox
    def spawn (self, name):

        if self.path:
            path = os.path.join (self.path, name)
        else:
            path = None

        return Sandbox (path)

    # copy all files from a given input directory to the sandbox
    def copyin (self, inputpath):

        # copy all required input files, if inputpath is valid
        if inputpath:

            # copy only if directory is empty
            if os.listdir (self.path) == []:

                # remove directory
                shutil.rmtree (self.path)

                # copy all files
                shutil.copytree (inputpath, self.path)

    # clean
    def clean (self):

        # remove entire sandbox
        if self.path is not None and os.path.exists (self.path):
            shutil.rmtree (self.path)
