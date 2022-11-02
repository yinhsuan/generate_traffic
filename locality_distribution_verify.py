import numpy as np

with open('locality_distribution.txt', 'a') as infile:
   rack_nums = infile.readlines()

rack_num_list = list()
for num in rack_nums:
    rack_num_list.append(int(num))

print(f"dst_mean : {np.mean(rack_num_list)}")
print(f"dst_std : {np.std(rack_num_list)}")