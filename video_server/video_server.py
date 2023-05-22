from network import *


class VideoServer:
    __socket = None
    __ip = None
    __port = 50000

    @classmethod
    def __get_ip(cls):
        network_interfaces = NetworkUtil.get_network_interfaces()
        print(network_interfaces)
        for nic in network_interfaces:
            cls.__ip = NetworkUtil.get_ip_address(nic)
            print(cls.__ip)
            if cls.__ip is not None and nic != 'lo':
                break

    @classmethod
    def configure(cls):
        cls.__get_ip()
        cls.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        cls.__socket.setblocking(False)
        cls.__socket.settimeout(1)
        cls.__socket.bind((VideoServer.__ip, VideoServer.__port))
        return VideoServer.__socket
