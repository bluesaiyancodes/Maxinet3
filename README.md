MaxiNet - Distributed Software Defined Network Emulation
========================================================

Welcome to the MaxiNet repository.

For additional information please have a look at the [wiki](https://github.com/MaxiNet/MaxiNet/wiki).

# MaxiNet installation

Introduction:
MaxiNet is a distributed version of mininet where multiple mininet instances
running on different physical machines (called workers) are interconnected and used
to run large scale experiments. Using the MaxiNet API, specification of
experiments feels like setting up experiments in Mininet because MaxiNet
automatically maps the topology of the network to the workers and configures
them accordingly.

Warning:
MaxiNet allows to run command line commands with root permissions over a
network rpc connection as well as a seperate ssh server. Although authentication
measures are in place to prevent unauthorized access, it is strongly disadvised
to run MaxiNet on an untrusted or publicly accessible network.


Supported Operating Systems:
Debian 8
Ubuntu 14.04


## manual installation 

### Set Python3 as default
> sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 10
### 1. Install dependencies
> sudo apt-get install git autoconf screen cmake build-essential sysstat python-matplotlib uuid-runtime python3-pip

### 2. Install mininet 
> cd ~/Documents/
> git clone git://github.com/mininet/mininet
> sudo mininet/util/install.sh -a

### 3. Install metis
> cd ~/Documents/
> wget http://glaros.dtc.umn.edu/gkhome/fetch/sw/metis/metis-5.1.0.tar.gz
> tar -xzf metis-5.1.0.tar.gz
> rm metis-5.1.0.tar.gz
> cd metis-5.1.0
> make config
> make
> sudo make install

### 4. Install Pyro4
> pip3 install Pyro4

### 5. Download and install MaxiNet
> cd ~/Documents
> git clone https://github.com/bluesaiyancodes/Maxinet3.git
> cd MaxiNet
> git checkout 3.4
> sudo make install

### 6. Set up cluster and configure MaxiNet
Repeat above (1-5) steps for every pc you want to use as a worker or frontend.

On the frontend machine copy the MaxiNet-cfg-sample file to ~/.MaxiNet.cfg and edit the file.
> cp share/MaxiNet-cfg-sample ~/.MaxiNet.cfg
> vi ~/.MaxiNet.cfg

Please note that every worker connecting to the MaxiNet Server will need an respective
entry in the configuration file, named by its hostname and containing its ip.
Although MaxiNet tries to guess the IP of the worker if not found in the
configuration file this is nothing one should depend on.

Copy the ./MaxiNet.cfg file to all worker machines.


### 7. Start MaxiNet
On the frontend machine call
> sudo MaxiNetFrontendServer
On every worker machine call
> sudo MaxiNetWorker

You should see that the workers are connecting to the frontend.
Start an OpenFlow controller for example by calling
> cd ~/documents/pox/ && python3 pox.py forwarding.l2_learning

Now run in a new terminal,
> python3 /usr/local/share/MaxiNet/examples/simplePing.py
Congratulations, you just set up your own SDN!
