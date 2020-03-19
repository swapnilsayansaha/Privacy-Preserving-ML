import numpy as np
from sklearn.datasets import load_diabetes
import phe as paillier
from sklearn.model_selection import train_test_split as tts
import pandas as pd
import time
import pickle





np.random.seed(42)
n_clients = 100
df = pd.read_csv('one.csv')
data = np.asarray(df.Temp)
print(data.shape)
step = int(data.shape[0] / n_clients)
X=[]
for c in range(n_clients):
    X.append(data[step * c: step * (c + 1)])
X = np.asarray(X)
key_length = 1024



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

    def decrypt_mean(self, mean_server):
        return self.privatekey.decrypt(mean_server)


keyring = paillier.PaillierPrivateKeyring()
elapsed_total=0
for i in range(10):
    start_time = time.process_time()
    public_key, private_key = paillier.generate_paillier_keypair(n_length=key_length)
    elapsed = (time.process_time()-start_time)*1000
    elapsed_total+=elapsed
print('Time Elapsed for Key Generation:', "{0:.4f}".format(elapsed_total/10), 'ms')

clients = []
for i in range(n_clients):
    clients.append(Client(X[i], public_key, private_key))

mean_server = 0
mean_clients = 0

elapsed_total=0
for c in clients:
    mean_server = mean_server + c.encrypt_mean()
    mean_clients = mean_clients + c.mean()

weights = np.random.randint(low=0, high=15, size=(n_clients,1))
weights_encrypted = []
for i in range(n_clients):
    w = int(weights[i,0])
    start_time = time.process_time()
    weights_encrypted.append(public_key.encrypt(w))
    elapsed = (time.process_time() - start_time) * 1000
    elapsed_total += elapsed
print('Time Elapsed for Encryption:', "{0:.4f}".format(elapsed_total/n_clients), 'ms')


convolve = 0
for c in clients:
    convolve += weights_encrypted[i]*c.mean()
mean_clients = mean_clients*(1/n_clients)
mean_server = mean_server*(1/n_clients)
start_time = time.process_time()
decrypted_mean = clients[0].decrypt_mean(mean_server)
elapsed = (time.process_time() - start_time) * 1000
print('Time Elapsed for Decryption:', "{0:.4f}".format(elapsed), 'ms')
decrypted_convolve = private_key.decrypt(convolve)
print(decrypted_convolve)
print(decrypted_mean)
print(mean_clients)

data=pickle.dumps(weights_encrypted)
data_load=pickle.loads(data)
print(data_load)
convolve=0
for c in clients:
    convolve += data_load[i]*c.mean()
decrypted_convolve = private_key.decrypt(convolve)
print(decrypted_convolve)
