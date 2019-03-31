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


def can_vehicle_turn(v1_lane, v1_y, v1_length):
    """Determines if a turn is possible"""
    # TODO: Implement
    return True

def can_switch_lane(v1_lane, v1_y, v1_length):
    """Determines if a turn is possible"""
    # TODO: Implement
    return True


def switch_lane(random_state=None):
    if random_state:
        np.random.seed(random_state)

    return np.random.rand() <= LANE_SWAP:


def vehicle_turn(random_state=None):
    if random_state:
        np.random.seed(random_state)

    return np.random.rand() <= MAKE_TURN:


def can_place(vehicle_positions, v1_lane, v1_y, v1_length):
    """
    :vehicle_positions:  - list of (lane, y, length) of where all other vehicles are
        at this time step.

    RETURN:
        True if this vehicle positioning won't cause colliding positions.
    """
    for (v2_lane, v2_y, v2_length) in vehicle_positions:
        if will_collide(v1_lane, v1_y, v1_length,
                        v2_lane, v2_y, v2_length):
            return False

    return True



def will_collide(v1_lane, v1_y, v1_length, v2_lane, v2_y, v2_length):
    """
    Determine if two vehicles will collide based on their respective centers
    and their respective vehicle lengths.
    """
    if v1_lane != v2_lane:
        return False

    v1low = v1_y   - v1_length
    v1high = v1_y  + v1_length

    v2low = v2_y   - v2_length
    v2high = v2_y  + v2_length

    if v1low >= v2low and v1low <= v2high:
        return True

    if v1high >= v2low and v1high <= v2high:
        return True

    return False

