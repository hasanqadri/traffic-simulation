
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
    def __init__(self, n_moving):
        self.car_queue           = deque()
        self.car_queue_lock      = Lock()

        self.moving              = n_moving
        self.lane_lock           = Lock()

        self.segment             = None
        self.started             = False


    def connect_segment(self, segment):
        self.segment = segment


    def start(self):
        # TODO: Implement
        self.start = True


    def handle_car(self, travel_time, metadata):
        """
        Simulate driving the car through Road Segment.
        Calls remove_car() upon completion.
        """
        time.sleep(travel_time)
        self.remove_car()


    def begin_handling_car(self, travel_time):
        print("Dispatching sleep for {}s".format(travel_time))
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
        metadata[enter(self.name)] = time.now()

        self.lane_lock.acquire()

        handled = False  # Indicates if car has been handled.
        if self.lanes > 0:
            self.lanes -= 1
            self.begin_handling_car(travel_time, metadata)
            handled = True

        self.lane_lock.release()

        if handled:
            return

        # Otherwise, add to the car queue
        self.car_queue_lock.acquire()
        self.car_queue.append(travel_time)
        self.car_queue_lock.release()


    def remove_car(self):

        # Track the time this vehicle left this RoadSegment.
        metadata[leave(self.name)] = time.now()

        if should_vehicle_turn():
            # Track the time this vehicle turned out of this RoadSegment.
            metadata[turn(self.name)] = time.now()
            pass
        else:
            # If we have a next segment, send this car there.
            if self.segment:
                self.segment.add_car(travel_time, metadata)


        # If we have car in the queue, just dispatch a new
        # car from the queue immediately.
        handled = False
        self.car_queue_lock.acquire()
        if self.car_queue:
            travel_time = self.car_queue.popleft()  # Pop from Queue
            self.begin_handling_car(travel_time)
            handled = True
        self.car_queue_lock.release()

        if not handled:
            self.lane_lock.acquire()
            self.lanes += 1
            self.lane_lock.release()
