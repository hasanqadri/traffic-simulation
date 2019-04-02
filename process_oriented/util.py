import numpy as np
import random

SEED = 42

# TODO: Get from trajectories.csv
LANE_SWAP  = 0.10
MAKE_TURN  = 0.05


def seed_rng():
    """Use preset SEED for random number generators"""
    np.random.seed(SEED)
    random.seed(SEED)


def should_vehicle_turn(random_state=None):
    if random_state:
        np.random.seed(random_state)

    return np.random.rand() <= MAKE_TURN:
