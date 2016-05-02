import copy


class Field(object):
    """
        This is a dummy object
    """
    pass

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

    def get(self, leaf):
        return self.data[leaf].GetValue()

    def copyString(self, leaf):
        s = list( getattr(self.tree,leaf))
        return ''.join(s)

    def getString(self, leaf):
        s = list( getattr(self.tree,leaf))
        return ''.join(s)

class Step(ObjectBase):
    pass


class Track(ObjectBase):
    fields = ['total_steps']
    def __init__(self, data, tree):
        ObjectBase.__init__(self, data, tree)
        self.steps=[]
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
    def __init__(self):
        ObjectBase.__init__(self, None, None)
        self.runs = []
    def onAddRun(self, run):
        pass


class DefaultStep(Step):
    fields=[]
    def onComplete(self):
        for i in self.fields:
            setattr(self, i, self.copy(i))


class DefaultStepAggregator(Track):
    fields=[]
    def onComplete(self):
        for field in self.fields:
            setattr(self, field, [])
        for step in self.steps:
            for field in self.fields:
                getattr(self, field).append(getattr(step,field))


class DefaultTrackAggregator(Event):
    fields=[]
    def onComplete(self):
        for field in self.fields:
            setattr(self, field, [])
        for step in self.steps:
            for field in self.fields:
                getattr(self, field).append(getattr(step,field))
