

import time
import optparse
import numpy as np
import pandas as pd
import pickle
import time

# Make sure when you call this, you use the same number of clients as the simulator
parser = optparse.OptionParser()
parser.add_option('-n', dest='num_clients')
(options, args) = parser.parse_args()

def initialize_node_data(n_clients):
    np.random.seed(42)
    df = pd.read_csv('one.csv')
    data = np.asarray(df.Temp)
    print(data.shape)
    step = int(data.shape[0] / n_clients)
    X=[]
    for c in range(n_clients):
        X.append(data[step * c: step * (c + 1)])
    X = np.asarray(X)

    np.save('vals.npy', X)

initialize_node_data(int(options.num_clients))
