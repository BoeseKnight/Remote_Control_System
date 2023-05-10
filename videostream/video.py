import cv2
import socket
import pickle
from .VideoServer import VideoServer
from window import Window
from PIL import Image, ImageTk


# SERVER
class VideoStream:
    @classmethod
    def get_stream(cls):
        server_socket = VideoServer.configure()
        image = cv2.imread("no_signal.jpg")
        captured_image = Image.fromarray(image)
        # Convert captured image to photoimage
        photo_image = ImageTk.PhotoImage(image=captured_image)
        Window.video_stream.configure(image=photo_image)
        while True:
            cv2.imshow('server', image)  # to open image
            cv2.waitKey(1000)

            try:
                x = server_socket.recvfrom(1000000)
            except socket.timeout as e:
                continue
            client_ip = x[1][0]
            print(f"{client_ip} connected!")
            data = x[0]
            print(data)
            data = pickle.loads(data)
            print(type(data))
            data = cv2.imdecode(data, cv2.IMREAD_COLOR)
            image = cv2.flip(data, 1)
            Window.video_stream.configure(image=image)
            cv2.imshow('server', image)  # to open image
            if cv2.waitKey(10) == 13:
                break
        cv2.destroyAllWindows()

# CLIENT
# class VideoStream:
#     @classmethod
#     def get_stream(cls):
#         s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1000000)
#         server_ip = "192.168.0.114"
#         server_port = 6666
#
#         cap = cv2.VideoCapture(-1)
#         while True:
#             ret, photo = cap.read()
#             cv2.imshow('streaming', photo)
#             ret, buffer = cv2.imencode(".jpg", photo, [int(cv2.IMWRITE_JPEG_QUALITY), 30])
#             x_as_bytes = pickle.dumps(buffer)
#             s.sendto((x_as_bytes), (server_ip, server_port))
#             if cv2.waitKey(10) == 13:
#                 break
#         cv2.destroyAllWindows()
#         cap.release()
