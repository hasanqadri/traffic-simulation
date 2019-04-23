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

print("Number of cars: ", len(arrival_times))


print("Mean travel time", np.mean(travel_times))
print("Var travel time", np.var(travel_times))
print("Std travel time", np.std(travel_times))
print("Median travel time", np.median(travel_times))

print("Sample travel times: ", travel_times[::500])

# Plot Hisotgrams
# plt.hist(travel_times, bins=20, density=1, alpha=0.5, edgecolor='#E6E6E6', color='#EE6666')

plt.figure(figsize=(12, 6), dpi=100)
plt.hist(travel_times, bins=10, density=1, alpha=0.5)
    #axis([xmin,xmax,ymin,ymax])
plt.xlabel('Car Travel Times (seconds)')
plt.ylabel('Counts')
plt.title("Car Travel Time Histogram")


plt.figure(figsize=(12, 6), dpi=100)
plt.hist(arrival_times, bins=10, density=1, alpha=0.5)
    #axis([xmin,xmax,ymin,ymax])
plt.xlabel('Car Arrival Times (s)')
plt.ylabel('Counts')
plt.title("Car Arrival Time Histogram")

# plt.show()
