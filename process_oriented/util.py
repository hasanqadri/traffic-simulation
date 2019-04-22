import numpy as np
import random
from threading import Lock
from pprint import pprint

SEED = 42

# TODO: Get from trajectories.csv
MAKE_TURN  = 0.005

record_lock = Lock()
records = []

name_seg1 = "10th to 11th"
name_seg2 = "11th to 12th"
name_seg3 = "12th to 13th"
name_seg4 = "13th to 14th"

def seed_rng():
    """Use preset SEED for random number generators"""
    np.random.seed(SEED)
    random.seed(SEED)


def should_vehicle_turn(random_state=None):
    if random_state:
        np.random.seed(random_state)

    return np.random.rand() <= MAKE_TURN


def random_travel_time(low=0.025, high=0.5, size=5):
    return np.random.uniform(low, high, size)



########################## Metadata Helpers ##########################

def enter(segment_name):
    return "enter_{}".format(segment_name)

def leave(segment_name):
    return "leave_{}".format(segment_name)

def turn(segment_name):
    return "turn_{}".format(segment_name)


class Records():
    """
    Keep a record of the metadata of each car.
    """
    def __init__(self):
        self.records = []
        self.lock = Lock()

    def add(self, metadata):
        # key_start  = enter(name_seg1)
        # key_end    = leave(name_seg4)

        # if key_start in metadata and key_end in metadata:
        #     start = metadata[key_start]
        #     end = metadata[key_end]

        #     elapsed = "Elapsed: {:.2f}s".format(end - start)
        #     print(elapsed)

        with self.lock:
            self.records.append(metadata)

    def get(self):
        return self.records.copy()

    def __str__(self):
        return str(self.records)

########################################################################
