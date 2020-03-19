import socket, optparse

# Read from the file to get comp node IPs
def read_comp_nodes(myIP):
    comp_ips = []
    f = open('comp_ips.txt', 'r')
    for line in f.readlines():
        current_comp_ip = line.strip()

        if myIP != current_comp_ip:
            comp_ips.append(line.strip())
    f.close()

    return comp_ips

# Basically if we recieve from another computation node,
#  we want the computation to stop here.
#  This just determines if the recieved IP is a computation
#  node or not.
def isComp(addr, comp_ips):
    isComp = False
    if addr[0] in comp_ips:
        isComp = True
    return isComp

# Parse options that we want - basically we want information
# about the ip and port numbers, as well as which compnode this is,
#  so that we can have an output file for each one.
parser = optparse.OptionParser()
parser.add_option('-n', dest='num', default='')
parser.add_option('-i', dest='ip', default='')
parser.add_option('-p', dest='port', type='int', default=12345)
(options, args) = parser.parse_args()
print('setting up listeners on ' + str(options.ip))
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind( (options.ip, options.port) )

# Open a file for writing to a log
f = open('log' + options.num + '.txt','w+')
comp_ips =read_comp_nodes(options.ip)

# Computation node will open and wait for input
#  All it does is write whatever it receives to the file.
#  If it receives input from an input node, it will say hello
#  to another computation node
#  Otherwise, if it recieves from a computation node it
#  will write to file.
while True:
  data, addr = s.recvfrom(512)
  data = data.decode()
  print('hello we have received data')
  f.write("%s: %s\n" % (addr, data))

  # If this is a compute node, we stop here
  if isComp(addr, comp_ips):
      f.write("recv from comp\n")
  else: # Otherwise we send a share to all other compute nodes
      for ip in comp_ips:
          s.sendto('hello from comp', (ip, options.port) )
  f.flush()
