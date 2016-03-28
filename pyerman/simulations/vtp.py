import vtk


class PointData:
    def __init__(self):
        self.x=0.0
        self.y=0.0
        self.z=0.0
        self.data = {}


class VTPDataGenerator():

    def __init__(self, filename, array_names=[]):
        self.reader = vtk.vtkXMLPolyDataReader()
        self.reader.SetFileName(filename)
        self.reader.Update()

        self.polydata = self.reader.GetOutput()
        self.n_points = self.polydata.GetNumberOfPoints()
        self.current_point = 0
        self.point = PointData()

        #initialize the array
        self.pointdata = self.polydata.GetPointData()
        n_arrays = self.pointdata.GetNumberOfArrays()
        self.array_map={}
        for name in array_names:
            self.point.data[name]=None
            for index in range(n_arrays):
                arr = self.pointdata.GetArray(index)
                if self.pointdata.GetArrayName(index)== name:
                    self.array_map[name]=arr

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



class VTPStepGenerator(VTPDataGenerator):
    pass
