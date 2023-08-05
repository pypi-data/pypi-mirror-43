# # # # # # # # # # # # # # # # # # # # # # # # # #
# Executor base class
#
# Jonas Sukys
# Eawag, Switzerland
# jonas.sukys@eawag.ch
# All rights reserved.
# # # # # # # # # # # # # # # # # # # # # # # # # #

from ..io.format import compactify

class AddressCall (object):

    def __init__ (self, root, owner, name, resources, addresscall):


        self.root = root
        self.owner = owner
        self.name = name
        self.resources = resources
        self.addresscall = addresscall

    def __call__ (self, peers):

        address = self.addresscall (peers)
        return self.root + [{'owner' : self.owner, 'name' : self.name, 'resources' : self.resources, 'address' : address}]

    def __str__ (self):

        out = '.'
        for level in self.root:
            out += '/%s-%s%s' % (level ['owner'], level ['name'], '-%d' % level ['address'] if level ['address'] is not None else '')
        out += '/%s-%s%s' % (self.owner, self.name, '-address()' if self.addresscall is not None else '')

        return out

class Executor (object):

    verbosity = 0

    @property
    def name (self):

        return type(self).__name__

    def setup (self, owner=None, rootcall=None, verbose=0, task=None):

        if owner is not None:
            self.task = owner.task
            self.owner = type(owner).__name__
            self.ownerbase = type(owner).__bases__[0].__name__
            if self.ownerbase == 'object':
                self.ownerbase = 'model'
        else:
            if task is not None:
                self.task = task
            else:
                self.task = None
            self.owner = 'none'
            self.ownerbase = 'none'
        self.rootcall = rootcall

        if self.verbosity and verbose:
            print ('%s executor setup: %s with rootcall: %s' % (self.owner, self.name, self.rootcall))

    # initialize executor
    def init (self, peers=None):
        
        # set root
        if self.rootcall is not None:
            self.root = self.rootcall (peers)
        else:
            self.root = []

        # prepare template task
        self.prepare (self.task)

        # bootup executor
        self.port = self.bootup ()
        if self.verbosity:
            print ('%s executor init: %s for a task %s with root %s and port %s' % (self.owner, self.name, type(self.task).__name__, compactify (self.root), self.port))

        return self.port
    
    # nice print of resources
    @staticmethod
    def table (resources):
        
        print (' :: Required resources:')
        print ('========================')
        strings = ['class', 'owner', 'task', 'executor']
        captions = ['class', 'owner', 'task', 'executor', 'manager', 'workers', 'resources', 'cumulative']
        print (' | '.join (['%15s' % label if label in strings else '%10s' % label for label in captions]))
        print (' + '.join (['-' * (15 if label in strings else 10) for label in captions]))
        if resources [-1] ['resources'] == 1:
            resource = {'class' : 'Model', 'owner' : resources [-1] ['task'], 'task' : '-', 'executor' : '-', 'manager' : 0, 'workers' : 1, 'resources' : 1, 'cumulative' : 1}
            print (' | '.join (['%15s' % resource[key] if key in strings else '%10d' % resource [key] for key in captions]))
        for resource in resources [::-1]:
            print (' | '.join (['%15s' % resource[key] if key in strings else '%10d' % resource [key] for key in captions]))

    # finalize executor
    def exit (self):
        
        # shutdown executor
        self.shutdown ()
        if self.verbosity:
            print ('%s executor exit: %s for a task %s' % (self.owner, self.name, type(self.task).__name__))

    # bind executor to a worker
    def bind (self, root, port):
        
        # set root
        self.root = root

        # set port
        self.port = port

        # report
        if self.verbosity:
            print ('%s executor bind: %s with root %s and port %s' % (self.owner, self.name, compactify (self.root), self.port))

    # prepate (setup) task executor
    def prepare (self, task):
        
        task.rootcall = self.addresscall ()
        if hasattr (task, 'executor'):
            task.executor.setup (task, rootcall=self.addresscall(), verbose=1)
    
    def resources (self, verbose=0):
        
        task_resources = self.task.executor.resources () if hasattr (self.task, 'executor') and hasattr (self.task.executor, 'resources') else []
        resources = task_resources [0] ['cumulative'] if len (task_resources) != 0 else 1
        cumulative = self.manager + self.workers * resources
        if self.verbosity and verbose:
            if hasattr (self, 'info'):
                print ('%s executor: %s with info:' % (self.owner, self.name), self.info ())
            print ('%s executor: %s with resources for each %s task:' % (self.owner, self.name, type(self.task).__name__), resources)
            print ('%s executor: %s with cumulative resources: %s%s x %d = %d' % (self.owner, self.name, '1 + ' if self.manager else '', self.workers, resources, cumulative))

        dictionary = {}
        dictionary ['class'] = self.ownerbase
        dictionary ['owner'] = self.owner
        dictionary ['task'] = type(self.task).__name__
        dictionary ['executor'] = self.name
        dictionary ['manager'] = self.manager
        dictionary ['workers'] = self.workers
        dictionary ['resources'] = resources
        dictionary ['cumulative'] = cumulative
        return [dictionary] + task_resources

    def addresscall (self):

        return AddressCall (self.root, self.owner, self.name, self.resources () [0] ['resources'], self.address)

    def capabilities (self, methods):
        
        if not all ([hasattr (self, method) for method in methods]):
            print (' :: ERROR: executor %s does not have all capabilities required by %s: %s' % (self.name, self.owner, methods))
            self.abort ()
