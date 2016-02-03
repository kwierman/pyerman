from pyerman.root import BaseGenerator

class StepGenerator(BaseGenerator):
    def __init__(self, filename=""):
        BaseGenerator.__init__(self, filename, "output_step_world_DATA")

class TrackGenerator(BaseGenerator):
    def __init__(self, filename=""):
        BaseGenerator.__init__(self, filename, "output_track_world_DATA")
