import phe as paillier
import numpy as np
import time
import pickle
public_key, private_key = paillier.generate_paillier_keypair(n_length=1024)
# pickle.dump( public_key, open( "public_key.p", "wb" ) )
# pickle.dump( private_key, open( "private_key.p", "wb" ) )
# public_key = pickle.load( open( "public_key.p", "rb" ) )
# private_key = pickle.load(open( "private_key.p", "rb" ))
elapsed_total_add = 0
elapsed_total_mult = 0
for i in range(100):
    a = np.random.randint(0, high=256)
    b = np.random.randint(0, high=256)
    encrypted_a = public_key.encrypt(a)
    encrypted_b = public_key.encrypt(b)
    start_time = time.process_time()
    for j in range(10000):
        adder = a+b
    elapsed = (time.process_time() - start_time)*1000
    elapsed_total_add += elapsed
    start_time_mult = time.process_time()
    for j in range(10000):
        mult = a * b
    elapsed = (time.process_time() - start_time_mult)*1000
    elapsed_total_mult += elapsed
print('Time Elapsed for add:', "{0:.6f}".format((elapsed_total_add)), 'ns')
print('Time Elapsed for multiply:', "{0:.6f}".format(elapsed_total_mult), 'ns')
