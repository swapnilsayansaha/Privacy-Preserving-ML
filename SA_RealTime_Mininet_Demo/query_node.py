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

def load_encrypt_weights(n_clients):
    public_key = pickle.load( open( "public_key.p", "rb" ) )
    private_key = pickle.load(open( "private_key.p", "rb" ))

    weights = np.random.randint(low=0, high=15, size=(n_clients,1))
    weights_encrypted = []
    for i in range(n_clients):
        w = int(weights[i,0])
        weights_encrypted.append(public_key.encrypt(w))
    data=pickle.dumps(weights_encrypted)

    return private_key, data

#send the data
def transmit_weights(sock, message, ip_dest, port_dest, num):
    f = open('log_query_' + num + '.txt', 'w+')
    f.write("Transmitting data to " + str(ip_dest) + "\n")
    #f.write("query sent at %s" %(time.time()))
    write_to_timer_log("Query sending:")
    #sock.sendto(message.encode(), (ip_dest, port_dest) )
    sock.sendto(message, (ip_dest, int(port_dest)) )
    f.close()

# Listen for received data
def listen_for_data(sock, private_key, ip_src, port_src, num):

    print("IP src and port: " + str(ip_src) + " " +  str(port_src))
    sock.bind( (ip_src, int(port_src)) )

    print("Successfully bound.")
    # open file for writing
    f = open('log_query_' + num + '.txt','a')
    f.write("Queryer listening at " + ip_src + " w/ port " + str(port_src) +"\n")
    f.close()
    # reopen -  we would expect to see the above output if we got to listen
    f = open('log_query_' + num + '.txt','a')

    while True:
        data, addr = sock.recvfrom(2048)
        #f.write("Received final query result at t=%s\n" %(time.time()))
        write_to_timer_log("Query Received:")
        data = pickle.loads(data)
        #data = data.decode()
        print('hello we have received data')
        f.write("Recieved data: %s, %s\n" % (addr, data))

        #receive the data
        decrypted_convolve = private_key.decrypt(data)
        f.write("Decrypted Values: %s, %s\n" % (addr, decrypted_convolve))

        f.flush()
        break
    f.close()


n_clients = 3
sock = setup_node()
priv_key,data  = load_encrypt_weights(n_clients)
transmit_weights(sock, data, options.ip_dest, options.port_dest, options.num)

print('setting up query listener on ' + str(options.ip_source))
sock = setup_node()  # setup node again othewise we can't bind?
listen_for_data(sock, priv_key, options.ip_source, options.port_source, options.num)
