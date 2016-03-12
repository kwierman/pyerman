from .generators import StepGenerator, TrackGenerator, EventMetadataGenerator
from .objects import Step, Track, Event, Run

class BaseFiller(object):
    def __iter__(self):
        return self
    def __len__(self):
        return 0
    def __next__(self):
        return self.next()
    def next(self):
        pass


class StepFiller(BaseFiller):
    def __init__(self, filename=""):
        self.step_gen = StepGenerator(filename)
        self.step_class = Step
    def next(self):
        """
        raises: StopIteration if it hits the end of the steps in the file
        """
        dat, tree = next(self.step_gen)
        step = self.step_class(dat, tree)
        step.onComplete()
        return step


class TrackFiller(BaseFiller):
    def __init__(self, filename=""):
        self.track_gen = TrackGenerator(filename)
        self.step_filler = StepFiller(filename)
        self.track_class = Track
    def next(self):
        dat, tree = next(self.track_gen)
        track = self.track_class (dat, tree)
        if self.step_filler is not None:
            while not track.isFull():
                # WHATEVER YOU DO, DO NOT PUT EXCEPTION HANDLING HERE< IT WILL
                # BREAK RECONSTRUCTION AT THE GENERATOR LEVEL
                # IN PYTHON <3
                track.steps.append(next(self.step_filler))
        track.onComplete()
        return track


class EventFiller(BaseFiller):
    def __init__(self, filename=""):
        self.track_filler = TrackFiller(filename)
        self.event_metadata = EventMetadataGenerator()
        self.event_class = Event

    def next(self):
        # The stop iteration should propogate from here
        self.metadata = next(self.event_metadata)
        first_track_index = self.metadata["FIRST_TRACK_INDEX"]
        last_track_index = self.metadata["LAST_TRACK_INDEX"]
        n_tracks = last_track_index-first_track_index

        event = self.event_class(None, None)
        for i in range(n_tracks):
            event.tracks.append(next(self.track_filler))
        event.onComplete()
        return event


class RunFiller(BaseFiller):
    def __init__(self, filename, runC=None):
        self.event_filler = EventFiller(filename)
        self.run_class = Run
        self.is_ready = True
        self.runConfig = runC
    def next(self):
        if self.is_ready:
            run = self.run_class(self.runConfig, None)
            for event in self.event_filler:
                run.events.append(event)
            run.onComplete()
            self.is_ready = False
            return run
        else:
            raise StopIteration()
