# A command line tool for persisting messages on the Ethereum blockchain forever

## Prep Your System
`sudo apt update`  
`sudo apt-get install build-essential checkinstall`  
`sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev`

## Install Python 3.5 (unless you already have it)
`cd /usr/src`  
`wget https://www.python.org/ftp/python/3.5.6/Python-3.5.6.tgz`  
`sudo tar xzf Python-3.5.6.tgz`  
`cd Python-3.5.6`  
`sudo ./configure --enable-optimizations`  
`sudo make install`
`cd ~`

## Clone the repo
`git clone https://github.com/mkeen/ethmsg.git`  
`cd ethmsg`

## Build

`python3 setup.py sdist`

## Install

`sudo pip3 install dist/ethmsg-0.0.1.tar.gz`

## Use

Either set `ETH_MSG_PRIVATE_KEY` environment variable or prefix command. Either sign up for infura or set up local eth endpoint or use VPC. Load up an account with some ether and reference it with address arg (replace address below), or wait for prompt. Simple example:
  
`ETH_MSG_PRIVATE_KEY=_PRIV_KEY_HERE_ ethmsg --endpoint 'https://rinkeby.infura.io/v3/endpoint_id_here --message helloooo --address 0x2f516689075daC29608a34C80880f15b30A5B59F`
