from mininet.net import Mininet
from mininet.node import Node
from mininet.topo import SingleSwitchTopo
from sec_agg_topo import smc_topo
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import OVSController
from mininet.link import TCLink

import time
import optparse
import os


setLogLevel('debug')
#setLogLevel('debug')

def write_diff_to_timer_log(message, time_diff):
    f = open('log_times.txt', 'a')
    f.write('internal: ' + message + " " + str(time_diff) + "s \n")
    f.close()

def write_message_to_timer_log(message):
    f = open('log_times.txt', 'a')
    f.write(message)
    f.close()


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



parser = optparse.OptionParser()
parser.add_option('--bandwidth', dest='bandwidth', type='float')
parser.add_option('--latency', dest='latency', type='string')
parser.add_option('--msg', dest='msg', type='string')
(options, args) = parser.parse_args()

topo = smc_topo(options.bandwidth, options.latency)   #topo is static for 3 inodes

net = Mininet(topo = topo, controller=OVSController, link=TCLink)
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

# Write to timer log file
write_message_to_timer_log("\n\nStarting simulation with parameters bandwidth=%s latency=%s %s\n\n" % (str(options.bandwidth), options.latency, options.msg))

#Set up aggregator and queryer listeners
start_agg_query_nodes(query_node, agg_node)

print("Aggregator and Query set up!")
print("Starting sensor transmissions!")


#Begin sensor node transmissions
transmit_sensor_values(input_nodes, agg_node)

time.sleep(5)

print("End sensor transmissions")


# Measure the latency and bandwidth of each session

# Stop the network
net.stop()

# Side note - you have to install packages from python -m -pip install
