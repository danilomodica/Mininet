# Internet & Multimedia Project
## Mininet/POX (Ubuntu 22.04)

### Requirements
- Mininet: http://mininet.org/download/
- POX controller: https://github.com/noxrepo/pox
- Python: https://www.python.org/

### Three basic applications:
Note: assume _pox_ folder is into the _home_ folder

1. **Load Balancer** <br>
Use POX controller as a load balancer. Follow these steps:
    - Open a terminal and move to the _load_balancer_ folder: 
    - Launch the Mininet topology with: 
      
      > sudo python3 lb_topo.py
    - Open a new terminal and launch the POX controller with: 
      
      > python3 /home/pox/pox.py log.level --DEBUG samples.pretty_log misc.ip_loadbalancer --ip=10.0.1.1 --servers=10.0.0.1,10.0.0.2
    - In the Mininet CLI run many times (replace X with the host number): 
      
      > hX curl 10.0.1.1
    - Watch the outputs/redirects on the POX terminal

2. **Firewall** <br>
Use POX controller as a network firewall. Follow these steps:
    - Copy the _firewall.py_ file into the _pox/pox/misc_ folder
    - Edit _firewall.py_ **rules** list, to set your firewall rules
    - Open a terminal and launch the POX controller with: 
      
      > python3 /home/pox/pox.py log.level --DEBUG samples.pretty_log misc.firewall
    - Open a new terminal and move to the _firewall_ folder
    - Launch the Mininet topology with: 
      
      > sudo python3 firewall_topo.py
    - In the Mininet CLI run: 
      
      > pingall
    - Watch the failed pings, according to the set firewall rules

3. **Routing** <br>
Use POX controller to forward traffic as a router. Follow these steps:
    - Open a terminal and launch the POX controller with: 
      
      > python3 home/pox/pox.py log.level --DEBUG samples.pretty_log forwarding.l2_pairs
    - Open a new terminal and move to the _routers_ folder
    - Launch the Mininet topology with: 
      
      > sudo python3 router_topo.py
    - In the Mininet CLI, run: 
      
      > pingall
      
      > h1 traceroute h2
    - In the Mininet CLI, simulate a network/link failure with:
      
      > link r1 r2 down
    - In the Mininet CLI, run again:
      
      > pingall
      
      > h1 traceroute h2
    - Watch the new routes, network is still working
