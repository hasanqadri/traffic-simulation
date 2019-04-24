import time

import numpy as np

from helpers import *
from empirical import *
from util import *
from threaded import *

# TODO: Remove
import scipy.stats as stats


START_TIME = 1163030800
MINTIME = 1000      # Ensure we run for at least this long
MAXTIME = 10000000  # No vehicles added after this point.

sim_state = SimulationState()
sim_time  = 0
fel       = FutureEventList()

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
    N_keep = NUM_EVENTS // 1000  # Reduces number of arrival times significantly without shifting distribution much
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
    init_interarrival_times()
    init_signals()


    # Now, add a single VehicleProcess based on the timings.
    arrival_time = get_random_interarrival_time()
    VehicleProcess(fel, arrival_time)  # Adds self to FEL.

    logger.debug("FEL size after initialization: {}".format(fel.size()))
    logger.debug(fel.data)


def main():
    global sim_time

    count = 0
    added = 1
    while sim_time < MINTIME or fel.has_vehicles():

        new_time, proc = fel.pop()
        sim_time = new_time
        proc.handle(fel, sim_time, sim_state)

        if count % 100000 == 0:
            logger.info({"Iteration count": count, "Elements in FEL": len(fel.data)})

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


    def compute_mavg(travel_times):
        mavg = []
        N = len(travel_times)
        for i in range(1, N):
            mavg.append(np.mean(travel_times[:i]))

        return mavg

    completed_procs = fel.completed
    arrival_times = np.array(list((map(lambda x: x[0], completed_procs))))
    exit_times    = np.array(list((map(lambda x: x[1],  completed_procs))))
    travel_times = exit_times - arrival_times

    mavg = compute_mavg(travel_times)
    xs = range(len(mavg))


    logger.info("Number of cars that traveled 10th to 14th all \
        the way: {}".format(len(arrival_times)))

    logger.info("Mean  travel time: {:.3f}s".format(np.mean(travel_times)))
    logger.info("Stdev travel time: {:.3f}s".format(np.std(travel_times)))


    # Confidence intervals
    n = len(travel_times) - 1
    conf_low, conf_high = stats.t.interval(0.95, n, loc=np.mean(travel_times), scale=stats.sem(travel_times))

    logger.info("95% confidence interval of mean travel time: [{:.3f}, {:.3f}]".format(conf_low, conf_high))
