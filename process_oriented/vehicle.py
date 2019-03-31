import numpy as np
from util import *


# TODO: Get averages from trajectories.csv
VELOCITIES = {
    "MOTORCYCLE":   1,
    "CAR":          2,
    "TRUCK":        1,
}

# TODO: Get averages from trajectories.csv
LENGTHS = {
    "MOTORCYCLE":   1,
    "CAR":          2,
    "TRUCK":        1,
}

N_LANES         = 2  # Two lane, one-way roads
LANES_POSSIBLE  = [1, 2]

class Vehicle():

    def __init__(self, vehicle_type):

        if vehicle_type not in VELOCITIES.keys():
            raise ValueError(f"Vehicle type '{vehicle_type}' not supported.")

        self.vehicle_type  = vehicle_type

        self.vel           = VELOCITIES[vehicle_type]
        self.length        = LENGTHS[vehicle_type]

        self.lane          = 1  # Which lane vehicle is in. Can be 1 or 2.
        self.y             = 0  # How far along the track we've gone.

        self.start_time   = None
        self.end_time     = None


    def drive(self, vehicle_positions, dt):
        """
        :vehicle_positions:  - list of (lane, y, length) of where all other vehicles are
        at this time step.
        :dt: delta_t, the timestep to move by.
        """
        v2_length = self.length

        v2_y_fullstep  = self.y + self.vel * dt          # Full speed
        v2_y_halfstep  = self.y + (self.vel * 0.5 * dt)  # Half speed

        switch = switch_lane()
        if switch:
            v2_lane = 2 if self.lane == 1 else 1
        else:
            v2_lane = self.lane

        fullstep_valid   = True
        halfstep_valid   = True

        # if can_place(vehicle_positions, v1_lane, v1_y, v1_length)

        # Check if either half step or full step is fine with this v2_lane.
        # Start evaluating full step. If this creates a collision
        # we will switch to half step. Otherwise we won't move.
        for (v1_lane, v1_y, v1_length) in vehicle_positions:

            # Try going at full velocity.
            if fullstep_valid:
                if will_collide(v1_lane, v1_y, v1_length, v2_lane, v2_y_fullstep,
                                v2_length):
                    fullstep_valid = False
                else:
                    continue  # Continue if no problem so far

            # Try going at half velocity.
            if halfstep_valid:
                if will_collide(v1_lane, v1_y, v1_length, v2_lane, v2_y_halfstep,
                                v2_length):
                    halfstep_valid = False
                    break  # Break out of the loop
                else:
                    continue  # Continue if no problem so far


        if fullstep_valid:
            return (v2_lane, v2_y_fullstep, v2_length)
        elif halfstep_valid:
            return (v2_lane, v2_y_halfstep, v2_length)
        elif not switch:
            # If we never switched lanes, we must just stay put in the same spot.
            return (self.lane, self.y, v2_length)


        # If we simulated lane change, undo lane change
        v2_lane         = self.lane
        fullstep_valid  = True
        halfstep_valid  = True

        # Repeat above step, but now staying in same lane.
        for (v1_lane, v1_y, v1_length) in vehicle_positions:

            # Try going at full velocity.
            if fullstep_valid:
                if will_collide(v1_lane, v1_y, v1_length, v2_lane, v2_y_fullstep,
                                v2_length):
                    fullstep_valid = False
                else:
                    continue  # Continue if no problem so far

            # Try going at half velocity.
            if halfstep_valid:
                if will_collide(v1_lane, v1_y, v1_length, v2_lane, v2_y_halfstep,
                                v2_length):
                    halfstep_valid = False
                    break  # Break out of the loop
                else:
                    continue  # Continue if no problem so far


        if fullstep_valid:
            return (v2_lane, v2_y_fullstep, v2_length)
        elif halfstep_valid:
            return (v2_lane, v2_y_halfstep, v2_length)

        # We must just stay put in the same spot.
        return (self.lane, self.y, v2_length)






















            if not will_collide(v1_lane, v1_y, v1_length, v2_lane,
                v2_y, v2_length):
                continue  # Continue if no problem so far

            # If we collide:
            if v2_y == v2_y_fullstep:
                v2_y

            # Try going at half velocity.
            elif not will_collide(v1_lane, v1_y, v1_length, v2_lane,
                v2_y_halfstep, v2_length):
                continue  # Continue if no problem so far

            # Try going at half velocity.
            elif not will_collide(v1_lane, v1_y, v1_length, v2_lane,
                v2_y_halfstep, v2_length):
                continue  # Continue if no problem so far

