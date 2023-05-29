import fcntl
import os
import socket
import struct


class NetworkUtil:
    @classmethod
    def get_network_interfaces(cls):
        nic_names = os.listdir('/sys/class/net/')
        return nic_names

    @classmethod
    def get_ip_address(cls, interface):
        ip_address = None
        ip_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            ip_address = socket.inet_ntoa(fcntl.ioctl(
                ip_socket.fileno(),
                0x8915,  # SIOCGIFADDR
                struct.pack('256s', bytes(interface[:15], 'utf-8'))
            )[20: 24])
        except OSError:
            # print("")
            print(f"Network Interface {interface} is down or doesn't exist")
        return ip_address
