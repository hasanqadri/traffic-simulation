"""
NOTE: This will not run on PACE as-is. Comment out the "import seaborn" line.
"""

from helpers import *

import numpy as np
from matplotlib import pyplot as plt
import scipy.stats as stats

try:
    import seaborn as sns; sns.set()
    pass
except:
    print("Seaborn is not installed. Proceeding without it.")


filename = "vehicle_metadata.pkl"
completed_procs = readpkl(filename)  # List<(time_arrive, time_exit)>

# We really only care about the time to INIT and END
arrival_times = np.array(list((map(lambda x: x[0], completed_procs))))
exit_times    = np.array(list((map(lambda x: x[1],  completed_procs))))
travel_times = exit_times - arrival_times


def compute_mavg(travel_times):
    mavg = []
    N = len(travel_times)
    for i in range(1, N):
        mavg.append(np.mean(travel_times[:i]))

    return mavg

mavg = compute_mavg(travel_times)
xs = range(len(mavg))

fig = plt.figure(figsize=(10, 6), dpi=100)
plt.plot(xs, mavg, label="Moving Average of Travel Time")
plt.axvline(x=25000, color="red", label="Cutoff")
plt.xlabel("Samples taken")
plt.ylabel("Mean Travel Time of Samples (s)")
plt.title("Moving Average of Mean Travel Time")
plt.legend()

fig.savefig("images/warmup.png")


# Based on above, we know k = 25000 is a good cutoff
k = 25000
travel_times = travel_times[k:]

print("Discarding the first {} samples.".format(k))
print("Number of cars that traveled 10th to 14th all the way: ", len(
    arrival_times))
print("Mean  travel time: {:.3f}s".format(np.mean(travel_times)))
print("Stdev travel time: {:.3f}s".format(np.std(travel_times)))


# Confidence intervals
n = len(travel_times) - 1
conf_low, conf_high = stats.t.interval(0.95, n, loc=np.mean(travel_times), scale=stats.sem(travel_times))

print("95% confidence interval of mean travel time: [{:.3f}, {:.3f}]".format(conf_low, conf_high))


# Histogram
fig = plt.figure(figsize=(10, 6), dpi=100)
plt.hist(travel_times, bins=20)
plt.xlabel("Travel Time (s)")
plt.ylabel("Counts")
plt.title("Travel Times Histogram")

fig.savefig("images/travel_time_histogram.png")
