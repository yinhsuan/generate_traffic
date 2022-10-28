import sys

class Traffic:
    def __init__(self, src_server_ip, dst_server_ip, port, protocol, data_rate, duration, iperf_version, pid=None):
        self.src_server_name = self.ip_to_server_name(src_server_ip)
        self.dst_server_name = self.ip_to_server_name(dst_server_ip)
        self.src_server_ip = src_server_ip
        self.dst_server_ip = dst_server_ip
        self.data_rate = data_rate
        self.port = port
        self.pid = pid

        self.protocol = protocol
        self.duration = duration
        self.iperf_version = iperf_version

    def ip_to_server_name(self, ip):
        parsed_ip = ip.split(".")
        server_name = "s0" + str(parsed_ip[1]) + "0" + str(parsed_ip[2]) + str(parsed_ip[3])
        return server_name

def get_traffics_from_file(traffic_file):
    traffics = list()

    fileLine = open(traffic_file,'r').read().splitlines()
    while("" in fileLine):
        fileLine.remove("")

    for line in fileLine:
        parsed_argv = line.split(" ")
        traffics.append(Traffic(parsed_argv[0], parsed_argv[1], parsed_argv[2], 
                                parsed_argv[3], parsed_argv[4], parsed_argv[5], parsed_argv[6]))

        # print("{src_server_name} {dst_server_ip} {port} {protocol} {data_rate} {duration} {iperf_version}".format(src_server_name=parsed_argv[0], 
        #                                                                                                             dst_server_ip=parsed_argv[1], 
        #                                                                                                             port=parsed_argv[2], 
        #                                                                                                             protocol=parsed_argv[3],
        #                                                                                                             data_rate=parsed_argv[4],
        #                                                                                                             duration=parsed_argv[5],
        #                                                                                                             iperf_version=parsed_argv[6]))
    return traffics