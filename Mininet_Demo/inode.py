import socket, optparse


# Important note - these parameters identify a computation node
#  they are not ip/ports of the input node
parser = optparse.OptionParser()
parser.add_option('-i', dest='ip', default='127.0.0.1')
parser.add_option('-p', dest='port', type='int', default=12345)
parser.add_option('-m', dest='msg')
(options, args) = parser.parse_args()

# This just transmits a message to a computation identified
# by the ip and port as parameters to this program.
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto(options.msg.encode(), (options.ip, options.port) )
print('hello sent data')
