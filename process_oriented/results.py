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

print("Number of cars that traveled 10th to 14th all the way: ", len(
    arrival_times))


print("Mean travel time:", np.mean(travel_times))
print("Stdev travel time:", np.std(travel_times))
print("Median travel time:", np.median(travel_times))


def plot_hist(data, bins=20):
    counts, mids = np.histogram(data, bins=bins)
    print(counts)
    print(mids)
    mids = mids[1:]
    plt.bar(mids, counts, width=8.0)
    plt.xticks(mids) # no need to add .5 anymore


# plt.figure(figsize=(15, 6), dpi=100)
# plot_hist(travel_times)
# plt.xlabel("Travel Time (s)")
# plt.ylabel("Counts")
# plt.title("Travel Times Histogram")

# plt.figure(figsize=(15, 6), dpi=100)
# plot_hist(arrival_times)
# plt.xlabel("Arrival Time (s)")
# plt.ylabel("Counts")
# plt.title("Travel Times Histogram")


# plt.show()


# print(np.histogram(travel_times, bins=20))

# Plot Histograms
plt.figure(figsize=(15, 6), dpi=100)
counts, mids = np.histogram(travel_times, bins=20)
plt.hist(travel_times, bins=20, density=1, alpha=0.5)
    #axis([xmin,xmax,ymin,ymax])
plt.xlabel('Car Travel Times (seconds)')
plt.ylabel('Counts')

# yrange = np.linspace(np.min(counts)-10, np.max(counts) + 10, 10)
# plt.yticks(np.arange(np.min(counts), np.max(counts)))
plt.title("Car Travel Time Histogram")
plt.show()


# plt.figure(figsize=(12, 6), dpi=100)
# plt.hist(arrival_times, bins=20, density=1, alpha=0.5)
#     #axis([xmin,xmax,ymin,ymax])
# plt.xlabel('Car Arrival Times (s)')
# plt.ylabel('Counts')
# plt.title("Car Arrival Time Histogram")

# # plt.show()
