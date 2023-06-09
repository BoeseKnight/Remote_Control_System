import threading
import time
import multiprocessing as mp
from gamepad import *
from control_system import ControlSystemState
# from gamepad.GamepadHandler import GamepadHandler

from route import *
from tkinter import *
from video_server import *
from window import Window
from receiver import *
from sender import *
import rospy
from std_msgs.msg import String


if __name__ == '__main__':
    app = Window()
    control_system_object = ControlSystemState()
    # rospy.init_node("remote_control_system", anonymous=True)

    stop = threading.Event()

    # on_board_receiver = OnBoardReceiver()
    # command_sender = CommandSender()
    video_stream_receiver = VideoStreamReceiver()

    # получение информации по ROS от бортового компьютера
    # receiver_thread = threading.Thread(target=on_board_receiver.receive, daemon=True)

    # отправление информации по ROS к бортовому компьютеру
    # sender_thread = threading.Thread(target=command_sender.send, daemon=True)

    # полная обработка событий геймпада
    gamepad_thread = threading.Thread(target=GamepadHandler.run, daemon=True)

    # получение информации по UDP от подсистемы технического зрения
    videostream_thread = threading.Thread(target=video_stream_receiver.receive, daemon=True)

    # Запускаем потоки
    gamepad_thread.start()
    # sender_thread.start()
    # receiver_thread.start()
    videostream_thread.start()
    app.run()
    stop.set()
