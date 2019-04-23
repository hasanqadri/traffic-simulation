import pickle
import gzip
import random
from pprint import pprint

import logging
# from logging import debug, info, warning

import numpy as np

from helpers import *
from empirical import *

############################# LOGGING #################################

import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)-5.5s]  %(message)s",
    handlers=[
        logging.FileHandler("run.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()


############################# ROAD SEGMENTS ###########################
# Road Segment names
SEG0 = " 9th to 10th"
SEG1 = "10th to 11th"
SEG2 = "11th to 12th"
SEG3 = "12th to 13th"
SEG4 = "13th to 14th"
EXIT = "Exit"


def get_next_segment(seg):
    if seg == SEG0:
        return SEG1
    elif seg == SEG1:
        return SEG2
    elif seg == SEG2:
        return SEG3
    elif seg == SEG3:
        return SEG4
    elif seg == SEG4:
        return EXIT

############################# TURNING #############################
P_TURNLEFT, P_TURNRIGHT = get_prob_turning()

P_INTERSECTIONS = {
    SEG0: (P_TURNLEFT, P_TURNRIGHT),  # Left or Right turns
    SEG1: (0, P_TURNRIGHT),  # Only Right turn
    SEG2: (0, P_TURNRIGHT),  # Only Right turn
    SEG3: (0, 0),  # No turns here, only forward
    SEG4: (P_TURNLEFT, P_TURNRIGHT),  # Left or Right turns
}

GO_LEFT     = "LEFT"
GO_RIGHT    = "RIGHT"
GO_FORWARD  = "FORWARD"


def which_way(segment):
    """
    Determine which way a car will go at a particular intersection.
    """
    if segment not in P_INTERSECTIONS.keys():
        raise ValueError("That's not a valid segment: {}".format(segment))

    pleft, pright = P_INTERSECTIONS[segment]
    p = np.random.random()

    if p < pleft:
        return GO_LEFT

    p = np.random.random()
    if p < pright:
        return GO_RIGHT

    return GO_FORWARD


############################# Transitions #############################
ARRIVE = "ARRIVE"
DEPART = "DEPART"

def flip(transition):
    if transition == ARRIVE:
        return DEPART
    else:
        return ARRIVE

# Time to traverse down segment
TRAVEL_TIMES = {
    SEG1: 12,
    SEG2:  8,
    SEG3:  8,
    SEG4: 12,
}

# Time to exit one segment and enter another via an intersection
# TRANSFER_DELAY = 2

#######################################################################

# def should_vehicle_turn(random_state=None):
#     if random_state:
#         np.random.seed(random_state)

#     return np.random.rand() <= MAKE_TURN


# def random_travel_time(low=0.025, high=0.5, size=5):
#     return np.random.uniform(low, high, size)

########################## Metadata Helpers ###########################

def enter(segment):
    return "enter_{}".format(segment)

def leave(segment):
    return "leave_{}".format(segment)

def turn(direction):
    return "turn_{}".format(direction)

#######################################################################
