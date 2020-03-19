import numpy as np
#from sklearn.datasets import load_diabetes
import phe as paillier
#from sklearn.model_selection import train_test_split as tts
import pandas as pd
import pickle
import time

import socket, optparse

parser = optparse.OptionParser()
parser.add_option('--it', dest='ip_dest', default='127.0.0.1')
parser.add_option('--pt', dest='port_dest', type='int', default=12345)
parser.add_option('--idx', dest='sensor_index', type='int')
(options, args) = parser.parse_args()

def write_to_timer_log(message):
    f = open('log_times.txt', 'a')
    f.write(message + " at time=%s\n" %(time.time()))
    f.close()



class Client:

    def __init__(self, X, pubkey=None, privatekey=None):
        self.pubkey = pubkey
        self.privatekey = privatekey
        self.X = X

    def mean(self):
        return np.mean(self.X)

    def encrypt_mean(self):
        return self.pubkey.encrypt(self.mean())

    def decrypt_mean(self, mean_server):
        return self.privatekey.decrypt(mean_server)

    def encrypt_square_sum(self):
        return self.pubkey.encrypt(np.sum(np.square(self.X)))

def load_from_np_file(file, index):

    values = np.load(file)
    return values[index]


# Transmit a message from a client
def setup_and_transmit(ip_dest, port_dest, message, sensor_index):

    f = open('log_sensor_nodes.txt','a')

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    public_key = pickle.load( open( "public_key.p", "rb" ) )
    private_key = pickle.load(open( "private_key.p", "rb" ))
    client = Client(message, public_key, private_key)
    data = pickle.dumps(client.mean())

    write_to_timer_log("Sensor node " + str(sensor_index) + " transmitting")
    s.sendto(data, (ip_dest, port_dest) )

    print("Transmitting to: " + str(ip_dest))

    f.close()


f = open('log_sensor_nodes.txt','w')
f.close()
message = load_from_np_file("vals.npy", options.sensor_index)
setup_and_transmit(options.ip_dest, options.port_dest, message, options.sensor_index)
