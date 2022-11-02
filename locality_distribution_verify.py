import numpy as np
import matplotlib.pyplot as plt

with open('locality_distribution.txt') as infile:
   rack_nums = infile.readlines()

rack_num_list = list()
for num in rack_nums:
    rack_num_list.append(int(num))
print(rack_num_list)

print(f"dst_mean : {np.mean(rack_num_list)}")
print(f"dst_std : {np.std(rack_num_list)}")

dst_server_num_bins = np.linspace(1, 16)
plt.hist(rack_num_list, dst_server_num_bins, histtype="step", label='Dst. Rack #')
plt.legend(loc='upper right')
plt.xlabel('Dst. Rack #')
plt.ylabel('Number of Chosen Dst. Rack #')
plt.show()

