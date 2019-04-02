import numpy as np
import random
from threading import Lock

SEED = 42

# TODO: Get from trajectories.csv
MAKE_TURN  = 0.05

record_lock = Lock()
records = []


def seed_rng():
    """Use preset SEED for random number generators"""
    np.random.seed(SEED)
    random.seed(SEED)


def should_vehicle_turn(random_state=None):
    if random_state:
        np.random.seed(random_state)

    return np.random.rand() <= MAKE_TURN


class Records():
    """
    Keep a record of the metadata of each car.
    """
    def __init__(self):
        self.records = []
        self.lock = Lock()

    def add(self, metadata):
        with self.lock:
            self.records.append(metadata)

    def get(self):
        return self.records

    def __str__(self):
        return str(self.records)
