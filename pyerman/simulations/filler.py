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

    def parent():
            doc = "The parent property."

            def fget(self):
                return self._parent

            def fset(self, value):
                self._parent = value

            def fdel(self):
                del self._parent
            return locals()
    parent = property(**parent())


class StepFiller(BaseFiller):
    def __init__(self, filename=""):
        self.step_gen = StepGenerator(filename)
        self.step_class = Step

    def setStepClass(self, cls):
        self.step_class = cls
        self.step_gen.prepareForStreaming(cls)

    def next(self):
        """
        raises: StopIteration if it hits the end of the steps in the file
        """
        dat, tree = next(self.step_gen)
        step = self.step_class(dat, tree)
        step.parent = self.parent
        step.onComplete()
        return step


class TrackFiller(BaseFiller):
    def __init__(self, filename=""):

        self.track_gen = TrackGenerator(filename)
        self.step_filler = StepFiller(filename)
        self.track_class = Track

    def setTrackClass(self, cls):
        self.track_class = cls
        self.track_gen.prepareForStreaming(cls)

    def next(self):
        dat, tree = next(self.track_gen)
        track = self.track_class(dat, tree)
        track.parent = self.parent
        if self.step_filler is not None:
            while not track.isFull():

                # WHATEVER YOU DO, DO NOT PUT EXCEPTION HANDLING HERE< IT WILL
                # BREAK RECONSTRUCTION AT THE GENERATOR LEVEL
                # IN PYTHON <3
                self.step_filler.parent = track
                track.steps.append(next(self.step_filler))
        track.onComplete()
        return track


class EventFiller(BaseFiller):
    def __init__(self, filename=""):
        self.track_filler = TrackFiller(filename)
        self.event_metadata = EventMetadataGenerator(filename)
        self.event_class = Event

    def next(self):
        # The stop iteration should propogate from here
        self.metadata, _ = next(self.event_metadata)
        first_track_index = self.metadata["FIRST_TRACK_INDEX"].GetValue()
        last_track_index = self.metadata["LAST_TRACK_INDEX"].GetValue()
        # N Tracks must be offset by one
        n_tracks = int(last_track_index)-int(first_track_index)+1
        # Sometimes if the first step gets killed by navigation, an event with
        # no tracks is created. This is ignored here.
        if n_tracks == 0:
            return self.next()
        event = self.event_class(None, None)
        event.parent = self.parent

        for i in range(n_tracks):
            self.track_filler.parent = event
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
            run.parent = self.parent
            self.event_filler.parent = run
            for event in self.event_filler:
                run.events.append(event)
            run.onComplete()
            self.is_ready = False
            return run
        else:
            raise StopIteration()
