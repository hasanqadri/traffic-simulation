
import time
import numpy as np
from pprint import pprint

from util import *
from traffic import *

# TODO: Modify these parameters
n_moving_seg1 = 5  # 10th to 11th
n_moving_seg2 = 5 # 11th to 12th
n_moving_seg3 = 5  # 12th to 13th
n_moving_seg4 = 2  # 13th to 14th


def initialize(seg1, seg2, seg3, seg4):
    seg1_travel_times = random_travel_time(size=10)
    seg2_travel_times = random_travel_time(size=10)
    seg3_travel_times = random_travel_time(size=10)
    seg4_travel_times = random_travel_time(size=10)

    seg1._initialize(seg1_travel_times)
    seg2._initialize(seg2_travel_times)
    seg3._initialize(seg3_travel_times)
    seg4._initialize(seg4_travel_times)


def main():
    seed_rng()  # Use a seed for reproducibility.
    records = Records()  # Bookkeeping.

    # Initialize road segments.
    seg1 = RoadSegment(name_seg1, records, n_moving_seg1)  # 10th to 11th
    seg2 = RoadSegment(name_seg2, records, n_moving_seg2)  # 11th to 12th
    seg3 = RoadSegment(name_seg3, records, n_moving_seg3)  # 12th to 13th
    seg4 = RoadSegment(name_seg4, records, n_moving_seg4)  # 13th to 14th

    # Connect segments together.
    seg1.connect_segment(seg2)
    seg2.connect_segment(seg3)
    seg3.connect_segment(seg4)

    # Initialize segments with cars.
    initialize(seg1, seg2, seg3, seg4)
    # Start up all the queues
    seg1.start()
    seg2.start()
    seg3.start()
    seg4.start()


    # TODO: Use information about segments.
    time.sleep(15)


    for record in records.get():
        key_start  = enter(name_seg1)
        key_end    = leave(name_seg4)

        if key_start in record and key_end in record:
            start = record[key_start]
            end = record[key_end]

            elapsed = "Elapsed: {:.2f}s".format(end - start)
            print(elapsed)


if __name__ == "__main__":
    main()
