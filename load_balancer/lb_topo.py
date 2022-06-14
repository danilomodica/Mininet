#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.term import makeTerm
from mininet.node import Node
from mininet.node import RemoteController
from mininet.log import setLogLevel, info
from mininet.cli import CLI


def treeTopo():
    net = Mininet( controller=RemoteController )
    
    info( '*** Adding controller\n' )
    net.addController('c0', port=6633)
    
    info( '*** Adding hosts\n' )
    h1 = net.addHost(name='h1', ip='10.0.0.1')
    h2 = net.addHost(name='h2', ip='10.0.0.2')
    h3 = net.addHost(name='h3', ip='10.0.0.3')          
    h4 = net.addHost(name='h4', ip='10.0.0.4')
    h5 = net.addHost(name='h5', ip='10.0.0.5')
    h6 = net.addHost(name='h6', ip='10.0.0.6')

    info( '*** Adding switches\n' )
    s1 = net.addSwitch( 's1' )
    
    info( '*** Creating links\n' )
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s1)
    net.addLink(h4, s1)
    net.addLink(h5, s1)
    net.addLink(h6, s1)
       
    info( '*** Starting network\n')
    net.start()
    
    info( '*** Running HTTP servers\n' )
    net.terms += makeTerm( net.get('h1'), cmd="bash -c 'python3 -m http.server 80;'")
    net.terms += makeTerm( net.get('h2'), cmd="bash -c 'python3 -m http.server 80;'")
    
    info( '*** Running CLI\n' )
    CLI( net )
    
    info( '*** Stopping network' )
    net.stop()
    

if __name__ == '__main__':
    setLogLevel( 'info' )
    treeTopo()

