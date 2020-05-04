from mininet.topo import Topo
from v2_config import conf


def index_gen(prefix):
    i = 1
    while True:
        yield f"{prefix}{i}"
        i += 1


class SingleSwitchTopo(Topo):
    # A Single Switch Topology connected to k hosts

    def build(self, k):
        # k: number of hosts
        switch = self.addSwitch('s1')
        for h in range(k):
            host = self.addHost(f'h{(h + 1)}', **conf["node"])
            self.addLink(host, switch, **conf["link"])


class SingleSwitchTopoSlowH1(Topo):
    # A Single Switch Topology connected to k hosts

    def build(self, k, h1bw):
        # k: number of hosts
        switch = self.addSwitch('s1')

        host = self.addHost('h1', **conf["node"])
        self.addLink(host, switch, bw=h1bw)

        for h in range(1, k):
            host = self.addHost(f'h{(h + 1)}', **conf["node"])
            self.addLink(host, switch, **conf["link"])


class LinearTopo(Topo):
    # A Linear Topology of k switches, with n hosts per switch.

    def build(self, k=2, n=1, **_opts):
        """k: number of switches
           n: number of hosts per switch"""
        self.k = k
        self.n = n

        lastSwitch = None
        for i in range(1, k + 1):
            # Add switch
            switch = self.addSwitch('s%s' % i)
            # Add hosts to switch
            for j in range(1, n + 1):
                host = self.addHost(f'h{(i - 1) * n + j}', **conf["node"])
                self.addLink(host, switch, **conf["link"])
            # Connect switch to previous
            if lastSwitch:
                self.addLink(switch, lastSwitch, **conf["link"])
            lastSwitch = switch


class TreeTopo(Topo):
    # A Tree Topology.

    def build(self, depth=1, fanout=2):
        """depth: number of switches/nodes levels, except the root level
           fanout: how many switches/nodes are connect to a switch/node in the previous level
            number of hosts = fanout^depth
        """
        # Numbering:  h1..N, s1..M
        self.hostNum = 1
        self.switchNum = 1
        # Build topology
        self.addTree(depth, fanout)

    def addTree(self, depth, fanout):
        """Add a subtree starting with node n.
           returns: last node added"""
        isSwitch = depth > 0
        if isSwitch:
            node = self.addSwitch('s%s' % self.switchNum)
            self.switchNum += 1
            for _ in range(fanout):
                child = self.addTree(depth - 1, fanout)
                self.addLink(node, child, **conf["link"])
        else:
            node = self.addHost('h%s' % self.hostNum, **conf["node"])
            self.hostNum += 1
        return node


class FatTreeTopo(Topo):
    # A Fat Tree Topology:
    # 3 layers of switches: core, aggregate, edge
    # 1 layer of hosts under edge switches
    def build(self, c, a, e, h):
        """
        c: # of core switches
        a: # of aggregate switches, each connects to all core switches
        e: # of edge switches, each connects to all aggregate switches
        h: # of hosts PER edge switch
        """
        self.cores = []
        self.aggrs = []
        self.edges = []
        self.host_list = []
        self.sgen = index_gen("s")
        self.hgen = index_gen("h")
        for i in range(c):
            self.cores.append(self.addSwitch(next(self.sgen)))
        for i in range(a):
            self.aggrs.append(self.addSwitch(next(self.sgen), stp=True, failMode='standalone'))
        for i in range(e):
            self.edges.append(self.addSwitch(next(self.sgen), stp=True, failMode='standalone'))

        for core in self.cores:
            for aggr in self.aggrs:
                self.addLink(core, aggr, **conf["link"])

        for aggr in self.aggrs:
            for edge in self.edges:
                self.addLink(aggr, edge, **conf["link"])

        for edge in self.edges:
            for i in range(h):
                host = self.addHost(next(self.hgen), **conf["node"])
                self.host_list.append(host)
                self.addLink(edge, host, **conf["link"])


class FatTreeTopoSlow2Hosts(Topo):
    # A Fat Tree Topology:
    # 3 layers of switches: core, aggregate, edge
    # 1 layer of hosts under edge switches
    def build(self, c, a, e, h):
        """
        c: # of core switches
        a: # of aggregate switches, each connects to all core switches
        e: # of edge switches, each connects to all aggregate switches
        h: # of hosts PER edge switch
        """
        self.cores = []
        self.aggrs = []
        self.edges = []
        self.host_list = []
        self.sgen = index_gen("s")
        self.hgen = index_gen("h")
        for i in range(c):
            self.cores.append(self.addSwitch(next(self.sgen)))
        for i in range(a):
            self.aggrs.append(self.addSwitch(next(self.sgen), stp=True, failMode='standalone'))
        for i in range(e):
            self.edges.append(self.addSwitch(next(self.sgen), stp=True, failMode='standalone'))

        for core in self.cores:
            for aggr in self.aggrs:
                self.addLink(core, aggr, **conf["link"])

        for aggr in self.aggrs:
            for edge in self.edges:
                self.addLink(aggr, edge, **conf["link"])

        for edge in self.edges[:2]:
            for i in range(h):
                host = self.addHost(next(self.hgen), **conf["nodeh1h2"])
                self.host_list.append(host)
                self.addLink(edge, host, **conf["linkh1h2"])
        for edge in self.edges[2:]:
            for i in range(h):
                host = self.addHost(next(self.hgen), **conf["node"])
                self.host_list.append(host)
                self.addLink(edge, host, **conf["link"])
