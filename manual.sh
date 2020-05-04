#geth --datadir $DDR1 --password <(echo -n 1234) account new
#geth --datadir $DDR2 --password <(echo -n 1234) account new
#geth --datadir $DDR3 --password <(echo -n 1234) account new


geth --datadir=$DDR1 --networkid 714715 --port 30303 --nat extip:192.168.197.128 --netrestrict 192.168.197.0/24

ENODE_ADDRESS="enode://$(bootnode -nodekey $DDR1/geth/nodekey -writeaddress)@192.168.197.128:30303"
geth --datadir $DDR2 --networkid 714715 --port 30304 --nat extip:192.168.197.128 --netrestrict 192.168.197.0/24 --bootnodes $ENODE_ADDRESS --mine --minerthreads=1 --etherbase=0x2dec65f7f6fecef9088afed7ab41ad0f1173ddb4
geth --datadir $DDR3 --networkid 714715 --port 30305 --nat extip:192.168.197.128 --netrestrict 192.168.197.0/24 --bootnodes $ENODE_ADDRESS --mine --minerthreads=1 --etherbase=0x0213af577d12cf11a5baf5a869e0b1305684ca0a


eth.getBlock("latest")


h1 nohup geth --datadir=$DDR1 --networkid 714715 --port 30303 --nat extip:10.0.0.1 --netrestrict 10.0.0.0/24 > nohup1.out &

h2 ENODE_ADDRESS="enode://$(bootnode -nodekey $DDR1/geth/nodekey -writeaddress)@10.0.0.1:30303"
h3 ENODE_ADDRESS="enode://$(bootnode -nodekey $DDR1/geth/nodekey -writeaddress)@10.0.0.1:30303"

h2 nohup geth --datadir $DDR2 --networkid 714715 --port 30304 --nat extip:10.0.0.2 --netrestrict 10.0.0.0/24 --bootnodes $ENODE_ADDRESS --mine --minerthreads=1 --etherbase=0x2dec65f7f6fecef9088afed7ab41ad0f1173ddb4 > nohup2.out &
h3 nohup geth --datadir $DDR3 --networkid 714715 --port 30305 --nat extip:10.0.0.3 --netrestrict 10.0.0.0/24 --bootnodes $ENODE_ADDRESS --mine --minerthreads=1 --etherbase=0x0213af577d12cf11a5baf5a869e0b1305684ca0a > nohup3.out &

geth attach $DDR1/geth.ipc
geth attach $DDR2/geth.ipc
geth attach $DDR3/geth.ipc


#node_1_check_blocks = (f"{geth_bin_file} attach $DDR1/geth.ipc "
#                       f"--exec 'eth.getBlock(\"latest\")'")
#node_2_check_blocks = (f"{geth_bin_file} attach $DDR2/geth.ipc "
#                       f"--exec 'eth.getBlock(\"latest\")'")
#node_3_check_mine = (f"{geth_bin_file} attach $DDR3/geth.ipc "
#                     f"--exec 'web3.fromWei(eth.getBalance(eth.coinbase), \"ether\")'")
#node_4_check_mine = (f"{geth_bin_file} attach $DDR4/geth.ipc "
#                     f"--exec 'web3.fromWei(eth.getBalance(eth.coinbase), \"ether\")'")