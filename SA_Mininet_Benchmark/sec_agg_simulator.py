from mininet.net import Mininet
from mininet.node import Node
from mininet.topo import SingleSwitchTopo
from sec_agg_topo import smc_topo
from mininet.log import setLogLevel
from mininet.cli import CLI

import time
import optparse
import os


# This parses a fraction given on the command line
#  should be of the form X-Y where X is the number of input nodes
#   and y is the number of computation nodes
def parse_fractions(frac_str):
    frac = [int(x) for x in frac_str.split('-')]
    frac.insert(0, sum(frac))
    return frac
#setLogLevel('output')
setLogLevel('debug')

parser = optparse.OptionParser()
parser.add_option('-r', dest='ratios')
(options, args) = parser.parse_args()
net_params = parse_fractions(options.ratios)



# Send sensor node values to aggregator node
def transmit_sensor_values(sensor_nodes, aggregator_node):

    # #initialize sensor values
    # data_values = initialize_node_data(len(sensor_nodes))

    for s_i, sensor_node in enumerate(sensor_nodes):

        print("Transmitting from " + str(sensor_node.IP()))
        #msg = pickle.dumps(data_values[s_i])
        sensor_node.popen('python3 sensor_node.py --idx ' + str(s_i) + ' --it ' + str(aggregator_node.IP()))

# This starts the aggregator and query nodes
#  aggregator begins listening for data
#  queryer sets up weights and transmits to aggregator
#  queryer then waits for response from aggregator
#  aggregator receives the weights
#  aggregator then waits for input from sensor nodes
#  aggregator receives data from sensor nodes and computes the convolve value
#  aggregator returns the value to queryer
def start_agg_query_nodes(query_node, aggregator_node):

    query_port = 12355
    # setup aggregator node for listening
    agg = aggregator_node.popen('python3 aggregator_node.py -n ' + str(0) + ' -i ' + str(aggregator_node.IP()) + ' --it ' + str(query_node.IP())
    + ' --pt ' + str(query_port))

    # Important - sleep for a bit to give the nodes time to set up
    time.sleep(2)

    # setup query node - it will transmit to aggregator node
    query = query_node.popen('python3 query_node.py -n ' + str(0) + ' -i ' + str(query_node.IP()) + ' --it ' + str(aggregator_node.IP()) +
    ' -p ' + str(query_port))

    # Important - sleep for a bit to give the nodes time to set up
    time.sleep(2)

# Net params - 0th position is total nodes, 1st is the num of inodes, 2nd is
#  num of comp_nodes

# First to set up the topology
# Single switch and 3 hosts should work for now
#topo = SingleSwitchTopo(net_params[0])

topo = smc_topo(net_params[0])   #TODO: Pointless at the moment - the topo is static for 3 inodes

net = Mininet(topo = topo)
net.start()

hosts = net.hosts
# Then decide which hosts are computation and which are input nodes, as well
#  as a final querying node

input_nodes = hosts[:3]
agg_node = hosts[3]
query_node = hosts[4]
print('len - input: ' + str(len(input_nodes)))
print('query node: ' + str(query_node.IP()))
print('agg_node: ' + str(agg_node.IP()))


#Set up aggregator and queryer listeners
start_agg_query_nodes(query_node, agg_node)

print("Aggregator and Query set up!")
print("Starting sensor transmissions!")

# Important - sleep for a bit to give the nodes time to set up
time.sleep(2)

#Begin sensor node transmissions
transmit_sensor_values(input_nodes, agg_node)

print("End sensor transmissions")
# Important - sleep for a bit to give the nodes time to set up
time.sleep(2)

# Measure the latency and bandwidth of each session

# Stop the network
net.stop()


# Side note - you have to install packages from python -m -pip install
