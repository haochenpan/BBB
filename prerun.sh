#!/usr/bin/env bash

#rm -rf $DDR1 $DDR2 $DDR3 $DDR4 ~/nw3/mngeth/data/*
rm -rf $DDR1 $DDR2 $DDR3 $DDR4 $DDR5 ~/nw3/mngeth/data/*
mkdir -p ~/ethData1/keystore
mkdir -p ~/ethData2/keystore
mkdir -p ~/ethData3/keystore
mkdir -p ~/ethData4/keystore
mkdir -p ~/ethData5/keystore
source ~/.bashrc
cp ~/nw3/mngeth/keys/UTC--2020-03-07T23-25-18.301273092Z--67e37abe6fb7bb2b0d61b9c6f53c71623ae65551 $DDR1/keystore
cp ~/nw3/mngeth/keys/UTC--2020-03-07T23-27-12.170957487Z--2dec65f7f6fecef9088afed7ab41ad0f1173ddb4 $DDR2/keystore
cp ~/nw3/mngeth/keys/UTC--2020-03-07T23-27-53.050585459Z--0213af577d12cf11a5baf5a869e0b1305684ca0a $DDR3/keystore
cp ~/nw3/mngeth/keys/UTC--2020-03-16T21-29-01.688713168Z--7d8466475a66c4363da52494af4a3c20298f5f73 $DDR4/keystore
# no need to copy the key for host5, host6, ...
geth init --datadir $DDR1 ~/nw3/mngeth/genesis.json
geth init --datadir $DDR2 ~/nw3/mngeth/genesis.json
geth init --datadir $DDR3 ~/nw3/mngeth/genesis.json
geth init --datadir $DDR4 ~/nw3/mngeth/genesis.json
geth init --datadir $DDR5 ~/nw3/mngeth/genesis.json
