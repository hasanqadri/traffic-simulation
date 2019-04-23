"""
This file holds all the Classes and Functions that will be used to support
threads in the simulation.
"""

from functools import total_ordering

from heapq import heappush, heappop
import numpy as np
import threading
from util import *


# Signal Names
SIG0 = "10th Signal"
SIG1 = "11th Signal"
SIG2 = "12th Signal"
# SIG3 = "14th Signal"
SIG4 = "14th Signal"

SIG0_LEFT = "10th Left Signal"
SIG4_LEFT = "14th Left Signal"

RED    = "RED  "
GREEN  = "GREEN"

class Signal(object):
    def __init__(self, name, green_time, red_time):
        self.name          = name

        # Track how long the given color stays.
        self.green_time    = green_time
        self.red_time      = red_time

        self.color         = GREEN  # Initialize to Green
        self.last_flipped  = 0

        self.lock          = threading.Lock()


    def flip(self, sim_time):
        with self.lock:
            color = self.color
            if color == RED:
                self.color = GREEN
            else:
                self.color = RED

            self.last_flipped = sim_time


    def next_flip_time(self, use_epsilon=True):
        """
        Estimates the time of the next signal flip. Use this to schedule
        when vehicles will move. The randomness serves as a tie-breaker.
        """
        if use_epsilon:  # Adds a random delay, 0 - 1 second.
            epsilon = np.random.random()
        else:
            epsilon = 0  # No delay.

        with self.lock:
            color = self.color
            flip_time = self.red_time
            if color == GREEN:
                flip_time = self.green_time

            estimate = self.last_flipped + self.green_time + epsilon

        return estimate


    def is_green(self):
        with self.lock:
            color = self.color

        return (color == GREEN)

    def __str__(self):
        rep = "{} is {}. Flips ({}, {})".format(self.name, self.color,
            self.green_time, self.red_time)

        return rep


class SimulationState(object):
    """
    This stores signal states.
    """
    def __init__(self):
        self.signals = {}


    def add_signal(self, signame, signal):
        self.signals[signame] = signal


    def get_signal_by_name(self, signame):
        if signame not in self.signals:
            raise ValueError("Unknown signame.")

        return self.signals[signame]


    def get_signal(self, direction, segment):
        signals = self.signals
        if direction == GO_LEFT:
            if segment == SEG0:
                return signals[SIG0_LEFT]
            elif segment == SEG4:
                return signals[SIG4_LEFT]
            else:
                print("DIR: {}    SEG: {}".format(direction, segment))
                raise ValueError("Direction not supported at this segment")

        if segment == SEG0:
            return signals[SIG0]
        elif segment == SEG1:
            return signals[SIG1]
        elif segment == SEG2:
            return signals[SIG2]
        elif segment == SEG3:
            return None  # No signal at 13th
        elif segment == SEG4:
            return signals[SIG4]

        raise ValueError("Segment not supported.")


class FutureEventList(object):
    """
    A thread-safe FEL implementation.

    Can also hold unsorted list of element
    """

    def __init__(self):
        self.data = []
        self.lock = threading.Lock()

        # Store terminated processes.
        self.completed       = []  # Completed processes.
        self.completed_lock  = threading.Lock()


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


    def add_completed(self, proc):
        """
        Add a terminated process here.
        """
        with self.completed_lock:
            self.completed.append(proc)


    def get_completed(self):
        return self.completed

@total_ordering
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


    def handle(self, fel, sim_time, sim_state):
        """
        To be implemented by every Process type differently.
        """
        raise NotImplementedError("Function not implemented")


    def __str__(self):
        out  = ""
        out += "Process: {}\n".format(self.name)
        out += "Data: {}".format(self.metadata)
        return out

    def __repr__(self):
        out  = ""
        out += "Process: {}\n".format(self.name)
        out += "Data: {}".format(self.metadata)
        return out

    # These functions handle tie-breakers. Tie-breakers handled by the
    # process id.
    def __eq__(self, other):
        if not isinstance(other, Process):
            return False

        return self.proc_id == other.proc_id and self.name == other.name

    def __ne__(self, other):
        if not isinstance(other, Process):
            return True

        return self.proc_id != other.proc_id or self.name != other.name

    def __lt__(self, other):
        if not isinstance(other, Process):
            return False

        return self.proc_id < other.proc_id


class VehicleProcess(Process):

    def __init__(self, fel, start_time):

        proc_type = "Vehicle Drive"
        proc_id   = np.random.randint(1, int(1e9))

        super(VehicleProcess, self).__init__(start_time, proc_type, proc_id,
                                                fel)

        self.metadata["INIT"]  = start_time

        # Mark as entering 10th street intersection.
        self.segment           = SEG0
        self.transition        = DEPART


    def _handle_depart(self, fel, sim_time, sim_state):
        """
        This is when we leave a road segment, AKA when we're at an intersetion.
        """
        segment     = self.segment
        transition  = self.transition

        # Mark that we left segment at this time.
        self.metadata[leave(segment)] = sim_time

        # Determine which way to go from here.
        direction = which_way(segment)

        # First, get the signal belonging to this intersection
        signal = sim_state.get_signal(direction, segment)
        # If the signal is green, there's a small transfer time to get out of segment.
        new_time = sim_time + 5

        # If the signal is not green, determine which time it will become
        # green, and add that to the transfer time.
        # EDGE Case: signal is None because SIG3 doesn't exist.
        if signal is not None and not signal.is_green():
            new_time += signal.next_flip_time()

        if direction in [GO_LEFT, GO_RIGHT]:
            # We are turning. Mark it in metadata.
            self.metadata[turn(direction)] = (new_time, segment)

            # Add this process to the completed pile.
            proc = self
            fel.add_completed(proc)
            return

        # We're going forward. Update where we'll go next.
        self.segment = get_next_segment(segment)

        # EDGE Case: If we're exiting 14th, mark the special key
        # and add it to the completed list.
        if self.segment == EXIT:
            self.metadata["END"] = new_time
            # Add this process to the completed pile.
            proc = self
            fel.add_completed(proc)
            return

        else:
            # Change from DEPART to ARRIVE and vice versa.
            self.transition = flip(transition)
            # Add self back onto FEL.
            self.waitUntil(fel, new_time)


    def _handle_arrive(self, fel, sim_time, sim_state):
        segment     = self.segment
        transition  = self.transition

        # Mark that we entered segment at this time.
        self.metadata[enter(segment)] = sim_time

        # Transition to departure now.
        self.transition = flip(transition)

        # 10 second delay to get through to intersection.
        new_time = sim_time + 10

        # Add self back onto FEL.
        self.waitUntil(fel, new_time)


    def handle(self, fel, sim_time, sim_state):
        if self.transition == DEPART:
            self._handle_depart(fel, sim_time, sim_state)
        else:
            self._handle_arrive(fel, sim_time, sim_state)


class SignalProcess(Process):

    def __init__(self, start_time, fel, sim_state, signame):
        proc_type = signame
        proc_id   = np.random.randint(1, int(1e9))

        super(SignalProcess, self).__init__(start_time, proc_type, proc_id,
                                                fel)

        self.signame = signame
        self.signal = sim_state.get_signal_by_name(self.signame)

    def handle(self, fel, sim_time, sim_state):
        """
        To be implemented by every Process type differently.
        """
        self.signal.flip(sim_time)
        new_time = self.signal.next_flip_time(use_epsilon=False)

        # Schedule the next flip of the signal.
        self.waitUntil(fel, new_time)

    def __str__(self):
        out = "Process: {}    Last Flipped: {:.1f}".format(self.name,
            self.signal.last_flipped)
        return out

    def __repr__(self):
        out = "Process: {}    Last Flipped: {:.1f}".format(self.name,
            self.signal.last_flipped)
        return out
