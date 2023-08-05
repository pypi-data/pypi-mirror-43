# # # # # # # # # # # # # # # # # # # # # # # # # #
# Java driver class
#
# Jonas Sukys
# Eawag, Switzerland
# jonas.sukys@eawag.ch
# All rights reserved.
# # # # # # # # # # # # # # # # # # # # # # # # # #

import os
#import socket
#import traceback

from sys import platform, version_info

import numpy

CLASSPATH_SEP = ";" if platform == "win32" else ":"

IS_VENV = os.environ.get("VIRTUAL_ENV") is not None


class Java(object):
    """Convenience wrapper for Python Java bindings.

    WARNING: due to underlying Python Java bindings library limitations, you
    cannot run a single Python process that uses this driver at least twice but
    with different Java classpaths. The subsequent classpaths won't correctly
    load.
    """
    jpype = None
    started_in = set()

    _jpype = None

    @classmethod
    def _get_jpype(cls):
        if cls._jpype is None:
            try:
                import jpype
            except ImportError:
                if (
                    version_info.major < 3
                ):
                    raise RuntimeError("you can only use java models with Python 3")
                if IS_VENV:
                    raise ImportError("please run 'pip3 install --user JPype1' first.")
                else:
                    raise ImportError(
                        "please run 'pip3 install --user JPype1' first."
                    )

            cls._jpype = jpype

        return cls._jpype

    def __init__(self, jvmpath=None, classpath=None, jvmargs="", cwrank=-1):

        # import pdb; pdb.set_trace()
        jpype = self._get_jpype()

        if jvmpath is None:
            jvmpath = jpype.getDefaultJVMPath()

        if not jpype.isJVMStarted(): #we get here at instantiation of first particle per PF worker

            jpype.startJVM(
                jvmpath,
                "-XX:ParallelGCThreads=1",
                jvmargs,
                "" if classpath is None else ("-Djava.class.path=%s" % classpath),
            )

        #else:
        #    print("Instantiating another JVM - this may be bad. I dunno."," cwrank: ",cwrank)
        # raise RuntimeError(
        # "you can not use two instances of JVM in the same process"
        # )

    # FIXME: enable JVM shutdown
    # def __enter__(self):
    #     return self
    #
    # def __exit__(self, exc_type, exc_value, traceback):
    #     jpype = self._get_jpype()
    #     if jpype.isJVMStarted():
    #         jpype.shutdownJVM()

    def get_class(self, name):
        # print("=== in get_class of Java in java.py =====")
        # print("self:",self) # spux.drivers.java.Java
        jpype = self._get_jpype()
        assert jpype is not None, "please instantiate Java first"
        return jpype.JClass(name)
        # print("=== done get_class of Java in java.py ===")

    @classmethod
    def save(cls, buffer_):
        state = numpy.empty(len(buffer_), dtype="uint8")

        try:
            state[:] = buffer_[:]  # fails almost always
        except:
            #print("I am in save of java.py with a warning")
            jpype = cls._get_jpype()
            Jstr = jpype.java.lang.String(buffer_,'ISO-8859-1').toString().encode('UTF-16LE')
            bytearr = numpy.array(numpy.frombuffer(Jstr, dtype='=u2'), dtype=numpy.byte)
            state = numpy.frombuffer(bytearr, dtype="uint8")
            #for i in range(0,len(state)):
            #    state[i] = buffer_[i]

        #print("I am in save of java.py with buffer_: ",buffer_[0:10])
        #print("I am in save of java.py with type(buffer_): ",type(buffer_))
        #print("I am in save of java.py with type(buffer_[0]): ",type(buffer_[0]))
        #print("I am in save of java.py with len(buffer_): ",len(buffer_))
        #print("done with save of java.py")

        return state

    @classmethod
    def load(cls, state):

        #print("I am in load of java.py")
        #import pdb; pdb.set_trace()
        jpype = cls._get_jpype()
        JByteArray = jpype.JArray(jpype.JByte)
        buffer_ = JByteArray(len(state))
        try:
            buffer_[:] = state[:]
            #buffer = state
        except:
            #print("I am in load of java.py with a warning")
            tmpstate = numpy.frombuffer(state,dtype="b") #int8,B
            buffer_ = jpype.JArray(jpype.JByte,1)(tmpstate.tolist())

        #print("I am in load of java.py with buffer_: ",buffer_[0:10])
        #print("I am in load of java.py with type(buffer_): ",type(buffer_))
        #print("I am in load of java.py with type(buffer_[0]): ",type(buffer_[0]))
        #print("I am in load of java.py with len(buffer_): ",len(buffer_))
        #print("done with load of java.py")

        return buffer_

    @classmethod
    def state(cls, size):
        # print('I AM IN JAVA DRIVER state of java.py')
        jpype = cls._get_jpype()

        JByteArray = jpype.JArray(jpype.JByte)
        state = JByteArray(size)
        return state
