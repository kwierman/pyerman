import copy

class ObjectBase(object):
    def __init__(self, data, tree):
        self.data=data
        self.tree=tree
        self.onCreate()

    def onCreate(self):
        """
            Declare Variables and Defaults here
            self.name = "Default"
            self.z = 1.e6
        """
        pass

    def onComplete(self):
        """
            Copy out values from data to variables here
            as such:
            self.name = self.copyString("creator_name")
            self.z = self.copy("position_z")
        """
        pass

    def copy(self, leaf):
        return copy.copy(self.data[leaf].GetValue())

    def copyString(self, leaf):
        s = list( getattr(self.tree,leaf))
        return ''.join(s)

class Step(ObjectBase):
    pass

class Track(ObjectBase):
    def __init__(self, data, tree):
        ObjectBase.__init__(self, data, tree)
        self.steps=[]
        self.isFirst = self.copyString("creator_name") == 'egun_electrons'
        self.n_steps = int(self.copy('total_steps'))
    def isFull(self):
        return len(self.steps) == self.n_steps


class Event(ObjectBase):
    def __init__(self, data, tree):
        ObjectBase.__init__(self, data, tree)
        self.tracks=[]


class Run(ObjectBase):
    def __init__(self, data, tree):
        ObjectBase.__init__(self, data, tree)
        self.events = []

class Composite(ObjectBase):
    def __init__(self, data, tree):
        ObjectBase.__init__(self, data, tree)
        self.runs = []
    def onAddRun(self, run):
        pass
