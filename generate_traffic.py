import subprocess as sp
import numpy as np
from scipy.stats import truncnorm
import argparse
import math

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
    high_bound = 0.1
    a, b = (low_bound - mean) / std, (high_bound - mean) / std
    return format(truncated_normal_distribution(a, b, mean, std)[0], '.2f')

def get_duration(scale):
    # return int(normal_distribution(mean, std))
    return int(exponential_distribution(scale))

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

def get_traffics(src_rack_num, dst_rack_num, src_racks, dst_racks, mean, std, protocol, iperf_version, scale):
    # STEP4: How many servers 
    server_num_list = np.arange(MIN_SERVER_NUM, MAX_SERVER_NUM+1) # (1 ~ 16)
    src_servers_per_rack_num = np.random.choice(server_num_list, size=src_rack_num)
    dst_servers_per_rack_num = np.random.choice(server_num_list, size=dst_rack_num)
    # low_bound = MIN_SERVER_NUM
    # high_bound = MAX_SERVER_NUM
    # a, b = (low_bound - mean) / std, (high_bound - mean) / std
    # src_servers_per_rack_num = int(truncated_normal_distribution(a, b, mean, std))
    # dst_servers_per_rack_num = int(truncated_normal_distribution(a, b, mean, std))
    
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
                    load = str(get_load(mean, std)) + "M"
                    # duration = get_duration(mean, std)
                    duration = get_duration(scale)

                    src_server_ip = rack_to_server_ip(src_rack, src_server)
                    dst_server_ip = rack_to_server_ip(dst_rack, dst_server)
                    port += 1
                    protocol = protocol
                    iperf_version = iperf_version

                    traffics.append(create_traffic(src_server_ip, dst_server_ip, port, protocol, load, duration, iperf_version))
    return traffics

def start_traffics(traffics):
    text_file = open("traffic_log.txt", "w")
    text_file.write("")
    text_file.close()
    for traffic in traffics:
        cmd = "salt \"" + str(traffic.src_server_name) + "\" cmd.run \"" + str(traffic.iperf_version) + " -u -c " + str(traffic.dst_server_ip) + " -b " + str(traffic.data_rate) + " -P " + str(traffic.thread_num) + " -t " + str(traffic.duration) + " -i 1 -p " + str(traffic.port) + "\" &" 
        # cmd = r'salt --async "{minionName}" cmd.run "{traffic.iperf_version} -c {traffic.dst_server_ip} -p {traffic.port} {optionCMD} &"'
        # process = sp.Popen(cmd, shell=True)
        text_file = open("traffic_log.txt", "a")
        text_file.write("{}\n".format(cmd))
        text_file.close()
        print(cmd)


def generate_traffic(case, mean, std, traffic_file=None, scale=1, dst_rack_mean=0, dst_rack_std=0, protocol="u", iperf_version="iperf"):
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
        traffics = get_traffics(src_rack_num, dst_rack_num, src_racks, dst_racks, mean, std, protocol, iperf_version, scale)
    elif case == "locality":
        # STEP2: How many racks (1 ~ 15)
        if dst_rack_mean > 0: # calculate LC
            low_bound = MIN_RACK_NUM
            high_bound = MAX_RACK_NUM
            a, b = (low_bound - mean) / std, (high_bound - mean) / std
            src_rack_num = int(uniform_distribution(MIN_RACK_NUM, MAX_RACK_NUM+1))
            dst_rack_num = int(truncated_normal_distribution(a, b, dst_rack_mean, dst_rack_std))
        else:
            src_rack_num = int(uniform_distribution(MIN_RACK_NUM, MAX_RACK_NUM+1))
            dst_rack_num = int(uniform_distribution(MIN_RACK_NUM, MAX_RACK_NUM+1))

        # STEP3: Which racks
        rack_list = np.arange(MIN_RACK_NUM, MAX_RACK_NUM+1) # (1 ~ 15)
        src_racks = np.random.choice(rack_list, size=src_rack_num, replace=False)
        dst_racks = np.random.choice(rack_list, size=dst_rack_num, replace=False)

        # GET TRAFFICS
        traffics = get_traffics(src_rack_num, dst_rack_num, src_racks, dst_racks, mean, std, protocol, iperf_version, scale)
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
    parser.add_argument('--scale', type=int)
    parser.add_argument('--dst_rack_mean', type=int)
    parser.add_argument('--dst_rack_std', type=float)
    args = parser.parse_args()

    generate_traffic(args.case, args.mean, args.std, args.traffic_file, args.scale, args.dst_rack_mean, args.dst_rack_std)