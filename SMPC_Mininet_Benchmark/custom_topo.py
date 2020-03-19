from mininet.topo import Topo

class smc_topo( Topo ):

    def __init__( self, num_nodes ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        cnode1 = self.addHost( 'cnode1' )
        cnode2 = self.addHost( 'cnode2' )

        # Connections to cnode1
        c1s = self.addSwitch( 'c1s' )
        # Connections to cnode2
        c2s = self.addSwitch( 'c2s' )

        # Add links
        self.addLink(c1s, c2s)
        self.addLink(c1s, cnode1)
        self.addLink(c2s, cnode2)


topos = { 'smc_topo': ( lambda: smc_topo() ) }
