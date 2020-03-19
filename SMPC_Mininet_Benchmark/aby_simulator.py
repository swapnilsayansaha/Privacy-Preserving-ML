from mininet.net import Mininet
from mininet.node import Node
from mininet.topo import SingleSwitchTopo
from custom_topo import smc_topo
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import OVSController
from mininet.util import pmonitor

import time
import optparse
import os


def begin_node_comm(node, role):

    # Assume we installed under build/python and we are calling build/bin/millionaire...
    node.pexec("../bin/millionaire_prob_test -r " + str(role))

setLogLevel('debug')

topo = smc_topo(1)
net = Mininet(topo = topo, controller=OVSController)
net.start()

hosts = net.hosts
# Then decide which hosts are computation and which are input nodes, as well
#  as a final querying node

cnode0 = hosts[0]
cnode1 = hosts[1]
print('node 0: ' + str(cnode0.IP()))
print('node 1: ' + str(cnode1.IP()))

# begin_node_comm(cnode0, 0)
# begin_node_comm(cnode1, 1)
monitor = {}
monitor[cnode0] = cnode0.popen("../bin/millionaire_prob_test -r 0 -a " + str(cnode0.IP()))
monitor[cnode1] = cnode1.popen("../bin/millionaire_prob_test -r 1 -a " + str(cnode0.IP()))

for h, line in pmonitor(monitor, timeoutms=500):
    if h:
        print '%s: %s' % (h.name, line)


# Stop the network
net.stop()


# Side note - you have to install packages from python -m -pip install
