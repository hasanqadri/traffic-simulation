"""
NOTE: This will not run on PACE as-is. Comment out the "import seaborn" line.
"""

from helpers import *

import numpy as np
from matplotlib import pyplot as plt

try:
    import seaborn as sns; sns.set()
    pass
except:
    print("Seaborn is not installed. Proceeding without it.")

from helpers import *
from simulate import *

init_interarrival_times()

samples = [get_random_interarrival_time() for _ in range(100000)]

fig = plt.figure(figsize=(10, 6), dpi=100)

plt.hist(samples, bins=20)
plt.xlabel("Arrival Time (s)")
plt.ylabel("Counts")
plt.title("Arrival Times Histogram")

fname = "images/arrivals_histogram.png"
fig.savefig(fname)
print("Saving file out to {}".format(fname))
