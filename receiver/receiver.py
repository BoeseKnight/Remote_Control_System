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
# import message_filters


class Receiver:
    def receive(self):
        pass


class OnBoardReceiver(Receiver):
    def __init__(self):
        self.command_list = ReceiveCommandsList()

    # def receive(self):
    #     # rospy.Subscriber("route_cmds", String, self.__callback)
    #     # rospy.Subscriber("route_cmds2", String, self.__callback)
    #     print("IN RECEIVE")
    #     r1 = message_filters.Subscriber("route_cmds", String)
    #     r2 = message_filters.Subscriber("route_cmds2", String)
    #     # r3=message_filters.Subscriber("route_cmds3", String)
    #     filter = message_filters.ApproximateTimeSynchronizer([r1, r2], 10, 0.1, allow_headerless=True)
    #     filter.registerCallback(self.__callback)
    #     rospy.spin()

    def __callback(self, route_cmds, route_cmds2):
        # def __callback(self, data):
        # print(f"Received: {data.data}")
        # self.command_list.append(data.data)
        print(f"[RECEIVED]: {route_cmds.data}")
        self.command_list.append(route_cmds.data)
        print(f"[RECEIVED]: {route_cmds2.data}")
        self.command_list.append(route_cmds2.data)
        # print(f"[RECEIVED]: {r3.data}")
        # self.command_list.append(r3.data)


# SERVER
class VideoStreamReceiver(Receiver):
    def __init__(self):
        self.frame_list = FramesList()

    def receive(self, stop_thread):

        Window.console.insert('1.0', "System initialized\n")
        server_socket = VideoServer.configure()
        image = cv2.imread("/home/ilya/catkin_ws/src/puk/src/receiver/no_signal.jpg")
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
                client_data = server_socket.recvfrom(1000000)
            except socket.timeout as e:
                continue
            client_ip = client_data[1][0]
            # print(f"{client_ip} connected!")
            data = client_data[0]
            data_loads = pickle.loads(data)
            data = cv2.imdecode(data_loads, cv2.IMREAD_COLOR)
            flipped_image = cv2.flip(data, 1)
            image = cv2.cvtColor(flipped_image, cv2.COLOR_BGR2RGB)
            self.frame_list.append(image)
            tkinter_image = Image.fromarray(image)
            photo_image = ImageTk.PhotoImage(image=tkinter_image)
            Window.video_stream.configure(image=photo_image)
            Window.video_stream.image = photo_image
