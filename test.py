import re

# cmd = r'salt "s010425" cmd.run "iperf2 -u -c 10.3.4.23 -b [3.96149976]M -P 1 -t 6237 -i 1 -p 7180" &'
# stats = re.findall(r'\d+', cmd)
# print(float(stats[6] + "." + stats[7])) # flow load
# print(stats[9]) # flow duration
# print(stats[5]) # dst server
# for idx, digit in enumerate(stats):
#     print(idx, digit)

# def cummulate_duplicates(l):
#     seen = {}

#     for item in l:
#         if item not in seen:
#             seen[item] = 1
#         else:
#             seen[item] += 1
#     return seen

src_rack = [5.4, 1.2, 1.3, 1.3, 1.3, 2.4, 3.5, 2.4]
res = [*set(src_rack)]
print(res)
print(len(res))

