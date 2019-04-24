import numpy as np
import random

from helpers import *
SEED = 42

# Will be used in other places
EVENTS     = compressed_readpkl(DATAPATH)
NUM_EVENTS = len(EVENTS)
print("Initialized data from ground truth.")

def seed_rng():
    """Use preset SEED for random number generators"""
    np.random.seed(SEED)
    random.seed(SEED)

########################## Empirical Probabilities #######################

def get_prob_turning():
    intersectionCounter = 0.0
    rightTurnCounter    = 0.0
    leftTurnCounter     = 0.0
    for z in range(len(EVENTS.keys())):
        if (EVENTS[str(z)]['Intersection'] != 0):
            intersectionCounter = intersectionCounter + 1
            if (EVENTS[str(z)]['Movement'] == 3):
                rightTurnCounter += 1
            if (EVENTS[str(z)]['Movement'] == 2):
                leftTurnCounter += 1

    p_left = leftTurnCounter / intersectionCounter
    p_right = rightTurnCounter / intersectionCounter

    return (p_left, p_right)
