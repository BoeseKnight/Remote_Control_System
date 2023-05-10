import threading
# from gamepad.GamepadHandler import GamepadHandler
from gamepad import *
from route import *
from tkinter import *
from videostream import *
from window import Window
shared_list = []


# Функция, которая добавляет числа в общий список
def receive():
    i = 0
    while i < 10:
        shared_list.append(i)
        print(f"\nДобавлено число {i}")
        i += 1


# Функция, которая читает числа из общего списка и добавляет их в свой список
def send(stop):
    my_list = []
    while True:
        if len(shared_list) > 0:
            number = shared_list.pop(0)
            my_list.append(number)
            print(f"\nПрочитано число {number}")
            print(f"Мой список: {my_list}")
        if stop.is_set():
            print("Child stopped")
            break


if __name__ == '__main__':
    stop = threading.Event()
    # Создаем два потока
    send_thread = threading.Thread(target=send, args=(stop,))
    receive_thread = threading.Thread(target=receive)
    gamepad_thread = threading.Thread(target=GamepadHandler.run)
    videostream_thread = threading.Thread(target=VideoStream.get_stream)

    # Запускаем потоки
    gamepad_thread.start()
    send_thread.start()
    receive_thread.start()
    videostream_thread.start()
    Window.run()

    # Ждем, пока оба потока завершатся (хотя они будут работать бесконечно)
    # send_thread.join()
    receive_thread.join()
    stop.set()
