import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

'''
Replace your path to a datafile of parsed raw measurement data
'''

class Hop():
    def __init__(self, idx, AS, ip, rtts, CC=None):
        self.idx = idx
        self.AS = AS
        self.CC = CC
        if rtts == 'null' or rtts is None:
            self.probes = [0]
        else:
            self.probes = [float(r) for r in rtts]

class MeasurementProfile():
    def __init__(self, hops, dst_ip, src_ip, dst_as, src_as):
        self.dst_ip = dst_ip
        if src_as is None:
            self.src_as = 0
        else:
            self.src_as = src_as
        self.dst_as = dst_as
        self.src_ip = src_ip
        self.hops = hops
        self.last_rtt = np.median(self.hops[-1].probes)

def make_profile(data):
    if 'results' not in data or len(data['results']) == 0 :
        return None
    if len(data) == 0:
        return None

    hops = data['results']
    c_hops = [None] * len(hops)
    for idx, hop in hops.items():
        if 'cc' in hop:
            c_hops.append(Hop(int(idx), hop['as'], hop['ip'], hop['rtts'], CC=hop['cc']))
        else:
            c_hops.append(Hop(int(idx), hop['as'], hop['ip'], hop['rtts']))
    return MeasurementProfile(c_hops, data['dstIP'], data['srcIP'], data['dstAS'], data['srcAS'])

def main():
    profile_file = '/home/max/codeZ/mlab/vantage/data.txt'

    profiles = []
    jsons = []
    with open(profile_file, 'r') as f:
        for line in f:
            f_json = json.loads(line)
            profiles.append(make_profile(f_json))

    print len(profiles)

    dst = {}
    for p in profiles:
        if p is None:
            continue
        if p.src_as not in dst:
            dst[p.src_as] = [p.dst_as]
        else:
            dst[p.src_as].append(p.dst_as)

    #Get an histogram from source as to dst as with number of paths
    x = range(0, len(dst.keys()) - 1)
    y = sorted(map(lambda x: len(x), dst.values()))[:-1]

    ax = plt.gca()
    ax.hist(x, y, facecolor='green', alpha=0.75)
    ax.set_ylabel('Number of paths to remote AS')
    ax.set_xlabel('AS ID')
    ax.set_xlim([0, 50])
    plt.show()

if __name__ == '__main__':
    main()
