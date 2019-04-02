
import time
import numpy as np
from pprint import pprint

from util import *
from traffic import *

# TODO: Get actual segment lengths.
SEG1 = 70  # 10th to 11th
SEG2 = 70  # 11th to 12th
SEG1 = 50  # 12th to 13th
SEG1 = 50  # 13th to 14th


def initialize(seg1, seg2, seg3, seg4):
    pass


def main():
    seed_rng()  # Use a seed for reproducibility.
    records = Records()  # Bookkeeping.

    # Initialize road segments.
    seg1 = RoadSegment("seg1", records, 10)  # 10th to 11th
    seg2 = RoadSegment("seg2", records, 10)  # 11th to 12th
    seg3 = RoadSegment("seg3", records, 10)  # 12th to 13th
    seg4 = RoadSegment("seg4", records, 10)  # 13th to 14th

    # Connect segments together.
    seg1.connect_segment(seg2)
    seg2.connect_segment(seg3)
    seg3.connect_segment(seg4)

    # Initialize segments with cars.
    initialize(seg1, seg2, seg3, seg4)

    travel_times = [1,1,1,1]
    for travel_time in travel_times:
        seg1.add_car(travel_time=travel_time)

    time.sleep(4.5)
    for record in records.get():
        pprint(record)


if __name__ == "__main__":
    main()
