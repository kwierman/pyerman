import threading
import subprocess
import Queue
import traceback
import signal
import sys


def default_config():
    return {
        "base_command":{}
    }


class Thread(threading.Thread):
    """
        Kassiopeia Run Threading. Given the number of configurations that need
        to be run simultaniously and the amount of resources kasper utilizes,
        a threaded approach can be used to
    """

    __ThreadExitFlag__ = 1
    queue = Queue.Queue(100000)
    queueLock = threading.Lock()
    activeThreads = []
    threadLock = threading.Lock()

    def __init__(self):
        """
            :param: base_file string pointing to location of base simulation
            :type: base_file string
        """
        super(Thread, self).__init__()

    def run(self):
        """
            Loops over queue to accept new configurations
        """
        while Thread.__ThreadExitFlag__:
            self.queueLock.acquire()
            if not self.queue.empty():
                config = Thread.queue.get()
                self.queueLock.release()
                try:
                    self.startSimulation(config)
                except Exception:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    print repr(traceback.format_exception(exc_type, exc_value,
                                                          exc_traceback))
            else:
                self.queueLock.release()

    def simulation_action(self, config):
        return []

    def startSimulation(self, config):
        base_command = [config['base_command']]+self.simulation_action(config)
        subprocess.call(base_command)

    @staticmethod
    def killRunThreads(signum, frame):
        """
            Sets the thread kill flag to each of the ongoing analysis threads
        """
        Thread.__ThreadExitFlag__ = 0
        sys.exit(signum)

    @staticmethod
    def startThreads(nThreads):
        for i in range(nThreads):
            thread = Thread()
            thread.start()
            Thread.activeThreads.append(thread)

    @staticmethod
    def waitTillComplete(callback=None):
        if callback is None:
            while not Thread.queue.empty() and Thread.__ThreadExitFlag__:
                sys.stdout.flush()
        else:
            while not Thread.queue.empty() and Thread.__ThreadExitFlag__:
                callback()

        # Notify threads it's time to exit
        Thread.__ThreadExitFlag__ = 0

        # Wait for all threads to complete
        for t in Thread.activeThreads:
            t.join()
        # dealloc
        Thread.activeThreads = []

signal.signal(signal.SIGINT, Thread.killRunThreads)


def go(configs=[], nthreads=4):

    Thread.threadLock.acquire()

    threads = Thread.startThreads(nthreads)
    Thread.queueLock.acquire()
    for config in configs:
        Thread.queue.put(config)
    Thread.queueLock.release()
    Thread.waitTillComplete()

    Thread.threadLock.release()
    del threads
