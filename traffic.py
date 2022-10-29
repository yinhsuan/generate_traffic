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

def print_traffics(traffics):
    for traffic in traffics:
        print("{src_server_name}, {dst_server_name}, {src_server_ip}, {dst_server_ip}, {data_rate}, {port}".format(
                                                                        src_server_name=traffic.src_server_name,
                                                                        dst_server_name=traffic.dst_server_name, 
                                                                        src_server_ip=traffic.src_server_ip, 
                                                                        dst_server_ip=traffic.dst_server_ip, 
                                                                        data_rate=traffic.data_rate, 
                                                                        port=traffic.port))

