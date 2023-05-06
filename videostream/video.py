import cv2
import socket
import pickle
from network import *

print(NetworkUtil.get_ip_address('enp2s0'))
print(NetworkUtil.get_ip_address('wlp4s0'))


# SERVER
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip = "192.168.0.102"
port = 60000
server_socket.bind((ip, port))
while True:
    x = server_socket.recvfrom(1000000)
    client_ip = x[1][0]
    data = x[0]
    print(data)
    data = pickle.loads(data)
    print(type(data))
    data = cv2.imdecode(data, cv2.IMREAD_COLOR)
    image = cv2.flip(data, 1)
    cv2.imshow('server', image)  # to open image
    if cv2.waitKey(10) == 13:
        break
cv2.destroyAllWindows()

# CLIENT

# import cv2
# import pickle
# import socket
#
# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1000000)
# server_ip = "192.168.0.114"
# server_port = 6666
#
# cap = cv2.VideoCapture(-1)
# while True:
#     ret, photo = cap.read()
#     cv2.imshow('streaming', photo)
#     ret, buffer = cv2.imencode(".jpg", photo, [int(cv2.IMWRITE_JPEG_QUALITY), 30])
#     x_as_bytes = pickle.dumps(buffer)
#     s.sendto((x_as_bytes), (server_ip, server_port))
#     if cv2.waitKey(10) == 13:
#         break
# cv2.destroyAllWindows()
# cap.release()
