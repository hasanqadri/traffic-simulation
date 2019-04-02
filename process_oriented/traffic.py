
from collections import deque
import time

import threading
from threading import Lock

from util import *


########################## Metadata Functions ##########################

def enter(segment_name):
    return "enter_{}".format(segment_name)

def leave(segment_name):
    return "leave_{}".format(segment_name)

def turn(segment_name):
    return "turn_{}".format(segment_name)

########################################################################

class RoadSegment():
    """
    Segment of a road, behaves like a Resource from Simpy.
    Parameterized by n_moving, the number of cars that may
    be processed in a single time step.
    """
    def __init__(self, name, records, n_moving):
        self.name                = name
        self.records             = records
        self.moving              = n_moving
        self.moving_lock         = Lock()
        self.car_queue           = deque()
        self.car_queue_lock      = Lock()

        self.segment             = None
        self.started             = False


    def connect_segment(self, segment):
        self.segment = segment


    def _initialize(self, travel_times):
        with self.car_queue_lock:
            for travel_time in travel_times:
                metadata = dict()  # Initialize with new dicts.
                self.car_queue.append(travel_time, metadata)

    def start(self):
        # TODO: Implement
        self.start = True
        # Create an internal function and run it via a thread.


    def handle_car(self, travel_time, metadata):
        """
        Simulate driving the car through Road Segment.
        Calls remove_car() upon completion.
        """
        time.sleep(travel_time)
        self.remove_car(travel_time, metadata)


    def begin_handling_car(self, travel_time, metadata):
        print("SEGMENT {} is handling a new car".format(self.name))
        t = threading.Thread(
            target=self.handle_car,
            args=(travel_time, metadata),
        )

        t.start()


    def add_car(self, travel_time=1, metadata={}):
        """
        :travel_time: - how long this vehicle takes to be processed.
            Related to velocity.
        :metadata: - a dict containing information about this vehicle's
            journey through road segments
        """

        # Track the time this vehicle was added to this RoadSegment.
        metadata[enter(self.name)] = time.time()

        self.moving_lock.acquire()

        handled = False  # Indicates if car has been handled.
        if self.moving > 0:
            self.moving -= 1
            self.begin_handling_car(travel_time, metadata)
            handled = True

        self.moving_lock.release()

        if handled:
            return

        # Otherwise, add to the car queue
        self.car_queue_lock.acquire()
        self.car_queue.append(travel_time)
        self.car_queue_lock.release()


    def remove_car(self, travel_time, metadata):

        # Track the time this vehicle left this RoadSegment.
        metadata[leave(self.name)] = time.time()

        if should_vehicle_turn():
            print("VEHICLE HAS TURNED")
            # Track the time this vehicle turned out of this RoadSegment.
            metadata[turn(self.name)] = time.time()
            self.records.add(metadata)
        else:
            # If we have a next segment, send this car there.
            if self.segment:
                self.segment.add_car(travel_time, metadata)
            else:
                print("VEHICLE HAS EXITED")
                self.records.add(metadata)


        # If we have car in the queue, just dispatch a new
        # car from the queue immediately.
        handled = False
        self.car_queue_lock.acquire()
        if self.car_queue:
            travel_time = self.car_queue.popleft()  # Pop from Queue
            self.begin_handling_car(travel_time, metadata)
            handled = True
        self.car_queue_lock.release()

        if not handled:
            self.moving_lock.acquire()
            self.moving += 1
            self.moving_lock.release()
