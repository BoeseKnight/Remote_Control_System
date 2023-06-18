import threading
import rospy
from std_msgs.msg import String
from window.main_window import Window
import control_system.state as state
import receiver.receiver as command_receiver
import gamepad.gamepad_handler as gamepad_handler
from route import *
from sender import *

if __name__ == '__main__':
    control_system_object = state.ControlSystemState()
    app = Window()
    # rospy.init_node("remote_control_system", anonymous=True)

    stop = threading.Event()

    # on_board_receiver = OnBoardReceiver()
    # command_sender = CommandSender()
    video_stream_receiver = command_receiver.VideoStreamReceiver()

    # получение информации по ROS от бортового компьютера
    # receiver_thread = threading.Thread(target=on_board_receiver.receive, daemon=True)

    # отправление информации по ROS к бортовому компьютеру
    # sender_thread = threading.Thread(target=command_sender.send, daemon=True)

    # полная обработка событий геймпада
    gamepad_thread = threading.Thread(target=gamepad_handler.GamepadHandler.run, daemon=True)

    # получение информации по UDP от подсистемы технического зрения
    videostream_thread = threading.Thread(target=video_stream_receiver.receive, daemon=True)

    # Запускаем потоки
    gamepad_thread.start()
    # sender_thread.start()
    # receiver_thread.start()
    videostream_thread.start()
    app.run()
    RouteStorage.read_routes()
