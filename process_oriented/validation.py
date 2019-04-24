from helpers import *

import numpy as np
from matplotlib import pyplot as plt
import scipy.stats as stats
import seaborn as sns; sns.set()
import pandas as pd

START_TIME = 1163030800

fname = "../data/trajectories.csv"
# fname = "../data/minitrajectories.csv"

df = pd.read_csv(fname, usecols=['Vehicle_ID', 'Epoch_ms',  'Org_Zone', 'Dest_Zone'])

# Filter where: Org_Zone = 114
correct_start = (df['Org_Zone'] == 114)
# Filter where: Dest_Zone = 201
correct_end = (df['Dest_Zone'] == 201)

df = df[(correct_start & correct_end)]
unique_vids = np.unique(df['Vehicle_ID'])

travel_times = []
for vid in unique_vids:
    tmp_df = df[df['Vehicle_ID'] == vid]
    start_time  =  np.min(tmp_df['Epoch_ms'])
    end_time    =  np.max(tmp_df['Epoch_ms'])
    travel_time =  end_time - start_time
    travel_times.append(travel_time / 1000)

print("="*30, " EMPIRICAL DATA ", "="*30)
print("Number of cars that traveled 10th to 14th all the way: ", len(
    travel_times))
print("Mean  travel time: {:.3f}s".format(np.mean(travel_times)))
print("Stdev travel time: {:.3f}s".format(np.std(travel_times)))

# Confidence intervals
n = len(travel_times) - 1
conf_low, conf_high = stats.t.interval(0.95, n, loc=np.mean(travel_times), scale=stats.sem(travel_times))

print("95% confidence interval of mean travel time: [{:.3f}, {:.3f}]".format(conf_low, conf_high))

fig = plt.figure(figsize=(10, 6), dpi=100)
plt.hist(travel_times, bins=10)
plt.xlabel("Travel Time (s)")
plt.ylabel("Counts")
plt.title("Empirical Travel Times Histogram")

fname = "images/empirical_time_histogram.png"
fig.savefig(fname)
print("Saving image to {}".format(fname))
