import numpy as np

from helpers import *
from empirical import *
from util import *
from threaded import *

# import logging
# logging.basicConfig(
#     level=logging.DEBUG,
#     format="%(asctime)s [%(levelname)-5.5s]  %(message)s",
#     handlers=[
#         logging.FileHandler("run.log"),
#         logging.StreamHandler()
#     ]
# )
# logger = logging.getLogger()


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
    MAXTIME = 1e5
    global sim_time

    count = 0
    added = 1
    while sim_time < MAXTIME and not fel.empty():
        new_time, proc = fel.pop()
        sim_time = new_time
        proc.handle(fel, sim_time, sim_state)

        # Simulates adding new car to our sim
        if (np.random.random() < 0.05):  # With 5% chance
            logger.info("Adding new vehicle")
            added += 1
            arrival_time = get_random_interarrival_time()
            VehicleProcess(fel, arrival_time)  # Adds self to FEL.

        count += 1

    logger.debug("Count: {}".format(count))
    logger.debug("Vehicles Simulated: {}".format(added))
    logger.debug("Remaining: {}".format(fel.completed))
    logger.debug("Completed: {}".format(fel.completed))


if __name__ == "__main__":
    initialize()
    main()
