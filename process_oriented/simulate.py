import numpy as np

from helpers import *
from empirical import *
from util import *
from threaded import *


START_TIME = 1163030800

sim_state = SimulationState()
sim_time  = 0
fel       = FutureEventList()
events    = {}
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
    N_keep = len(interarrival_times)
    i = np.random.randint(0, N_keep)
    if (interarrival_times[i] < sim_time):
        return abs(interarrival_times[i] - sim_time) + interarrival_times[i] + 5000
    return interarrival_times[i]


def init_interarrival_times():
    global interarrival_times
    interarrival_times = [0]

    # Dividing by 10k limits range of interarrival times but GREATLY speeds
    # up the simulation
    N_keep = numEvents // 10000
    for _ in range(N_keep):
        interarrival_times.append(events[str(z)]['Epoch_ms'] - START_TIME)


def init_signals():
    global numEvents
    numEvents = len(EVENTS)

    for (signame, green_time, red_time) in signal_timings:
        signal = Signal(signame, green_time, red_time)

        sim_state.add_signal(signame, signal)
        # logger.debug(signal)

        # Creates a process. Assume it starts green, so switch when turns red.
        new_time = sim_time + red_time
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

    MINTIME = 1000    # Ensure we run for at least this long
    MAXTIME = 1000000  # No vehicles added after this point.

    count = 0
    added = 1
    while sim_time < MINTIME or fel.has_vehicles():

        new_time, proc = fel.pop()
        sim_time = new_time
        proc.handle(fel, sim_time, sim_state)

        # Simulates adding new car to our sim only if MAXTIME not exceeded.
        if sim_time < MAXTIME and (np.random.random() < 0.05):  # With 5% chance
            logger.info("Adding new vehicle")
            added += 1
            arrival_time = get_random_interarrival_time()
            VehicleProcess(fel, arrival_time)  # Adds self to FEL.

        count += 1  # Loop counter.


    logger.info("Completed: {}".format(len(fel.completed)))
    logger.info("Loop Count: {}".format(count))
    logger.info("Vehicles Simulated: {}".format(added))

    filename = "completed_procs_results.pkl"
    savepkl(fel.completed, filename)
    logger.info("Saving completed vehicle processes to {}".format(filename))


if __name__ == "__main__":
    seed_rng()
    initialize()
    main()
