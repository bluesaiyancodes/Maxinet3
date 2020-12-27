MaxiNet - Distributed Software Defined Network Emulation
========================================================

Welcome to the MaxiNet repository.

For additional information please have a look at the [wiki](https://github.com/MaxiNet/MaxiNet/wiki).

# Installation
Install dependencies
> sudo apt-get install git autoconf screen cmake build-essential sysstat python-matplotlib uuid-runtime python-pip


### Install containernet and OpenVSwitch
> 1. git clone https://github.com/containernet/containernet.git
> 2. sudo apt-get install ansible git aptitude
> 3. cd containernet/ansible
> 4. sudo ansible-playbook -i "localhost," -c local install.yml
> 5. cd .. && sudo make install

### Install metis
> 1. wget http://glaros.dtc.umn.edu/gkhome/fetch/sw/metis/metis-5.1.0.tar.gz
> 2. tar -xzf metis-5.1.0.tar.gz
> 3. rm metis-5.1.0.tar.gz
> 4. cd metis-5.1.0
> 5. make config
> 6. make
> 7. sudo make install

### Install Pyro4
> sudo pip install Pyro4

### Download and install MaxiNet
> 1. git clone https://github.com/bluesaiyancodes/Maxinet3.git
> 2. cd MaxiNet
> 3. sudo make install

Set up clusr and configure MaxiNet
Repeat above (1-5) steps for every pc you want to use as a worker or frontend.

On the frontend machine copy the MaxiNet-cfg-sample file to ~/.MaxiNet.cfg and edit the file.
> cp share/MaxiNet-cfg-sample ~/.MaxiNet.cfg
> vi ~/.MaxiNet.cfg

Please note that every worker connecting to the MaxiNet Server will need an respective
entry in the configuration file, named by its hostname and containing its ip.
Although MaxiNet tries to guess the IP of the worker if not found in the
configuration file this is nothing one should depend on.

Copy the ./MaxiNet.cfg file to all worker machines.

Start MaxiNet
On the frontend machine call
> sudo MaxiNetFrontendServer
On every worker machine call
> sudo MaxiNetWorker
