from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink

class smc_topo( Topo ):

    def __init__( self, bandwidth, delay):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        cnode1 = self.addHost( 'cnode1' )
        cnode2 = self.addHost( 'cnode2' )

        # Connections to cnode1
        c1s = self.addSwitch( 'c1s')
        # Connections to cnode2
        c2s = self.addSwitch( 'c2s')

        # Add links
        self.addLink(c1s, c2s,  bw=bandwidth, delay=delay)
        self.addLink(c1s, cnode1,  bw=bandwidth, delay=delay)
        self.addLink(c2s, cnode2, bw=bandwidth, delay=delay)


def perfTest():

    topo = smc_topo(1, "1ms")
    net = Mininet(topo=topo, link=TCLink)
    net.start()
    net.pingAll()

    net.stop()


topos = { 'smc_topo': ( lambda: smc_topo() ) }

if __name__== '__main__':
    perfTest()
