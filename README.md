# pynetem

Running network based testing experiments require executing the application along with a network emulator in the background
in a highly controlled and repeatable manner. It is quite tedious to run the experiments and the network emulation as 
two separate processes. *pynetem* addresses this problem for Python based applications on MacOS.
 
*pynetem* is a simple Python wrapper library for network emulation on MacOS. It provides wrapper functions based on top of dummynet and packet filter which are the default tools
to emulate network link delay, bandwidth and packet loss on MacOS. 


Emulating a network link is as easy as applying a decorator to method.

### Pip install


pip install pynetem


### Usage examples

Types of emulated links: Incoming, Outgoing, and Duplex

Example: Fetch a webpage with a emulated outgoing network link


###### Emulate incoming network link
```python
# Incoming:
# bandwidth = 3 Mbits/s
# delay = 100 ms
# packet loss percentage = 1 %

@emulate("incoming", bandwidth_in = 3, delay_in = 100, plr_in = 1)
def fetch_page():
    resp = req.get("http://www.google.de")
    return resp
```

###### Emulate outgoing network link

```python
# Outgoing:
# bandwidth = 10 Mbits/s
# delay = 100 ms
# packet loss percentage = 1 %

import requests as req

@emulate("outgoing", bandwidth_out = 10, delay_out = 100, plr_out = 1)
def fetch_page():
    resp = req.get("http://www.google.de")
    return resp
```

###### Emulate bidirectional network links 

```python
# Duplex:
# incoming bandwidth = 3 Mbits/s
# incoming delay = 15 ms
# incoming packet loss percentage = 1 %
# outgoing bandwidth = 1 Mbits/s
# outgoing delay = 10 ms
# outgoing packet loss percentage = 0.1 %
 
@emulate("duplex", bandwidth_in = 3, delay_in = 15, plr_in = 1,
          bandwidth_out = 1, delay_out = 10, plr_out = 0.1)
def fetch_page():
    resp = req.get("http://www.google.de")
    return resp
```