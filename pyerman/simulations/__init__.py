from .file_generator import base_file_name_generator, TFFilenameGenerator, file_name_filter
from .filler import StepFiller, TrackFiller, EventFiller, RunFiller
from .generators import StepGenerator, TrackGenerator
from .objects import Step, Track, Event, Run, Composite

def composite_generator(**kwargs):
    """
        
    """
    runConfigs = kwargs['runConfig']

    composite =kwargs['compClass']()

    for runC in runConfigs:
        voltage = runC['voltage']
        filename = runC['file']

        step_fill = None
        if 'stepsFill' in kwargs:
            step_fill = kwargs['stepFill'](filename)
        else:
            step_fill = StepFiller(filename)
        if 'stepClass' in kwargs:
            step_fill.step_class = kwargs['stepClass']


        track_fill = TrackFiller(filename)
        if 'trackFill' in kwargs:
            track_fill = kwargs['trackFill'](filename)
        track_fill.step_filler=step_fill
        if 'trackClass' in kwargs:
            track_fill.track_class = kwargs['trackClass']
        else:
            track_fill.track_class = Track


        event_fill = EventFiller(filename)
        if 'eventFill' in kwargs:
            event_fill = kwargs['eventFill'](filename)
        event_fill.track_filler=track_fill
        if 'eventClass' in kwargs:
            event_fill.event_class = kwargs['eventClass']
        else:
            event_fill.event_class = Event

        run_fill = RunFiller(filename)
        if 'runFill' in kwargs:
            run_fill = kwargs['runFill'](filename)
        run_fill.event_filler=event_fill

        run_fill.run_class = Run
        if 'runClass' in kwargs:
            run_fill.run_class = kwargs['runClass']
        try:
            for run in run_fill:
                composite.runs.append(run)
        except IOError:
            print "Tree not found in: ", voltage
    return composite
