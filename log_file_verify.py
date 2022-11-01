import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import truncnorm
import re
import argparse

flow_duration = list()
flow_load = list()
dst_rack = list()
dst_server = list()

def parse_cmd():
    with open('traffic_log.txt') as infile:
        cmds = infile.readlines()

    for cmd in cmds:
        # print(cmd)
        stats = re.findall(r'\d+', cmd)
        flow_load.append(float((stats[6] + "." + stats[7])))
        flow_duration.append(float(stats[9]))
        dst_rack.append(stats[3] + "." + stats[4])
        dst_server.append(int(stats[5]))


def generate_std_flow_load(mean, std):
    low_bound = 0
    high_bound = 10
    a, b = (low_bound - mean) / std, (high_bound - mean) / std
    std_load = [round(i, 2) for i in truncnorm.rvs(a, b, loc=mean, scale=std, size=len(flow_load))]
    return std_load

def generate_std_flow_duration(scale):
    std_duration = np.random.exponential(scale=scale, size=len(flow_duration))
    std_duration.astype(int)
    return std_duration

def generate_std_rack():
    rack_list = ['1.1', '1.2', '1.3', '1.4', '1.5', '2.1', '2.2', '2.3', '2.4', '2.5',
                '3.1', '3.2', '3.3', '3.4', '3.5']
    std_rack = np.random.choice(rack_list, size=len(dst_rack))
    print(std_rack)
    return std_rack

def generate_std_server():
    server_list = np.arange(16, 32) # [16 ~ 31]
    std_server = np.random.choice(server_list, size=len(dst_server))
    return std_server

def print_stats_result(std_duration, std_load):
    print(f"duration_mean: {np.mean(flow_duration)}")
    print(f"std_duration_mean: {np.mean(std_duration)}\n")
    print(f"duration_sigma: {np.std(flow_duration)}")
    print(f"std_duration_sigma: {np.std(std_duration)}\n")
    print(f"load_mean: {np.mean(flow_load)}")
    print(f"std_load_mean: {np.mean(std_load)}\n")
    print(f"load_sigma: {np.std(flow_load)}")
    print(f"std_load_sigma: {np.std(std_load)}")

def plot_duration(std_duration):
    duration_bins = np.linspace(0, 1000, 100)
    plt.hist(std_duration, duration_bins, histtype="step", label='Exponential Distribution')  # alpha: transparency
    plt.hist(flow_duration, duration_bins, histtype="step", label='Flow Duration')
    plt.legend(loc='upper right')
    plt.xlabel('Flow Duration (s)')
    plt.ylabel('Number of Flows')
    plt.show()

def plot_load(std_load):
    load_bins = np.linspace(0, 14, 200)
    plt.hist(std_load, load_bins, histtype="step", label='Truncated-normal Distribution')  # alpha: transparency
    plt.hist(flow_load, load_bins, histtype="step", label='Flow Load')
    plt.legend(loc='upper right')
    plt.xlabel('Flow Load (MB)')
    plt.ylabel('Number of Flows')
    plt.show()

def calculate_duplicates(racks):
    keys = ('1.1', '1.2', '1.3', '1.4', '1.5', '2.1', '2.2', '2.3', '2.4', '2.5', '3.1', '3.2', '3.3', '3.4', '3.5')
    value = 0
    rack_count = dict.fromkeys(keys, value)
    for rack_id in racks:
        rack_count[rack_id] += 1
    return rack_count

def plot_dst_rack(std_rack):
    dst_rack_bins = [1.1, 1.2, 1.3, 1.4, 1.5, 2.1, 2.2, 2.3, 2.4, 2.5, 3.1, 3.2, 3.3, 3.4, 3.5]
    dst_rack_count = calculate_duplicates(dst_rack)
    std_dst_rack_count = calculate_duplicates(std_rack)
    plt.plot(dst_rack_bins, list(std_dst_rack_count.values()), label='Uniform Distribution')
    plt.plot(dst_rack_bins, list(dst_rack_count.values()), label='Dst. Rack')
    plt.xticks([1.1, 1.2, 1.3, 1.4, 1.5, 2.1, 2.2, 2.3, 2.4, 2.5, 3.1, 3.2, 3.3, 3.4, 3.5])
    plt.legend(loc='upper right')
    plt.xlabel('Dst. Pod_Rack ID')
    plt.ylabel('Number of Chosen Rack ID')
    plt.show()

def plot_dst_server(std_server):
    dst_server_bins = np.linspace(16, 32)
    plt.hist(std_server, dst_server_bins, histtype="step", label='Uniform Distribution')
    plt.hist(dst_server, dst_server_bins, histtype="step", label='Dst. Server')
    axes = plt.gca()
    # axes.set_ylim([0, 1000])
    plt.legend(loc='upper right')
    plt.xlabel('Dst. Server ID')
    plt.ylabel('Number of Chosen Server ID')
    plt.show()

def start_analysis(mean, std, scale=1):
    parse_cmd()
    std_duration = generate_std_flow_duration(scale)
    std_load = generate_std_flow_load(mean, std)
    std_rack = generate_std_rack()
    std_server = generate_std_server()
    plot_duration(std_duration)
    plot_load(std_load)
    plot_dst_rack(std_rack)
    plot_dst_server(std_server)
    print_stats_result(std_duration, std_load)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--mean', type=int)
    parser.add_argument('--std', type=float)
    parser.add_argument('--scale', type=int)
    args = parser.parse_args()

    start_analysis(args.mean, args.std, args.scale)