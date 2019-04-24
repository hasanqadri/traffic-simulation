"""
NOTE: This will not run on PACE as-is. Comment out the "import seaborn" line.
"""

import numpy as np
from matplotlib import pyplot as plt
import scipy.stats as stats

try:
    import seaborn as sns; sns.set()
    pass
except:
    print("Seaborn is not installed. Proceeding without it.")

from event_sim import *

############################ INIT ###############################
START_TIME = 1163030800;
currentTime = START_TIME;

with open('../data/trajectories0.json') as json_data:
    events = json.load(json_data)

numEvents = len(events.keys())
global interArrivalTimes
interArrivalTimes = []
for z in range(numEvents):
    ts = events[str(z)]['Epoch_ms'] - START_TIME
    interArrivalTimes.append(ts)

##############################################################

def get_arrival_times(size):
    arrival_times = np.random.choice(interArrivalTimes, size=size, replace=False)
    return arrival_times

np.random.seed(42)
samples = get_arrival_times(10000)

print("Arrival Time Mean:   {:.3f}".format(np.mean(samples)))
print("Arrival Time Stdev:  {:.3f}".format(np.std(samples)))

# Confidence intervals
n = len(samples) - 1
conf_low, conf_high = stats.t.interval(0.95, n, loc=np.mean(samples), scale=stats.sem(samples))

print("95% confidence interval of Mean Arrival Time: [{:.3f}, {:.3f}]".format(conf_low, conf_high))


fig = plt.figure(figsize=(10, 6), dpi=100)

plt.hist(samples, bins=20)
plt.xlabel("Arrival Time (s)")
plt.ylabel("Counts")
plt.title("Arrival Times Histogram")

fname = "images/arrivals_histogram.png"
fig.savefig(fname)
print("Saving file out to {}".format(fname))
