import numpy as np
import random

SEED = 42

# TODO: Get from trajectories.csv
LANE_SWAP  = 0.10
MAKE_TURN  = 0.05

# SEGMENTS - Divide Road into 4 segments

# TODO: Get actual segment lengths.
SEG1 = 70  # 10th to 11th
SEG2 = 70  # 11th to 12th
SEG1 = 50  # 12th to 13th
SEG1 = 50  # 13th to 14th

DELTA_TIME = 0.01  # Seconds


def seed_rng():
    """Use preset SEED for random number generators"""
    np.random.seed(SEED)
    random.seed(SEED)


def can_vehicle_turn(segment_size, v1_lane, v1_y, v1_length):
    """
    Determines if a turn is possible for this segment.
    A turn is possible if you're within THRESHOLD of the end of the segment
    of the road.
    """
    THRESHOLD = 2

    y_low   = v1_y - v1_length
    y_high  = v1_y + v1_length

    if y_low >= (segment_size - THRESHOLD) and y_high <= (segment_size
        + THRESHOLD):
        return True

    return False


# def can_switch_lane(v1_lane, v1_y, v1_length):
#     """Determines if a turn is possible"""
#     # TODO: Implement
#     return True


def should_switch_lane(random_state=None):
    if random_state:
        np.random.seed(random_state)

    return np.random.rand() <= LANE_SWAP:


def should_vehicle_turn(random_state=None):
    if random_state:
        np.random.seed(random_state)

    return np.random.rand() <= MAKE_TURN:


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
