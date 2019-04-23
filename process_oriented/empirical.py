import numpy as np
import random

from helpers import *

SEED = 42

def seed_rng():
    """Use preset SEED for random number generators"""
    np.random.seed(SEED)
    random.seed(SEED)

########################## Empirical Probabilities #######################

def get_prob_turning():
    datapath = "../data/trajectory_events.pklz"
    events = compressed_readpkl(datapath)

    intersectionCounter = 0.0
    rightTurnCounter    = 0.0
    leftTurnCounter     = 0.0
    for z in range(len(events.keys())):
        if (events[str(z)]['Intersection'] != 0):
            intersectionCounter = intersectionCounter + 1
            if (events[str(z)]['Movement'] == 3):
                rightTurnCounter += 1
            if (events[str(z)]['Movement'] == 2):
                leftTurnCounter += 1

    p_left = leftTurnCounter / intersectionCounter
    p_right = rightTurnCounter / intersectionCounter

    return (p_left, p_right)
