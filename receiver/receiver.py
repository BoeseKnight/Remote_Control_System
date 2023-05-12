import time

from commands import *
import cv2
import socket
import pickle
from video_server import *
from window import Window
from PIL import Image, ImageTk
import rospy
from std_msgs.msg import String


class Receiver:
    def receive(self, stop_thread):
        pass


# Working and tested variant
# class Receiver:
#     @classmethod
#     def receive(cls):
#         rospy.Subscriber("route_cmds", String, cls.callback)
#         rospy.spin()
#
#     @classmethod
#     def callback(cls, data):
#         global i
#         i += 1
#         print(data.data + str(i))
class OnBoardReceiver(Receiver):
    def __init__(self):
        self.command_list = ReceiveCommandsList()

    def receive(self, stop_thread):
        rospy.Subscriber("route_cmds", String, self.__callback)
        rospy.spin()

    def __callback(self, data):
        print(f"Received: {data.data}")
        self.command_list.append(data.data)


# SERVER
class VideoStreamReceiver(Receiver):
    def __init__(self):
        self.frame_list = FramesList()

    def receive(self, stop_thread):
        server_socket = VideoServer.configure()
        image = cv2.imread("no_signal.jpg")
        captured_image = Image.fromarray(image)
        # Convert captured image to photoimage
        photo_image = ImageTk.PhotoImage(image=captured_image.resize((920, 540)))
        Window.video_stream.configure(image=photo_image)

        while True:
            # time.sleep(0.1)
            if stop_thread.is_set():
                print("Child stopped")
                break
            try:
                x = server_socket.recvfrom(1000000)
            except socket.timeout as e:
                continue
            client_ip = x[1][0]
            # print(f"{client_ip} connected!")
            data = x[0]
            data_loads = pickle.loads(data)
            data = cv2.imdecode(data_loads, cv2.IMREAD_COLOR)
            flipped_image = cv2.flip(data, 1)
            image = cv2.cvtColor(flipped_image, cv2.COLOR_BGR2RGB)
            self.frame_list.append(image)
            tkinter_image = Image.fromarray(image)
            photo_image = ImageTk.PhotoImage(image=tkinter_image)
            Window.video_stream.configure(image=photo_image)
            Window.video_stream.image = photo_image
