from commands import ReceiveCommandsList, FramesList
import cv2
import pickle
from video_server import *
from PIL import Image, ImageTk
import rospy
from std_msgs.msg import String
from window import Window
import threading
from decoder import CommandDecoder


class Receiver:
    def receive(self):
        pass


class OnBoardReceiver(Receiver):
    def __init__(self):
        self.decoder=CommandDecoder()
        self.command_list = ReceiveCommandsList()
        self.ros_topics = ["route_cmds", "telemetry"]

    def receive(self):
        print("IN RECEIVE")
        for topic in self.ros_topics:
            rospy.Subscriber(name=topic,
                             data_class=String,
                             callback=self.__callback)

    def __callback(self, route_cmds):
        print(f"[RECEIVED]: {route_cmds.data}")
        self.command_list.append(route_cmds.data)
        # self.decoder.set_command()

        # decoder_thread=threading.Thread(target=)


# SERVER
class VideoStreamReceiver(Receiver):
    def __init__(self):
        self.frame_list = FramesList()

    def receive(self):
        app = Window()
        is_no_signal = False
        # Window.console.insert('1.0', "System initialized\n")
        server_socket = VideoServer.configure()
        image = cv2.imread("/home/ilya/catkin_ws/src/puk/src/receiver/no_signal.jpg")
        captured_image = Image.fromarray(image)

        # Convert captured image to photoimage
        no_signal_image = ImageTk.PhotoImage(image=captured_image.resize((920, 540)))
        app.frames_queue.put(no_signal_image)
        app.root.event_generate("<<FramesQueue>>")
        # app.video_stream.configure(image=photo_image)
        while True:
            # time.sleep(0.1)

            try:
                client_data = server_socket.recvfrom(1000000)
            except socket.timeout as e:
                if is_no_signal is False:
                    is_no_signal = True
                    app.frames_queue.put(no_signal_image)
                    app.root.event_generate("<<FramesQueue>>")
                continue
            is_no_signal = False
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
            app.frames_queue.put(photo_image)
            app.root.event_generate("<<FramesQueue>>")
            # app.video_stream.configure(image=photo_image)
            # app.video_stream.image = photo_image
