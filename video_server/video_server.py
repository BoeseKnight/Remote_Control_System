import socket
from network import NetworkUtil


class VideoServer:
    __socket = None
    __ip = None
    __port = 50000

    @classmethod
    def __get_ip(cls):
        network_interfaces = NetworkUtil.get_network_interfaces()
        # print(network_interfaces)
        # Window.console.insert('1.0', "Available network interfaces: " + ' '.join([str(elem) for elem in network_interfaces])+'\n')
        for nic in network_interfaces:
            cls.__ip = NetworkUtil.get_ip_address(nic)
            # print(cls.__ip)
            # Window.console.insert('1.0', str(nic)+" ip Address: "+str(cls.__ip)+'\n')
            # print(str(nic)+" ip Address: "+str(cls.__ip)+'\n')
            if cls.__ip is not None and nic != 'lo':
                # Window.console.insert('1.0', "Server IP Address: " + str(cls.__ip) + '\n')
                break

    @classmethod
    def configure(cls):
        cls.__get_ip()
        cls.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        cls.__socket.setblocking(False)
        cls.__socket.settimeout(2)
        cls.__socket.bind((VideoServer.__ip, VideoServer.__port))
        return VideoServer.__socket
