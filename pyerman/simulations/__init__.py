from .file_generator import base_file_name_generator, TFFilenameGenerator, file_name_filter
from .filler import StepFiller, TrackFiller, EventFiller, RunFiller
from .generators import StepGenerator, TrackGenerator
from .objects import Step, Track, Event, Run, Composite

import Queue
import threading

import traceback

import signal, os
import sys

__runThreadExitFlag__ = 1

def killRunThreads(signum, frame):
    """
        Sets the thread kill flag to each of the ongoing analysis threads
    """
    global __runThreadExitFlag__
    __runThreadExitFlag__= 0
signal.signal(signal.SIGINT, killRunThreads)

class RunThread(threading.Thread):
    """
        Threading Object for Run-level analysis
    """
    def __init__(self, analysis, queue, queuelock, compositeLock, composite):
        super(RunThread, self).__init__()
        self.analysis = analysis
        self.queue = queue
        self.queuelock = queuelock
        self.compositeLock = compositeLock
        self.composite = composite

    def run(self):
        """
            Wrapper for data processing function
        """
        global __runThreadExitFlag__
        while __runThreadExitFlag__:
            self.queuelock.acquire()
            if not self.queue.empty():
                runConfig = self.queue.get()
                self.queuelock.release()
                try:
                    self.process_data(runConfig)
                except Exception:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    print repr(traceback.format_exception(exc_type, exc_value,
                                          exc_traceback))
            else:
                self.queuelock.release()

    def process_data(self, runConfig):
        """
            Runs analysis on runConfig in question
        """
        filename = runConfig['file']

        step_fill = None
        if 'stepFill' in self.analysis:
            if self.analysis['stepFill'] is not None:
                step_fill = self.analysis['stepFill'](filename)
        else:
            step_fill = StepFiller(filename)
        if 'stepClass' in self.analysis:
            step_fill.setStepClass(self.analysis['stepClass'])

        track_fill = TrackFiller(filename)
        if 'trackFill' in self.analysis:
            track_fill = self.analysis['trackFill'](filename)
        track_fill.step_filler=step_fill
        if 'trackClass' in self.analysis:
            track_fill.setTrackClass(self.analysis['trackClass'])
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

        run_fill = RunFiller(filename, runConfig)
        if 'runFill' in self.analysis:
            run_fill = self.analysis['runFill'](filename)
        run_fill.event_filler=event_fill

        run_fill.run_class = Run
        if 'runClass' in self.analysis:
            run_fill.run_class = self.analysis['runClass']
        for run in run_fill:
            self.compositeLock.acquire()
            self.composite.runs.append(run)
            self.composite.onAddRun(run)
            self.compositeLock.release()

def composite_generator(runConfigs, analysis, nthreads=4):
    global __runThreadExitFlag__

    __runThreadExitFlag__ = 1

    composite = Composite
    if 'compClass' in analysis:
        composite = analysis['compClass']()
    composite.onCreate()

    # The threading part of all this
    queueLock = threading.Lock()
    workQueue = Queue.Queue(100)
    compositeLock = threading.Lock()

    threads = []
    print "Creating Threads"
    for i in range(nthreads):
        thread = RunThread( analysis,workQueue,queueLock,compositeLock,composite )
        thread.start()
        threads.append(thread)

    print "Filling Queue"
    queueLock.acquire()
    for runC in runConfigs:
        workQueue.put(runC)
    queueLock.release()
    # Wait for queue to empty
    print "Waiting For analysis to finish"
    while not workQueue.empty():
        sys.stdout.flush()

    # Notify threads it's time to exit
    __runThreadExitFlag__ = 0

    # Wait for all threads to complete
    for t in threads:
        t.join()

    composite.onComplete()
    return composite
