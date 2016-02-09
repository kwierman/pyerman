from pyerman.root import BaseGenerator
from .generators import StepGenerator, TrackGenerator
from .objects import Step, Track, Event, Run

class StepFiller(BaseGenerator):
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

class TrackFiller(BaseGenerator):
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


class EventFiller(BaseGenerator):
    def __init__(self, filename=""):
        self.track_filler = TrackFiller(filename)
        self.event_class = Event
        self.stored_track = None
        self.empty = False

    def next(self):
        if self.empty:
            raise StopIteration()
        event = self.event_class(None, None)
        if self.stored_track is None:
            self.stored_track = next(self.track_filler)
        event.tracks.append(self.stored_track)
        try:
            self.stored_track = next(self.track_filler)
        except StopIteration:
            self.stored_track = None
            event.onComplete()
            self.empty=True
            return event
        while not self.stored_track.isFirst:
            event.tracks.append(self.stored_track)
            try:
                self.stored_track = next(self.track_filler)
            except StopIteration:
                self.stored_track = None
                event.onComplete()
                self.empty=True
                return event
        event.onComplete()
        return event


class RunFiller(BaseGenerator):
    def __init__(self, filename=""):
        self.event_filler = EventFiller(filename)
        self.run_class = Run
        self.is_ready = True
    def next(self):
        if self.is_ready:
            run = self.run_class(None, None)
            for event in self.event_filler:
                run.events.append(event)
            run.onComplete()
            self.is_ready = False
            return run
        else:
            raise StopIteration()
