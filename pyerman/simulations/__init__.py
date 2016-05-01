from .file_generator import base_file_name_generator, TFFilenameGenerator, file_name_filter
from .filler import StepFiller, TrackFiller, EventFiller, RunFiller
from .generators import StepGenerator, TrackGenerator
from .objects import Step, Track, Event, Run, Composite

import Queue
import threading


__runThreadExitFlag__ = 1

class RunThread(threading.Thread):
    def __init__(self, analysis, queue, queuelock, compositeLock):
        super(RunThread, self).__init__()
        self.analysis = analysis
        self.queue = queue
        self.queuelock = queuelock
        self.compositeLock = compositeLock
    def run(self):
        global __runThreadExitFlag__
        while __runThreadExitFlag__:
            self.queuelock.acquire()
            if not self.queue.empty():
                runConfig = self.queue.get()
                self.queuelock.release()
                self.process_data(runConfig)

            else:
                self.queuelock.release()
    def process_data(self, runConfig):
        filename = runConfig['file']

        step_fill = None
        if 'stepFill' in self.analysis:
            if self.analysis['stepFill'] is not None:
                step_fill = self.analysis['stepFill'](filename)
        else:
            step_fill = StepFiller(filename)
        if 'stepClass' in self.analysis:
            step_fill.step_class = self.analysis['stepClass']

        track_fill = TrackFiller(filename)
        if 'trackFill' in self.analysis:
            track_fill = self.analysis['trackFill'](filename)
        track_fill.step_filler=step_fill
        if 'trackClass' in self.analysis:
            track_fill.track_class = self.analysis['trackClass']
        else:
            track_fill.track_class = Track

        event_fill = EventFiller(filename)
        if 'eventFill' in self.analysis:
            event_fill = self.analysis['eventFill'](filename)
        event_fill.track_filler=track_fill
        if 'eventClass' in self.analysis:
            event_fill.event_class = self.analysis['eventClass']
        else:
            event_fill.event_class = Event

        run_fill = RunFiller(filename, self.runConfig)
        if 'runFill' in self.analysis:
            run_fill = self.analysis['runFill'](filename)
        run_fill.event_filler=event_fill

        run_fill.run_class = Run
        if 'runClass' in self.analysis:
            run_fill.run_class = self.analysis['runClass']
        for run in run_fill:
            self.compositeLock.acquire()
            composite.runs.append(run)
            composite.onAddRun(run)
            self.compositeLock.release()

def composite_generator(runConfigs, analysis):
    """

    """
    global __runThreadExitFlag__

    composite = analysis['Compclass']()
    composite.onCreate()

    # The threading part of all this
    queueLock = threading.Lock()
    workQueue = Queue.Queue(100)
    compositeLock = threading.Lock()

    threads = []
    threadID=1
    print "Creating Threads"
    for i in range(4):
        thread = RunThread( analysis,workQueue,  queueLock,compositeLock, )
        thread.start()
        threads.append(thread)
        threadID += 1
    print "Filling Queue"

    queueLock.acquire()
    for runC in runConfigs:
        workQueue.put(runC)
    queueLock.release()
    # Wait for queue to empty
    while not workQueue.empty():
        pass

    # Notify threads it's time to exit
    exitFlag = 1

    # Wait for all threads to complete
    for t in threads:
        t.join()

    composite.onComplete()
    return composite
