from helpers import *

import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns; sns.set()


filename = "completed_procs_results.pkl"
completed_procs = readpkl(filename)

# We really only care about the time to INIT and END
arrival_times = np.array(list((map(lambda x: x['INIT'], completed_procs))))
exit_times    = np.array(list((map(lambda x: x['END'],  completed_procs))))
travel_times = exit_times - arrival_times


def compute_mavg(travel_times):
    mavg = []
    N = len(travel_times)
    for i in range(1, N):
        mavg.append(np.mean(travel_times[:i]))

    return mavg

mavg = compute_mavg(travel_times)
xs = range(len(mavg))
plt.plot(xs, mavg)
plt.axvline(x=30000, color="red")

# Based on above, we know k=30000 is a good cutoff
k = 30000
travel_times = travel_times[k:]


print("Number of cars that traveled 10th to 14th all the way: ", len(
    arrival_times))

print("Mean travel time: {:.3f} s".format(np.mean(travel_times)))
print("Stdev travel time: {:.3f} s".format(np.std(travel_times)))
print("Median travel time: {:.3f} s".format(np.median(travel_times)))


def plot_hist(data, bins=20, ticks=True):
    counts, mids = np.histogram(data, bins=bins)
    mids = mids[1:]
    plt.bar(mids, counts, width=8.0)

    if ticks:
        plt.xticks(mids) # no need to add .5 anymore

plt.figure(figsize=(15, 6), dpi=100)
plot_hist(travel_times, bins=20)
plt.xlabel("Travel Time (s)")
plt.ylabel("Counts")
plt.title("Travel Times Histogram")

# plt.show()
