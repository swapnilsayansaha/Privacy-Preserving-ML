import phe as paillier
import numpy as np
import time
start_time_key = time.process_time()
for i in range(100):
    public_key, private_key = paillier.generate_paillier_keypair(n_length=1024)
time_keygen = time.process_time()-start_time_key
print("Time for key generation:", time_keygen/100000, " ms")
elapsed_total_add = 0
elapsed_total_mult_encr = 0
elapsed_total_add_encr = 0
elapsed_total_mult = 0
for i in range(100):
    a = np.random.randint(0, high=256)
    b = np.random.randint(0, high=256)
    encrypted_a = public_key.encrypt(a)
    encrypted_b = public_key.encrypt(b)
    start_time = time.process_time()
    for j in range(100):
        adder = a + b
    elapsed = (time.process_time() - start_time)*100000
    elapsed_total_add += elapsed
    start_time_mult = time.process_time()
    for j in range(100):
        mult = a * b
    elapsed = (time.process_time() - start_time_mult)*100000
    elapsed_total_mult += elapsed
    start_time = time.process_time()
    for j in range(100):
        adder = encrypted_a + encrypted_b
    elapsed = (time.process_time() - start_time) * 100000
    elapsed_total_add_encr += elapsed
    start_time_mult = time.process_time()
    for j in range(100):
        mult = encrypted_a * b
    elapsed = (time.process_time() - start_time_mult) * 100000
    elapsed_total_mult_encr += elapsed
print('Time Elapsed for add:', "{0:.6f}".format((elapsed_total_add)), 'ns')
print('Time Elapsed for multiply:', "{0:.6f}".format(elapsed_total_mult), 'ns')
print('Time Elapsed for encrypted add:', "{0:.6f}".format((elapsed_total_add_encr)), 'ns')
print('Time Elapsed for encrypted multiply:', "{0:.6f}".format(elapsed_total_mult_encr), 'ns')
