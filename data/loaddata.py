"""
Utility for loading data from pkl format, either zipped or unzipped.
"""

import pickle
import gzip

def readpkl(fname):
    with open(fname, 'rb') as f:
        data = pickle.load(f)

    return data

def compressed_readpkl(fname):
    with gzip.open(fname, 'rb') as f:
        data = pickle.load(f)

    return data


def savepkl(data, fname):
    with open(fname, 'wb') as f:
        pickle.dump(data, f)


def compressed_savepkl(data, fname):
    with gzip.open(fname, 'wb') as f:
        pickle.dump(data, f)
