# Process-Based Queues

## Requirements
This project uses `python3`.

## Running on PACE
To execute the simulation, run the following on PACE servers:
```bash
module load anaconda3/4.2.0
python simulate.py
```

## Interpreting Output
The output of the script is the elapsed time each vehicle took to go from
the 10th street intersection to the 14th street intersection. The vehicles
that began at any point other than the 10th street intersection or ended at
any point before the 14th street intersection are discarded for now.

### Example Results
```
...
Elapsed: 1.31s
Elapsed: 1.57s
Elapsed: 1.67s
Elapsed: 1.69s
Elapsed: 1.90s
Elapsed: 2.23s
Elapsed: 2.34s
Elapsed: 2.35s
Elapsed: 2.47s
Elapsed: 2.72s
Elapsed: 2.78s
Elapsed: 2.89s
Elapsed: 3.06s
Elapsed: 3.26s
Elapsed: 3.42s
Elapsed: 3.49s
Elapsed: 3.77s
Elapsed: 3.86s
Elapsed: 4.20s
Elapsed: 4.35s
```
