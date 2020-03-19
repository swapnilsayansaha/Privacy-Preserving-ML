from mininet.topo import Topo

class smc_topo( Topo ):

    def __init__( self, num_nodes ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        inode1 = self.addHost( 'inode1' )
        inode2 = self.addHost( 'inode2' )
        inode3 = self.addHost( 'inode3' )

        cnode1 = self.addHost( 'cnode1' )
        cnode2 = self.addHost( 'cnode2' )
        cnode3 = self.addHost( 'cnode3' )

        # Connections to inode1
        i1s = self.addSwitch( 'i1s' )
        # Connections to inode2
        i2s = self.addSwitch( 'i2s' )
        # Connections to inode3
        i3s = self.addSwitch( 'i3s' )
        # Switch for inode 1,2,3
        s123 = self.addSwitch('s123')

        # Connections to cnode1
        c1s = self.addSwitch( 'c1s' )
        # Connections to cnode2
        c2s = self.addSwitch( 'c2s' )
        # Connections to cnode3
        c3s = self.addSwitch( 'c3s' )

        # Add links
        self.addLink(inode1, i1s)
        self.addLink(inode2, i2s)
        self.addLink(inode3, i3s)
        self.addLink(i1s, s123)
        self.addLink(i2s, s123)
        self.addLink(i3s, s123)
        self.addLink(s123, c1s)
        self.addLink(s123, c2s)
        self.addLink(s123, c3s)

        self.addLink(c1s, cnode1)
        self.addLink(c2s, cnode2)
        self.addLink(c3s, cnode3)


topos = { 'smc_topo': ( lambda: smc_topo() ) }
