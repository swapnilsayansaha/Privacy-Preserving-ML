from mininet.net import Mininet
from mininet.node import Node
from mininet.topo import SingleSwitchTopo
from custom_topo import smc_topo
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

# Begin listening for incoming transmissions on computations
def setup_listeners(computation_nodes):

    for c_i, comp_node in enumerate(computation_nodes):
        p1 = comp_node.popen('python compnode.py -n ' + str(c_i) + ' -i %s &' % comp_node.IP())
        print('listening for incoming transmissions on ' + str(comp_node.IP()))
        print('producing log files at log' + str(c_i) + ".txt")


# Create message passing function from input nodes to computation nodes, and message
#  passing in between computation nodes.
# This means custom functions depending on what nodes are what
def inodes_msg_passing(inodes, msg, computation_nodes):

    for c_i, comp_node in enumerate(computation_nodes):
        # For every input node, we pass the message to all computation nodes
        for i_i, inode in enumerate(inodes):
            print('inode: ' + str(i_i) + 'transmitting to ' + str(comp_node.IP()))
            inode.cmd('python inode.py -i %s -m "hello from inode"' % comp_node.IP())


# Net params - 0th position is total nodes, 1st is the num of inodes, 2nd is
#  num of comp_nodes

# First to set up the topology
# Single switch and 3 hosts should work for now
#topo = SingleSwitchTopo(net_params[0])
topo = smc_topo(net_params[0])

net = Mininet(topo = topo)
net.start()

hosts = net.hosts
# Then decide which hosts are computation and which are input nodes, as well
#  as a final querying node
# input_nodes = hosts[:net_params[1]]
# computation_nodes = hosts[net_params[1]:]
input_nodes = hosts[:3]
computation_nodes = hosts[3:]
print('len - input: ' + str(len(input_nodes)))
print('len - comp: ' + str(len(computation_nodes)))

#Write down who the computation nodes are so they communicate with each other
f = open('comp_ips.txt','w')
for comp_node in computation_nodes:
    f.write(str(comp_node.IP()) + '\n')
f.close()

#Make sure computation nodes are listening for incoming traffic
setup_listeners(computation_nodes)

# Important - sleep for a bit to give the nodes time to set up
time.sleep(2)

# Use message passing function in sessions of some time, after which
#  the result will get passed to the querying node.
inodes_msg_passing(input_nodes, "", computation_nodes)

# Measure the latency and bandwidth of each session

# Stop the network
net.stop()


# Side note - you have to install packages from python -m -pip install
