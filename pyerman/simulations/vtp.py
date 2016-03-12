import vtk


class VTKAnalysisObject:
    def onInit(self):
        pass
    def onBuild(self):
        pass
    def onFinish(self):


def readinTrackData(filename=""):
    reader = vtk.XMLPolyDataReader()
    reader.SetFileName(fileaname)
    reader.Update()
