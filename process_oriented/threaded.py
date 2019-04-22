"""
This file holds all the Classes and Functions that will be used to support
threads in the simulation.
"""

from heapq import heappush, heappop
import numpy as np
import threading


class FutureEventList(object):
    """
    A thread-safe FEL implementation.
    """

    def __init__(self):
        self.data = []
        self.lock = threading.Lock()


    def size(self):
        n_elements = None
        with self.lock:
            n_elements = len(self.data)

        return n_elements


    def empty(self):
        return self.size() == 0


    def push(self, element, priority):
        with self.lock:
            heappush(self.data, (priority, element))


    def pop(self):
        if self.empty():
            raise ValueError("No elements left in FEL")

        with self.lock:
            out = heappop(self.data)

        return out

    def peek(self):
        first = None
        with self.lock:
            if len(self.data):
                first = self.data[0]
        return first


class Process(object):
    """
    An interface of what different processes must be able to handle.
    """
    def __init__(self, start_time, proc_type, proc_id, fel):
        self.proc_id    = proc_id
        self.name       = "{}_{}".format(proc_type, proc_id)
        self.metadata   = {}

        # Schedule this process onto the FEL.
        self.waitUntil(fel, start_time)


    def waitUntil(self, fel, new_time):
        """
        Push this object itself onto the FEL.
        """
        element   = self
        priority  = new_time
        fel.push(element, priority)


    def handle(self, fel, sim_time):
        """
        To be implemented by every Process type differently.
        """
        raise NotImplementedError("Function not implemented")


    def __str__(self):
        out =   "="*80
        out +=  "Process: {}\n".format(self.name)
        out +=  "Data: {}".format(self.metadata)
        return out


def VehicleProcess(Process):
    def __init__(self, start_time, fel):
        proc_type = "Drive"
        proc_id   = np.random.randint((1, int(1e9)))

        super(VehicleProcess, self).__init__(start_time, proc_type,
                                                proc_id, fel)

        self.meta["INIT"]  = start_time
        self.meta['Calls'] = 0  # The number of times handle() is called.


    def handle(self, fel, sim_time):
        self.meta['Calls'] += 1

        # TODO: Do something smarter
        # For now, if we hit some time threshold, stop immediately.
        if sim_time > 100:
            return

        # Otherwise cause some delay and reschedule the process
        new_time = sim_time + 10
        self.waitUntil(new_time, fel)
