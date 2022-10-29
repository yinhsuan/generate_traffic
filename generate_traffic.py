import subprocess as sp
import numpy as np
from scipy.stats import truncnorm
import argparse

from distribution import normal_distribution
from distribution import truncated_normal_distribution
from distribution import exponential_distribution
from distribution import log_normal_distribution
from distribution import weibull_distribution
from distribution import pareto_distribution
from distribution import poisson_distribution
from distribution import uniform_distribution

from traffic import *

from params import NUM_OF_PODS
from params import NUM_OF_RACKS_PER_POD
from params import MIN_RACK_NUM
from params import MAX_RACK_NUM
from params import MIN_SERVER_ID
from params import MAX_SERVER_ID
from params import MIN_SERVER_NUM
from params import MAX_SERVER_NUM
from params import START_PORT

# Fixed
def get_traffics_from_file(traffic_file):
    traffics = list()

    fileLine = open(traffic_file,'r').read().splitlines()
    while("" in fileLine):
        fileLine.remove("")

    for line in fileLine:
        parsed_argv = line.split(" ")
        traffics.append(Traffic(parsed_argv[0], parsed_argv[1], parsed_argv[2], 
                                parsed_argv[3], parsed_argv[4], parsed_argv[5], parsed_argv[6]))
    return traffics

# Locality & Whole
def create_traffic(src_server_ip, dst_server_ip, port, protocol, load, duration, iperf_version):
    return Traffic(src_server_ip, dst_server_ip, port, protocol, load, duration, iperf_version)
    
def get_load(mean, std):
    low_bound = 0
    high_bound = 10
    return int(truncated_normal_distribution(low_bound, high_bound, mean, std))

def get_duration(mean, std):
    return int(normal_distribution(mean, std))

def rack_to_server_ip(rack, server_num):
    if 1 <= rack and rack <= 5:
        pod_num = 1
        rack_num = rack
    elif 6 <= rack and rack <= 10:
        pod_num = 2
        rack_num = rack - 5
    elif 11 <= rack and rack <= 15:
        pod_num = 3
        rack_num = rack - 10
    else:
        print("Wrong Rack# !!!!")
    return "10.{pod}.{rack}.{server}".format(pod=pod_num, rack=rack_num, server=server_num)

def get_traffics(src_rack_num, dst_rack_num, src_racks, dst_racks, mean, std, protocol, iperf_version):
    # STEP4: How many servers 
    server_num_list = np.arange(MIN_SERVER_NUM, MAX_SERVER_NUM+1) # (1 ~ 16)
    src_servers_per_rack_num = np.random.choice(server_num_list, size=src_rack_num)
    dst_servers_per_rack_num = np.random.choice(server_num_list, size=dst_rack_num)
    
    # STEP5: Which servers
    src_servers_per_rack = list()
    dst_servers_per_rack = list()
    server_list = np.arange(MIN_SERVER_ID, MAX_SERVER_ID+1) # (16 ~ 31)
    for src_num in src_servers_per_rack_num:
        src_servers_per_rack.append(np.random.choice(server_list, size=src_num, replace=False))
    for dst_num in dst_servers_per_rack_num:
        dst_servers_per_rack.append(np.random.choice(server_list, size=dst_num, replace=False))
    
    # STEP6: Determine src & dst pair
    traffics = list()
    port = START_PORT
    for src_index, src_rack in enumerate(src_racks):
        for dst_index, dst_rack in enumerate(dst_racks):
            for src_server in src_servers_per_rack[src_index]:
                for dst_server in dst_servers_per_rack[dst_index]:
                    # STEP7: Determine flow load & duration
                    load = get_load(mean, std)
                    duration = get_duration(mean, std)

                    src_server_ip = rack_to_server_ip(src_rack, src_server)
                    dst_server_ip = rack_to_server_ip(dst_rack, dst_server)
                    port += 1
                    protocol = protocol
                    iperf_version = iperf_version

                    traffics.append(create_traffic(src_server_ip, dst_server_ip, port, protocol, load, duration, iperf_version))
    return traffics

def start_traffics(traffics):
    for traffic in traffics:
        cmd = "salt \"" + str(traffic.src_server_name) + "\" cmd.run \"ping " + str(traffic.dst_server_ip) + " -c " + str(traffic.duration) + " > " + str(traffic.src_server_name) + "_to_" + str(traffic.dst_server_name) + ".txt\" &"
        # process = sp.Popen(cmd, shell=True)
        print(cmd)


def generate_traffic(case, mean, std, traffic_file=None, protocol="u", iperf_version="iperf2"):
    # STEP1: Traffic Generate Case
    if case == "fixed":
        traffics = get_traffics_from_file(traffic_file)
    elif case == "whole":
        # STEP2: How many racks
        src_rack_num = MAX_RACK_NUM
        dst_rack_num = MAX_RACK_NUM

        # STEP3: Which racks
        src_racks = np.arange(MIN_RACK_NUM, MAX_RACK_NUM+1)
        dst_racks = np.arange(MIN_RACK_NUM, MAX_RACK_NUM+1)

        # GET TRAFFICS
        traffics = get_traffics(src_rack_num, dst_rack_num, src_racks, dst_racks, mean, std, protocol, iperf_version)
    elif case == "locality":
        # STEP2: How many racks (1 ~ 15)
        src_rack_num = int(uniform_distribution(MIN_RACK_NUM, MAX_RACK_NUM+1))
        dst_rack_num = int(uniform_distribution(MIN_RACK_NUM, MAX_RACK_NUM+1))

        # STEP3: Which racks
        rack_list = np.arange(MIN_RACK_NUM, MAX_RACK_NUM+1) # (1 ~ 15)
        src_racks = np.random.choice(rack_list, size=src_rack_num, replace=False)
        dst_racks = np.random.choice(rack_list, size=dst_rack_num, replace=False)

        # GET TRAFFICS
        traffics = get_traffics(src_rack_num, dst_rack_num, src_racks, dst_racks, mean, std, protocol, iperf_version)
    else:
        print("Wrong Case Input!!!!")

    # STEP8: Start the traffic
    start_traffics(traffics)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--case', type=str)
    parser.add_argument('--traffic_file', type=str)
    parser.add_argument('--mean', type=int)
    parser.add_argument('--std', type=float)
    args = parser.parse_args()

    generate_traffic(args.case, args.mean, args.std, args.traffic_file)