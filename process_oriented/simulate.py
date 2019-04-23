import numpy as np

from helpers import *
from empirical import *
from util import *
from threaded import *

sim_state = SimulationState()
sim_time  = 0
fel       = FutureEventList()
events    = {}
numEvents = 0

# Signal name, green time, red time
signal_timings = [
    (SIG0,      38.1,         49.3),  # 10th
    (SIG1,      44.7,         55.4),  # 11th
    (SIG2,      64.1,         35.7),  # 12th
    (SIG4,      37.8,         45.3),  # 14th

    (SIG0_LEFT, 10.6,  2.2),  # 10th street, left turn
    (SIG4_LEFT, 12.4,  3.6),  # 14th street, left turn
]

def getInterArrivalTime():
    global numEvents
    global events

    events = compressed_readpkl(DATAPATH)
    #Interarrival times
    interArrivalTimes = [0]

    # Dividing by 10k limits range of interarrival times but GREATLY speeds
    # up the simulation
    for n in range(int(numEvents/10000)):
        interArrivalTimes.append(0)

    for z in range(int(numEvents/10000)):
        interArrivalTimes[z] = events[str(z)]['Epoch_ms'] - START_TIME
    i = random.randint(0, int(numEvents/10000))
    if (interArrivalTimes[i] < currentTime):
        return abs(interArrivalTimes[i] - currentTime) + interArrivalTimes[i] + 5000
    return interArrivalTimes[i]


def initialize():
    global numEvents
    numEvents = len(EVENTS)

    for (signame, green_time, red_time) in signal_timings:
        signal = Signal(signame, green_time, red_time)

        sim_state.add_signal(signame, signal)
        print(signal)

        # Creates a process. Assume it starts green, so switch when
        #
        SignalProcess(fel, sim_time + red_time, signame)

    print(fel.size())
    print(fel.data)


if __name__ == "__main__":
    initialize()
