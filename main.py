import threading
import time

# from gamepad.GamepadHandler import GamepadHandler
from gamepad import *
from route import *
from tkinter import *
from video_server import *
from window import Window
from receiver import *
from sender import *
import rospy
from std_msgs.msg import String

shared_list = []

if __name__ == '__main__':
    # rospy.init_node("remote_control_system", anonymous=True)

    stop = threading.Event()

    # on_board_receiver = OnBoardReceiver()
    # command_sender = CommandSender()
    video_stream_receiver = VideoStreamReceiver()

    # получение информации по ROS от бортового компьютера
    # receive_thread = threading.Thread(target=on_board_receiver.receive, args=(stop,))

    # отправление информации по ROS к бортовому компьютеру
    # sender_thread = threading.Thread(target=command_sender.send)

    # полная обработка событий геймпада
    gamepad_thread = threading.Thread(target=GamepadHandler.run, args=(stop,))

    # получение информации по UDP от подсистемы технического зрения
    videostream_thread = threading.Thread(target=video_stream_receiver.receive, args=(stop,))

    # Запускаем потоки
    gamepad_thread.start()
    # send_thread.start()
    # receive_thread.start()
    videostream_thread.start()
    Window.run()
    stop.set()
