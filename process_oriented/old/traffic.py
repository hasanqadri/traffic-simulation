
from collections import deque
import time

import threading
from threading import Lock

from util import *


class RoadSegment():
    """
    Segment of a road, behaves like a Resource from Simpy.
    Parameterized by n_moving, the number of cars that may
    be processed in a single time step.
    """
    def __init__(self, name, records, n_moving):
        self.name                = name
        self.records             = records
        self.n_moving            = n_moving  # Will stay constant
        self.moving              = n_moving  # Will change over time. Workers.
        self.moving_lock         = Lock()
        self.car_queue           = deque()
        self.car_queue_lock      = Lock()

        self.segment             = None
        self.started             = False

    def __str__(self):
        return self.name


    def empty(self):
        answer = False
        with self.car_queue_lock:
            with self.moving_lock:
                answer = (not self.car_queue) and (self.moving == self.n_moving)

        return answer


    def connect_segment(self, segment):
        self.segment = segment


    def _initialize(self, travel_times):
        with self.car_queue_lock:
            for travel_time in travel_times:
                metadata = dict()  # Initialize with new dicts.

                # Track the time this vehicle was added to this RoadSegment.
                metadata[enter(self.name)] = time.time()

                self.car_queue.append((travel_time, metadata))

    def start(self):
        # TODO: Implement
        # Create an internal function and run it via a thread.
        def begin():
            # print("BEGIN {}".format(self.name))
            with self.car_queue_lock:
                with self.moving_lock:
                    while self.moving > 0 and self.car_queue:
                        self.moving -= 1
                        # print("BEGIN MOVING: {}".format(self.moving))
                        (travel_time, metadata) = self.car_queue.popleft()  # Pop from Queue
                        self.begin_handling_car(travel_time, metadata)

        t = threading.Thread(target=begin)
        t.start()


    def handle_car(self, travel_time, metadata):
        """
        Simulate driving the car through Road Segment.
        Calls remove_car() upon completion.
        """
        time.sleep(travel_time)
        self.remove_car(travel_time, metadata)


    def begin_handling_car(self, travel_time, metadata):
        t = threading.Thread(
            target=self.handle_car,
            args=(travel_time, metadata),
        )

        t.start()


    def add_car(self, travel_time, metadata):
        """
        :travel_time: - how long this vehicle takes to be processed.
            Related to velocity.
        :metadata: - a dict containing information about this vehicle's
            journey through road segments
        """
        # print("Car added to SEGMENT '{}': travel time '{}' - {}".format(self.name, travel_time, id(metadata)))

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
        self.car_queue.append((travel_time, metadata))
        self.car_queue_lock.release()


    def remove_car(self, travel_time, metadata):

        # Track the time this vehicle left this RoadSegment.
        metadata[leave(self.name)] = time.time()

        if should_vehicle_turn():
            print("VEHICLE HAS TURNED FROM {}".format(self.name))
            # Track the time this vehicle turned out of this RoadSegment.
            metadata[turn(self.name)] = time.time()
            self.records.add(metadata)
        else:
            # If we have a next segment, send this car there.
            if self.segment:
                print("VEHICLE TRANSITION TO {}".format(self.segment.name))
                self.segment.add_car(travel_time, metadata)
            else:
                print("VEHICLE HAS EXITED FROM {}".format(self.name))
                self.records.add(metadata)

        # If we have car in the queue, just dispatch a new
        # car from the queue immediately.
        handled = False
        self.car_queue_lock.acquire()
        if self.car_queue:
            (travel_time, metadata) = self.car_queue.popleft()  # Pop from Queue
            self.begin_handling_car(travel_time, metadata)
            handled = True
        self.car_queue_lock.release()

        if not handled:
            self.moving_lock.acquire()
            self.moving += 1
            self.moving_lock.release()
