from pprint import pprint
import re
from sys import argv
import datetime

num_of_miners = int(argv[1])


def read_file(file):
    with open(file) as f:
        return f.readlines()


def find_max_valid_block(raw_logs):
    num = 0
    for raw_log in raw_logs:
        for line in raw_log[::-1]:
            if "🔗 block reached canonical chain " in line:
                cnum = int(line.split()[-2].split("=")[-1])
                if cnum > num:
                    num = cnum
    if num == 0:
        raise Exception("not block has reached the canonical chain")
    else:
        return num


def extract_time(time_raw="[04-11|14:39:58.449]"):
    time_arr = re.split("[\[Srw\-|:.\]]", time_raw)[1:-1]
    time_arr = [int(i) for i in time_arr]
    time_arr[-1] = time_arr[-1] * 1000
    assert len(time_arr) == 6
    time_dt = datetime.datetime(2020, *time_arr)
    return time_dt.timestamp()


def extract_history(nodes, raw_logs, max_valid_block_num):
    histories = []
    for block_num in range(max_valid_block_num):
        histories.append([])
        for node_num, raw_log in enumerate(raw_logs):
            for line in raw_log:
                if f" number={block_num} " in line:
                    histories[block_num].append(nodes[node_num] + "\t" + line.strip())
    for i in range(max_valid_block_num):
        histories[i] = sorted(histories[i], key=lambda s: s.split()[2] + s.split()[0])
    return histories


def print_block_hist_info(histories, info_arr, num):
    print()
    print()
    print("block number = ", num)
    print("total log entries = ", len(histories[num]))
    print(info_arr[num])
    print()
    for line in histories[num]:
        print(line)


def extract_info(histories, max_valid_block_num):
    info_arr = []
    for num in range(max_valid_block_num):
        info = {"num": num}

        for line in histories[num][::-1]:
            if "🔗 block reached canonical chain " in line:
                info["hash"] = line.split()[-1].split()[-1]
                info["sender_recv_time"] = extract_time(line.split()[2])
                break

        for line in histories[num]:
            if "🔨 mined potential block " in line and info["hash"] in line:
                info["sender"] = line.split()[0]
                info["sender_send_time"] = extract_time(line.split()[2])
                break

        if len(list(info.keys())) == 5:
            info["valid"] = True
        else:
            info["valid"] = False
        info_arr.append(info)

    return info_arr


def calculate_metrics(nodes, info_arr):
    pass
    # definitions
    # sender_send_time: the system time that a miner reports it has mined a potential block
    # sender_recv_time: the system time that a miner reports its block has reached the canonical chain

    # a valid block: a block that has the above time recorded in logs

    # when two miners produce their i-th blocks at around the same time,
    # only one miner reports its block (say, with hash A) has reached the canonical chain
    # so sender_send_time, sender_recv_time are all related to the block with hash A
    # (so another miner's send time is ignored in this version)

    # this method calculates & returns
    # 1) miner i's throughput: a float, equals to
    # the total # of blocks that 1) considered valid and 2) sent by miner i
    # 2) miner i's latencies: an array of floats,
    # i-th element stores (sender_recv_time - sender_send_time) of i-th block that satisfies 1) and 2)

    # 3) system throughput: a float, equals to
    # the total # of valid blocks / ((last valid block's sender_recv_time) - (first valid block's sender_send_time))
    # 4) system latencies: an array of floats,
    # i-th element stores i-th valid block's sender_recv_time - sender_send_time

    first_valid, last_valid = None, None
    total_valid_count = 0
    for info in info_arr:
        if info["valid"]:
            total_valid_count += 1
            if first_valid is None:
                first_valid = info
            last_valid = info
    assert first_valid is not None
    assert last_valid is not None
    # print(first_valid)
    # print(last_valid)
    runtime = last_valid['sender_recv_time'] - first_valid['sender_send_time']
    sys_tho = total_valid_count / (last_valid['sender_recv_time'] - first_valid['sender_send_time'])
    # 0th entry: system tho
    # 1st entry: minier 1's tho
    # 2nd entry: minier 2's tho
    # 3rd entry: minier 3's tho
    # ...
    throughputs = [sys_tho]
    for miner in nodes:
        # print(miner)
        miner_first_valid, miner_last_valid = None, None
        miner_valid_count = 0
        for info in info_arr:
            if info["valid"] and info["sender"] == miner:
                miner_valid_count += 1
                if miner_first_valid is None:
                    miner_first_valid = info
                miner_last_valid = info
        if miner_first_valid is not None:
            miner_tho = miner_valid_count / (last_valid['sender_recv_time'] - first_valid['sender_send_time'])
        else:
            miner_tho = 0
        throughputs.append(miner_tho)
    # print(throughputs)

    cros_lat = []
    for info in info_arr:
        if info["valid"]:
            cros_lat.append(info['sender_recv_time'] - info['sender_send_time'])

    latencies = [cros_lat]
    for miner in nodes:
        miner_lat = []
        for info in info_arr:
            if info["valid"] and info["sender"] == miner:
                miner_lat.append(info['sender_recv_time'] - info['sender_send_time'])
        latencies.append(miner_lat)

    return runtime, total_valid_count, throughputs, latencies


def report_metrics(nodes, rt, total_valid_count, throughputs, latencies):
    pass
    print("*****report*****")
    print("[overall]\t", "runtime\t", round(rt, 2), "(sec)")
    print("[overall]\t", "total_valid\t", total_valid_count, "(blocks)")

    tho = throughputs[0]
    lat = latencies[0]
    print("[overall]\t", "throughput\t", round(tho, 2), "(blocks/sec)")
    print("[overall]\t", "latency", "average", round(sum(lat) / len(lat), 2), "(sec)")
    print("[overall]\t", "latency", "median\t", round(sorted(lat)[int(len(lat) * 0.5)], 2), "(sec)")
    print("[overall]\t", "latency", "95th\t", round(sorted(lat)[int(len(lat) * 0.95)], 2), "(sec)")

    for i, node in enumerate(nodes):
        tho = throughputs[i + 1]
        print(f"[{nodes[i]}]\t", "throughput\t", round(tho, 2), "(blocks/sec)")
        lat = latencies[i + 1]
        if len(lat) != 0:
            print(f"[{nodes[i]}]\t", "latency", "average", round(sum(lat) / len(lat), 2), "(sec)")
            print(f"[{nodes[i]}]\t", "latency", "median\t", round(sorted(lat)[int(len(lat) * 0.5)], 2), "(sec)")
            print(f"[{nodes[i]}]\t", "latency", "95th\t", round(sorted(lat)[int(len(lat) * 0.95)], 2), "(sec)")
        else:
            print(f"[{nodes[i]}]\t", "latency", "average", 0, "(sec)")
            print(f"[{nodes[i]}]\t", "latency", "median\t", 0, "(sec)")
            print(f"[{nodes[i]}]\t", "latency", "95th\t", 0, "(sec)")
    print("*****end of the report*****")


def main():
    # all nodes are miners
    nodes = [f"10.0.0.{i}" for i in range(1, num_of_miners + 1)]
    raw_logs = [read_file(f"./data/nohup-{i}.out") for i in nodes]
    max_valid_block_num = find_max_valid_block(raw_logs) + 1
    histories = extract_history(nodes, raw_logs, max_valid_block_num)
    info_arr = extract_info(histories, max_valid_block_num)

    # print(nodes)
    # print("len(histories) = ", len(histories))
    # print("len(info_arr) = ", len(info_arr))

    # print_block_hist_info(histories, info_arr, 0)
    # print_block_hist_info(histories, info_arr, 1)
    # print_block_hist_info(histories, info_arr, 2)
    rt, twc, tho, lat = calculate_metrics(nodes, info_arr)
    report_metrics(nodes, rt, twc, tho, lat)


main()
