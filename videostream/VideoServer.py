from network import *

class VideoServer:
    __socket = None
    __ip = None
    __port = 60000

    @classmethod
    def __get_ip(cls):
        network_interfaces = NetworkUtil.get_network_interfaces()
        for nic in network_interfaces:
            VideoServer.__ip = NetworkUtil.get_ip_address(nic)
            if VideoServer.__ip is not None:
                break

    @classmethod
    def configure(cls):
        VideoServer.__get_ip()
        VideoServer.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        VideoServer.__socket.setblocking(False)
        VideoServer.__socket.settimeout(1)
        VideoServer.__socket.bind((VideoServer.__ip, VideoServer.__port))
        return VideoServer.__socket

