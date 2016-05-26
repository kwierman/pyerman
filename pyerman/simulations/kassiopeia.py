import threading
import subprocess
import Queue
import traceback
import signal
import os, sys

def default_config():
    return {
        'runid':0,
        'events':10,
        'seed':0,
        'generator': 'egun_gauss_cosine',
        'max_steps':'100000000',
        'max_turns':'100',
        'egun_line_width':0.20,
        'egun_line_mean': 0.20,
        'egun_angle_spread':17.0,
        'egun_backplate_voltage': -18610,
        'egun_acceleration_voltage':5000,
        'egun_dipole_voltage':3000,
        'ground_potential':0,
        'hull_potential': -18400.0,
        'ie_common_potential': -200.0,
        'ap_offset_potential':0.0,
    }


class Thread(threading.Thread):
    """
        Kassiopeia Run Threading. Given the number of configuration that need
        to be run simultaniously and the amount of resources kasper utilizes,
        a threaded approach can be used to
    """

    __ThreadExitFlag__=1
    queue = Queue.Queue(10000)
    queueLock = threading.Lock()
    activeThreads=[]

    def __init__(self, base_file="$KASPERSYS/config/Kassiopeia/EGun/NonAxialEGunSimulation.xml"):
        super(Thread, self).__init__()
        self.base_file = base_file

    def run(self):
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

    def startSimulation(self, config):
        base = ["Kassiopeia",self.base_file,'-r']
        for key,value in config.iteritems():
            base.append("{}={}".format(key, value))
        subprocess.call(base)


    @staticmethod
    def killRunThreads(signum, frame):
        """
            Sets the thread kill flag to each of the ongoing analysis threads
        """
        Thread.__ThreadExitFlag__ =  0

    @staticmethod
    def startThreads(nThreads, simulation_file):
        for i in range(nThreads):
            thread = Thread(simulation_file)
            thread.start()
            Thread.activeThreads.append(thread)

    @staticmethod
    def waitTillComplete(callback=None):
        if callback is None:
            while not Thread.queue.empty():
                sys.stdout.flush()
        else:
            while not Thread.queue.empty():
                callback()

        # Notify threads it's time to exit
        Thread.__ThreadExitFlag__ = 0

        # Wait for all threads to complete
        for t in Thread.activeThreads:
            t.join()
        # dealloc
        Thread.activeThreads=[]

signal.signal(signal.SIGINT, Thread.killRunThreads)

def go(simulation_file="Go.xml",configs=[], nthreads=4):

    threads = Thread.startThreads(nthreads, simulation_file)

    Thread.queueLock.acquire()
    for config in configs:
        Thread.queue.put(config)
    Thread.queueLock.release()

    Thread.waitTillComplete()
