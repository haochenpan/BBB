import yaml
import pprint

conf = yaml.load(open("./v2/v2_config.yaml"))["network"]


def process():
    if "topo" not in conf:
        conf["topo"] = {"class": "SingleSwitchTopo", "args": [4]}
    if "link" not in conf:
        conf["link"] = {"bw": None}
    if "node" not in conf:
        conf["node"] = {'cores': None, 'cpu': -1}
    if "test" not in conf:
        conf["test"] = {'iperf': -1}

    if "args" not in conf["topo"]:
        conf["topo"]["args"] = []
    if "kwargs" not in conf["topo"]:
        conf["topo"]["kwargs"] = {}

    assert conf["test"]['iperf'] in [-1, 0, 1]


process()
pprint.pprint(conf)
