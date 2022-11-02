import numpy as np
import matplotlib.pyplot as plt

def init_rack_dict():
    keys = ('1.1', '1.2', '1.3', '1.4', '1.5', '2.1', '2.2', '2.3', '2.4', '2.5', '3.1', '3.2', '3.3', '3.4', '3.5')
    value = 0
    rack_count = dict.fromkeys(keys, value)
    return rack_count

def calculate_duplicates(racks):
    keys = ('1.1', '1.2', '1.3', '1.4', '1.5', '2.1', '2.2', '2.3', '2.4', '2.5', '3.1', '3.2', '3.3', '3.4', '3.5')
    value = 0
    rack_count = dict.fromkeys(keys, value)
    for rack_id in racks:
        rack_count[rack_id] += 1
    return rack_count

def rack_set_addition(rack_set1, rack_set2):
    for rack_id in rack_set1:
        rack_set1[rack_id] += rack_set2[rack_id]
    return rack_set1

def parse_file(dst_rack_num_list, src_rack_num_list, dst_rack_count, src_rack_count):

    with open('dst_num_distribution.txt', 'r') as infile:
        dst_rack_nums = infile.readlines()
    for num in dst_rack_nums:
        dst_rack_num_list.append(int(num))
    print(dst_rack_num_list)
    print(f"dst_rack_num_mean : {np.mean(dst_rack_num_list)}")
    print(f"dst_rack_num_std : {np.std(dst_rack_num_list)}")


    with open('src_num_distribution.txt', 'r') as infile:
        src_rack_nums = infile.readlines()
    for num in src_rack_nums:
        src_rack_num_list.append(int(num))
    print(src_rack_num_list)
    print(f"src_rack_num_mean : {np.mean(src_rack_num_list)}")
    print(f"src_rack_num_std : {np.std(src_rack_num_list)}")


    with open('dst_rack_distribution.txt', 'r') as infile:
        lines = infile.readlines()
    for line in lines:
        dst_rack_set = line.strip().split(' ')
        dst_rack_set_count = calculate_duplicates(dst_rack_set)
        dst_rack_count = rack_set_addition(dst_rack_count, dst_rack_set_count)

    with open('src_rack_distribution.txt', 'r') as infile:
        lines = infile.readlines()
    for line in lines:
        src_rack_set = line.strip().split(' ')
        src_rack_set_count = calculate_duplicates(src_rack_set)
        src_rack_count = rack_set_addition(src_rack_count, src_rack_set_count)


def plot_dst_rack_num(dst_rack_num_list):
    dst_server_num_bins = np.linspace(1, 16)
    plt.hist(dst_rack_num_list, dst_server_num_bins, histtype="step", label='Dst. Rack #')
    plt.legend(loc='upper right')
    plt.xlabel('Dst. Rack #')
    plt.ylabel('Number of Chosen Dst. Rack #')
    plt.show()

def plot_src_rack_num(src_rack_num_list):
    src_server_num_bins = np.linspace(1, 16)
    plt.hist(src_rack_num_list, src_server_num_bins, histtype="step", label='Src. Rack #')
    plt.legend(loc='upper right')
    plt.xlabel('Src. Rack #')
    plt.ylabel('Number of Chosen Src. Rack #')
    plt.show()

def  plot_dst_rack_distribution(dst_rack_count):
    dst_rack_bins = ['1.1', '1.2', '1.3', '1.4', '1.5', '2.1', '2.2', '2.3', '2.4', '2.5', '3.1', '3.2', '3.3', '3.4', '3.5']
    x = np.arange(len(dst_rack_bins))
    plt.bar(x, list(dst_rack_count.values()), label='Dst. Rack', tick_label=dst_rack_bins, fill=False)
    plt.legend(loc='upper right')
    plt.xlabel('Dst. Rack ID')
    plt.ylabel('Number of Chosen Destination Rack')
    plt.show()

def  plot_src_rack_distribution(src_rack_count):
    src_rack_bins = ['1.1', '1.2', '1.3', '1.4', '1.5', '2.1', '2.2', '2.3', '2.4', '2.5', '3.1', '3.2', '3.3', '3.4', '3.5']
    x = np.arange(len(src_rack_bins))
    plt.bar(x, list(src_rack_count.values()), label='Src. Rack', tick_label=src_rack_bins, fill=False)
    plt.legend(loc='upper right')
    plt.xlabel('Src. Rack ID')
    plt.ylabel('Number of Chosen Source Rack')
    plt.show() 


if __name__ == "__main__":

    dst_rack_num_list = list()
    src_rack_num_list = list()
    dst_rack_count = init_rack_dict()
    src_rack_count = init_rack_dict()

    parse_file(dst_rack_num_list, src_rack_num_list, dst_rack_count, src_rack_count)
    plot_dst_rack_num(dst_rack_num_list)
    plot_src_rack_num(src_rack_num_list)
    plot_dst_rack_distribution(dst_rack_count)
    plot_src_rack_distribution(src_rack_count)