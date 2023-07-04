#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.node import RemoteController
from mininet.log import setLogLevel, info
from mininet.cli import CLI


# Enable IP forwarding to use a host as a router
class LinuxRouter(Node):
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()


class NetworkTopo(Topo):
    def build(self, **_opts):
        # Add 4 routers in four different subnets
        r1 = self.addHost('r1', cls=LinuxRouter, ip='10.0.0.1/24')
        r2 = self.addHost('r2', cls=LinuxRouter, ip='10.1.0.1/24')
        r3 = self.addHost('r3', cls=LinuxRouter, ip='10.2.0.1/24')
        r4 = self.addHost('r4', cls=LinuxRouter, ip='10.3.0.1/24')

        # Add 4 switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')     

        # Add host-switch links in the relative same subnet
        self.addLink(s1,
                     r1,
                     intfName2='r1-eth1',
                     params2={'ip': '10.0.0.1/24'})

        self.addLink(s2,
                     r2,
                     intfName2='r2-eth1',
                     params2={'ip': '10.1.0.1/24'})

        self.addLink(s3,
                     r3,
                     intfName2='r3-eth1',
                     params2={'ip': '10.2.0.1/24'})

        self.addLink(s4,
                     r4,
                     intfName2='r4-eth1',
                     params2={'ip': '10.3.0.1/24'})

        # Add router-router links in new subnets for the router-router connections
        self.addLink(r1,
                     r2,
                     intfName1='r1-eth2',
                     intfName2='r2-eth2',
                     params1={'ip': '10.100.0.1/24'},
                     params2={'ip': '10.100.0.2/24'})
        
        self.addLink(r1,
                     r3,
                     intfName1='r1-eth3',
                     intfName2='r3-eth2',
                     params1={'ip': '10.101.0.1/24'},
                     params2={'ip': '10.101.0.2/24'})
        
        self.addLink(r3,
                     r4,
                     intfName1='r3-eth3',
                     intfName2='r4-eth2',
                     params1={'ip': '10.102.0.1/24'},
                     params2={'ip': '10.102.0.2/24'})
        
        self.addLink(r2,
                     r4,
                     intfName1='r2-eth3',
                     intfName2='r4-eth3',
                     params1={'ip': '10.103.0.1/24'},
                     params2={'ip': '10.103.0.2/24'})

        # Adding hosts, specifying the default route
        h1 = self.addHost(name='h1',
                          ip='10.0.0.10/24',
                          defaultRoute='via 10.0.0.1')
        h2 = self.addHost(name='h2',
                          ip='10.1.0.10/24',
                          defaultRoute='via 10.1.0.1')
        
        h3 = self.addHost(name='h3',
                          ip='10.2.0.10/24',
                          defaultRoute='via 10.2.0.1')
                          
        h4 = self.addHost(name='h4',
                          ip='10.3.0.10/24',
                          defaultRoute='via 10.3.0.1')

        # Add host-switch links
        self.addLink(h1, s1)
        self.addLink(h2, s2)
        self.addLink(h3, s3)
        self.addLink(h4, s4)
        

def run():
    topo = NetworkTopo()
    net = Mininet(topo=topo, controller=RemoteController)

    # Add routes for reaching networks that aren't directly connected: "metric" specifies the priority
    info(net['r1'].cmd("ip route add 10.1.0.0/24 via 10.100.0.2 dev r1-eth2 metric 100"))
    info(net['r1'].cmd("ip route add 10.1.0.0/24 via 10.101.0.2 dev r1-eth3 metric 200"))
    info(net['r1'].cmd("ip route add 10.2.0.0/24 via 10.101.0.2 dev r1-eth3"))
    info(net['r1'].cmd("ip route add 10.3.0.0/24 via 10.101.0.2 dev r1-eth3 metric 100"))
    info(net['r1'].cmd("ip route add 10.3.0.0/24 via 10.100.0.2 dev r1-eth2 metric 200"))
    info(net['r1'].cmd("ip route add 10.102.0.0/24 via 10.101.0.2 dev r1-eth3"))
    info(net['r1'].cmd("ip route add 10.103.0.0/24 via 10.100.0.2 dev r1-eth2 metric 100"))
    info(net['r1'].cmd("ip route add 10.103.0.0/24 via 10.101.0.2 dev r1-eth3 metric 200"))
    
    info(net['r2'].cmd("ip route add 10.0.0.0/24 via 10.100.0.1 dev r2-eth2 metric 100"))
    info(net['r2'].cmd("ip route add 10.0.0.0/24 via 10.103.0.2 dev r2-eth3 metric 200"))
    info(net['r2'].cmd("ip route add 10.3.0.0/24 via 10.103.0.2 dev r2-eth3"))
    info(net['r2'].cmd("ip route add 10.2.0.0/24 via 10.103.0.2 dev r2-eth3 metric 100"))
    info(net['r2'].cmd("ip route add 10.2.0.0/24 via 10.100.0.1 dev r2-eth2 metric 200"))
    info(net['r2'].cmd("ip route add 10.102.0.0/24 via 10.103.0.2 dev r2-eth3"))
    info(net['r2'].cmd("ip route add 10.101.0.0/24 via 10.100.0.1 dev r2-eth2 metric 100"))
    info(net['r2'].cmd("ip route add 10.101.0.0/24 via 10.103.0.2 dev r2-eth3 metric 200"))
    
    info(net['r3'].cmd("ip route add 10.0.0.0/24 via 10.101.0.1 dev r3-eth2"))
    info(net['r3'].cmd("ip route add 10.3.0.0/24 via 10.102.0.2 dev r3-eth3 metric 100"))
    info(net['r3'].cmd("ip route add 10.3.0.0/24 via 10.101.0.1 dev r3-eth2 metric 200"))
    info(net['r3'].cmd("ip route add 10.1.0.0/24 via 10.102.0.2 dev r3-eth3 metric 100"))
    info(net['r3'].cmd("ip route add 10.1.0.0/24 via 10.101.0.1 dev r3-eth2 metric 200"))
    info(net['r3'].cmd("ip route add 10.103.0.0/24 via 10.102.0.2 dev r3-eth3 metric 100"))
    info(net['r3'].cmd("ip route add 10.103.0.0/24 via 10.101.0.1 dev r3-eth2 metric 200"))
    info(net['r3'].cmd("ip route add 10.100.0.0/24 via 10.101.0.1 dev r3-eth2 metric 100"))
    info(net['r3'].cmd("ip route add 10.100.0.0/24 via 10.102.0.2 dev r3-eth3 metric 200"))

    
    info(net['r4'].cmd("ip route add 10.1.0.0/24 via 10.103.0.1 dev r4-eth3 metric 100"))
    info(net['r4'].cmd("ip route add 10.1.0.0/24 via 10.102.0.1 dev r4-eth2 metric 200"))
    info(net['r4'].cmd("ip route add 10.2.0.0/24 via 10.102.0.1 dev r4-eth2 metric 100"))    
    info(net['r4'].cmd("ip route add 10.2.0.0/24 via 10.103.0.1 dev r4-eth3 metric 200")) 
    info(net['r4'].cmd("ip route add 10.0.0.0/24 via 10.102.0.1 dev r4-eth2 metric 100"))
    info(net['r4'].cmd("ip route add 10.0.0.0/24 via 10.103.0.1 dev r4-eth3 metric 200"))
    info(net['r4'].cmd("ip route add 10.101.0.0/24 via 10.102.0.1 dev r4-eth2 metric 100"))
    info(net['r4'].cmd("ip route add 10.101.0.0/24 via 10.103.0.1 dev r4-eth3 metric 200"))
    info(net['r4'].cmd("ip route add 10.103.0.0/24 via 10.103.0.1 dev r4-eth3"))
    info(net['r3'].cmd("ip route add 10.100.0.0/24 via 10.102.0.1 dev r4-eth2 metric 100"))
    info(net['r3'].cmd("ip route add 10.100.0.0/24 via 10.103.0.1 dev r4-eth3 metric 200"))

    net.start()
    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run()
 
