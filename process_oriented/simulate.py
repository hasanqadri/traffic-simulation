import numpy as np

from helpers import *
from util import *
from threaded import *

sim_state = None
sim_time  = None


# Signal name, green time, red time
signal_timings = [
    (SIG0,      38.1,         49.3),  # 10th
    (SIG1,      44.7,         55.4),  # 11th
    (SIG2,      64.1,         35.7),  # 12th
    (SIG4,      37.8,         45.3),  # 14th

    (SIG0_LEFT, 10.6,  2.2),  # 10th street, left turn
    (SIG4_LEFT, 12.4,  3.6),  # 14th street, left turn
]


def initialize():
    global sim_time
    global sim_state

    sim_time = 0
    sim_state = SimulationState()

    for (signame, green_time, red_time) in signal_timings:
        signal = Signal(signame, green_time, red_time)

        sim_state.add_signal(signame, signal)

        print(signal)


if __name__ == "__main__":
    initialize()
