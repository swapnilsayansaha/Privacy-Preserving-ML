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

        anode1 = self.addHost( 'anode1' )
        qnode1 = self.addHost( 'qnode1' )

        # Connections to inode1
        i1s = self.addSwitch( 'i1s' )
        # Connections to inode2
        i2s = self.addSwitch( 'i2s' )
        # Connections to inode3
        i3s = self.addSwitch( 'i3s' )
        # Switch for inode 1,2,3
        s123 = self.addSwitch('s123')

        # Connections to cnode1
        a1s = self.addSwitch( 'a1s' )
        # Connections to qnode1
        q1s = self.addSwitch( 'q1s' )

        # Add links
        # Links from inodes to switches
        self.addLink(inode1, i1s)
        self.addLink(inode2, i2s)
        self.addLink(inode3, i3s)

        # Links from inodes switches to central switch and to queryer/aggregator
        self.addLink(i1s, s123)
        self.addLink(i2s, s123)
        self.addLink(i3s, s123)
        self.addLink(s123, a1s)
        self.addLink(s123, q1s)
        # Links from query/agg nodes to switches
        self.addLink(a1s, anode1)
        self.addLink(q1s, qnode1)


topos = { 'smc_topo': ( lambda: smc_topo() ) }
