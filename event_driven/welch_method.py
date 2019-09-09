def compute_mavg(travel_times):
    mavg = []
    N = len(travel_times)
    for i in range(1, N):
        mavg.append(np.mean(travel_times[:i]))

    return mavg

mavg = compute_mavg(travel_times)
xs = range(len(mavg))

fig = plt.figure(figsize=(15, 6), dpi=100)
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


fig = plt.figure(figsize=(15, 6), dpi=100)
plt.hist(travel_times, bins=20)
plt.xlabel("Travel Time (s)")
plt.ylabel("Counts")
plt.title("Travel Times Histogram")

fig.savefig("images/travel_time_histogram.png")