import numpy as np
#from sklearn.datasets import load_diabetes
import phe as paillier
#from sklearn.model_selection import train_test_split as tts
import pandas as pd
import time
import pickle

import socket, optparse

parser = optparse.OptionParser()
parser.add_option('-i', dest='ip_source', default='127.0.0.1')
parser.add_option('-p', dest='port_source', type='int', default=12345)
parser.add_option('--it', dest='ip_dest', default='127.0.0.1')
parser.add_option('--pt', dest='port_dest', type='int', default=12345)
parser.add_option('-n', dest='num')
(options, args) = parser.parse_args()

def write_to_timer_log(message):
    f = open('log_times.txt', 'a')
    f.write(message + " at time=%s\n" %(time.time()))
    f.close()

def setup_node():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return s

# Listen for received data
def listen_for_query(sock, ip_src, port_src, num):

    print("IP src and port: " + str(ip_src) + " " + str(port_src))
    sock.bind( (ip_src, int(port_src)) )


    # open file for writing
    f = open('log_agg_' + num + '.txt','w+')

    weights = []

    while True:
        data, addr = sock.recvfrom(2048)
        q_recv_t = time.time()
        #f.write("Received query at t=%s" %(q_recv_t))
        #data = data.decode()
        print('hello we have received query')
        f.write("Recieved data: %s, %s only first 20 bytes \n\n" % (addr, data[:20]))
        write_to_timer_log("Received query at agg ")

        # save weights and quit
        weights = pickle.loads(data)
        #f.write("\nBODOD")
        f.flush()
        break

    f.close()
    return weights


def listen_for_data(sock, ip_src, port_src, num, weights, total_nodes):

    # open file for writing
    f = open('log_agg_' + num + '.txt','a')

    # current weight index
    w_i = 0
    # current convolve value
    convolve = 0
    f.write("Started new listening for sensor nodes")
    while True:
        data, addr = sock.recvfrom(2048)
        #f.write("Received sensor data from %s at t=%s" %(addr, time.time()))

        #data = data.decode()
        data = pickle.loads(data)
        print('\nhello we have received data')
        f.write("\nRecieved sensor data: %s, %s only first 20 bytes\n\n" % (addr, data))
        write_to_timer_log("Aggregator received sensor data from " + str(addr))

        convolve += weights[w_i]*data
        #f.write("\nWOWZERS")
        w_i += 1

        if (total_nodes <= w_i):
          f.write("Final convolve value: " + str(convolve))
          break

        f.flush()
    f.close()
    return convolve

# Ip dest should be the queryer
def transmit_final_val(sock, message, ip_dest, port_dest):
    #sock.sendto(message.encode(), (ip_dest, port_dest)
    f = open('log_agg_' + options.num + '.txt','a')
    toSend = pickle.dumps(message)

    write_to_timer_log("Transmitting aggregated value")
    sock.sendto(toSend, (ip_dest, port_dest) )

    #f.write("Transmitting calculated value at t=%s" %(time.time()))

    f.write("Transmitted from aggregator to " + str(ip_dest) + " " + str(port_dest))
    f.close()




n_clients = 3

# setup the node
sock = setup_node()
print("Aggregator waiting for query...")
# Listen for a query from the queryer
weights = listen_for_query(sock, options.ip_source, options.port_source, options.num)



# Something to keep in mind - this implementation does not care about the ordering
#  of convolutions to nodes (i.e. 1st recevied node does not match with 1st weight)
convolve = listen_for_data(sock, options.ip_source, options.port_source, options.num, weights, n_clients)

sock = setup_node()  #set up again otherwise we get send errors
#Transmit final value to queryer
transmit_final_val(sock, convolve, options.ip_dest, options.port_dest)

f = open('log_agg_' + options.num + '.txt','a')
f.write("\nEnd\n")
f.close()
