import vtk
import copy

import threading

class PointData:
    def __init__(self):
        self.x=0.0
        self.y=0.0
        self.z=0.0
        self.data = {}
    def copy(self):
        ret = PointData()
        ret.x = copy.copy(self.x)
        ret.y = copy.copy(self.y)
        ret.z = copy.copy(self.z)
        ret.data = copy.copy(self.data)


class DataGenerator():

    def __init__(self, filename, array_names=[]):
        self.reader = vtk.vtkXMLPolyDataReader()
        self.reader.SetFileName(filename)
        self.reader.Update()

        self.polydata = self.reader.GetOutput()
        self.n_points = self.polydata.GetNumberOfPoints()
        self.current_point = 0
        self.point = PointData()

        self.pointdata = self.polydata.GetPointData()
        n_arrays = self.pointdata.GetNumberOfArrays()
        self.array_map={}
        for name in array_names:
            self.point.data[name]=None
            for index in range(n_arrays):
                arr = self.pointdata.GetArray(index)
                if self.pointdata.GetArrayName(index)== name:
                    self.array_map[name]=arr
            if not name in self.array_map:
                raise IOError("No Array with Name: {} in file".format(name) )

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        if self.current_point+1 == self.n_points:
            raise StopIteration()
        self.point.x, self.point.y, self.point.z = self.polydata.GetPoint(self.current_point)
        #iterate through the data and pick out the relevent arrays
        for name in self.point.data:
            self.point.data[name] = self.array_map[name].GetTuple1(self.current_point)
        self.current_point+=1
        return self.point


class TrackStepsGenerator(DataGenerator):
    def __init__(self, filename, array_names):
        array_names.append('parent_track_id')
        super(DataGenerator, self).__init__(filename, array_names)
        self.track_id=0
        self.current_step=None
    def next(self):
        steps=[]
        if self.current_step == None:
            current_step = super(StepGenerator, self).next()
        while(self.current_step.data['parent_track_id']==self.track_id):
            steps.append(self.current_step.copy())
        self.track_id = self.current_step.data['parent_track_id']
        return steps


class TrackGenerator(DataGenerator):
    def __init__(self, track_filename, array_names):
        super(TrackGenerator, self).__init__(filename, array_names)
        self.track_id=0
        self.current_step=None
