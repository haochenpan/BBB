from sys import argv

num_of_miners = int(argv[1])
miner_thread = 3
network_id = 714715
port = 30303

nodes = [f"10.0.0.{i}" for i in range(1, num_of_miners + 1)]
b1 = "0x67e37abe6fb7bb2b0d61b9c6f53c71623ae65551"
b2 = "0x2dec65f7f6fecef9088afed7ab41ad0f1173ddb4"
b3 = "0x0213af577d12cf11a5baf5a869e0b1305684ca0a"
b4 = "0x7d8466475a66c4363da52494af4a3c20298f5f73"
bases = [b1, b2, b3, b4]

gen_enode = (f"ENODE_ADDRESS=\"enode://$(bootnode -nodekey $DDR1/geth/nodekey -writeaddress)"
             f"@{nodes[0]}:{port}\"")

node_1_start = (
    f"nohup geth --datadir=$DDR1 --networkid {network_id} --port {port} "
    f"--nat extip:{nodes[0]} --netrestrict 10.0.0.0/24 "
    f"--mine --minerthreads={miner_thread} --etherbase={bases[0]} "
    f"> ~/nw3/mngeth/data/nohup-{nodes[0]}.out &")
node_n_start = (
    "nohup geth --datadir $DDR{n} --networkid {networkid} --port {port} "
    "--nat extip:{ip} --netrestrict 10.0.0.0/24 "
    "--bootnodes $ENODE_ADDRESS "
    f"--mine --minerthreads={miner_thread} "
    "--etherbase={etherbase} "
    "> ~/nw3/mngeth/data/nohup-{ip}.out &")
node_n_check_join = "geth attach $DDR{}/geth.ipc --exec admin.peers"

node_1_check_blocks = (f"geth attach $DDR1/geth.ipc "
                       f"--exec 'eth.getBlock(\"latest\")' > ~/nw3/mngeth/data/nohup-node_1_block.out")


def read_get_block(file="./data/nohup-node_1_block.out"):
    with open(file) as f:
        for line in f.readlines():
            if "number" in line:
                # print(line)
                num = line.strip().split(":")[-1][:-1]
                return int(num)
        raise Exception("no 'number' field found error")
        # data = json.load(f)
        # print(data["difficulty"], data["number"])

# change gas limit
# change topology
