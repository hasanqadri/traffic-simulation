import time

import numpy as np

from helpers import *
from empirical import *
from util import *
from threaded import *


START_TIME = 1163030800

sim_state = SimulationState()
sim_time  = 0
fel       = FutureEventList()
numEvents = 0

interarrival_times = []

# Signal name, green time, red time
signal_timings = [
    (SIG0,      38.1,         49.3),  # 10th
    (SIG1,      44.7,         55.4),  # 11th
    (SIG2,      64.1,         35.7),  # 12th
    (SIG4,      37.8,         45.3),  # 14th

    (SIG0_LEFT, 10.6,  2.2),  # 10th street, left turn
    (SIG4_LEFT, 12.4,  3.6),  # 14th street, left turn
]


def get_random_interarrival_time():
    arrival_time = np.random.choice(interarrival_times)
    if (arrival_time < sim_time):
        return abs(arrival_time - sim_time) + arrival_time + 5000
    return arrival_time


def init_interarrival_times():
    global interarrival_times
    N_keep = numEvents // 1000  # Reduces number of arrival times significantly without shifting distribution much
    for z in range(N_keep):
        interarrival_times.append(EVENTS[str(z)]['Epoch_ms'] - START_TIME)

    logger.debug("We have {} arrival times to choose from.".format(len(interarrival_times)))

def init_signals():
    for (signame, green_time, red_time) in signal_timings:
        signal = Signal(signame, green_time, red_time)

        # Randomly initialize signal color
        signal.color = np.random.choice([RED, GREEN])

        sim_state.add_signal(signame, signal)
        # logger.debug(signal)

        # Determine time after which signal will flip, create a SignalProcess
        # based on that.
        new_time = signal.next_flip_time(use_epsilon=False)
        SignalProcess(new_time, fel, sim_state, signame)  # Adds self to FEL.


def initialize():
    global numEvents
    numEvents = len(EVENTS)
    init_interarrival_times()
    init_signals()

    # Now, add a single VehicleProcess based on the timings.
    arrival_time = get_random_interarrival_time()
    VehicleProcess(fel, arrival_time)  # Adds self to FEL.

    logger.debug("FEL size after initialization: {}".format(fel.size()))
    logger.debug(fel.data)



def main():
    global sim_time

    MINTIME = 1000      # Ensure we run for at least this long
    MAXTIME = 10000000  # No vehicles added after this point.

    count = 0
    added = 1
    while sim_time < MINTIME or fel.has_vehicles():

        new_time, proc = fel.pop()
        sim_time = new_time
        proc.handle(fel, sim_time, sim_state)

        if count % 100000 == 0:
            logger.info({"Loop count": count, "Elements in FEL": len(fel.data)})

        # Simulates adding new car to our sim only if MAXTIME not exceeded.
        if sim_time < MAXTIME and (np.random.random() < 0.05):  # With 5% chance
            logger.debug("Adding new vehicle")
            added += 1
            arrival_time = get_random_interarrival_time()
            VehicleProcess(fel, arrival_time)  # Adds self to FEL.

        count += 1  # Loop counter.

    logger.info("Loop Count: {}".format(count))
    logger.info("Vehicles Simulated: {}".format(added))
    logger.info("Vehicles that made it to 14th Street: {}".format(len(fel.completed)))

    filename = "vehicle_metadata.pkl"
    savepkl(fel.completed, filename)
    logger.info("Saving vehicle metadata to {}".format(filename))


if __name__ == "__main__":
    start = time.time()
    seed_rng()
    initialize()
    main()
    elapsed = time.time() - start
    logger.info("Time Elapsed: {:.2f}s".format(elapsed))
