import numpy as np
from util import *


# TODO: Get average velocities from trajectories.csv
VELOCITIES = {
    "MOTORCYCLE":   1,
    "CAR":          2,
    "TRUCK":        1,
}

# TODO: Get average vehicle lengths from trajectories.csv
LENGTHS = {
    "MOTORCYCLE":   1,
    "CAR":          2,
    "TRUCK":        2.5,
}

N_LANES         = 2  # Two lane, one-way roads
LANES_POSSIBLE  = [1, 2]


class Vehicle():
    """
    A class to capture vehicle driving. Driving is an activity.
    """

    def __init__(self, vehicle_type):

        if vehicle_type not in VELOCITIES.keys():
            raise ValueError(f"Vehicle type '{vehicle_type}' not supported.")

        self.vehicle_type  = vehicle_type
        self.vel           = VELOCITIES[vehicle_type]
        self.length        = LENGTHS[vehicle_type]

        self.turned        = False  # Indicates if this turned off Peachtree street.
        self.lane          = 1      # Which lane vehicle is in. Can be 1 or 2.
        self.y             = 0      # How far along the track we've gone.

        # Track time steps taken by this vehicle.
        self.total_time   = 0


    def drive(self, vehicle_positions, dt):
        """
        :vehicle_positions:  - list of (lane, y, length) of where all other vehicles are
        at this time step.
        :dt: delta_t, the timestep to move by.
        """
        # Update time spent.
        self.total_time += dt

        v1_length = self.length

        v1_y_fullstep  = self.y + self.vel * dt          # Full speed
        v1_y_halfstep  = self.y + (self.vel * 0.5 * dt)  # Half speed

        switch = should_switch_lane()  # Switch lane with some probability
        if switch:
            v1_lane = 2 if self.lane == 1 else 1  # Flip the lane
        else:
            v1_lane = self.lane

        if can_place(vehicle_positions, v1_lane, v1_y_fullstep, v1_length):
            return (v1_lane, v1_y_fullstep, v1_length)

        elif can_place(vehicle_positions, v1_lane, v1_y_halfstep, v1_length):
            return (v1_lane, v1_y_halfstep, v1_length)

        elif switch and can_place(vehicle_positions, self.lane, v1_y_fullstep, v1_length):
            return (v1_lane, v1_y_fullstep, v1_length)

        elif switch and can_place(vehicle_positions, self.lane, v1_y_halfstep, v1_length):
            return (v1_lane, v1_y_halfstep, v1_length)

        return (self.lane, self.y, self.length)


    def done_driving(self, y_max):
        return (self.turned or self.y >= y_max)

