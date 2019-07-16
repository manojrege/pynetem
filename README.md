# pynetem

Running network based testing experiments require executing the application along with a network emulator in the background
in a highly controlled and repeatable manner. It is quite tedious to run the experiments and the network emulation as 
two separate processes. *pynetem* addresses this problem for Python based applications on MacOS.
 
*pynetem* is a simple Python wrapper library for network emulation on MacOS. It provides wrapper functions based on top of dummynet and packet filter which are the default tools
to emulate network link delay, bandwidth and packet loss on MacOS. 


Emulating a network link is as easy as applying a decorator to method.






