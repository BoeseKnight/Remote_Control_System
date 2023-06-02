import traceback
from window import *

import pygame


class Gamepad:
    controller = None

    @classmethod
    def setup(cls):
        try:
            pygame.init()
            pygame.joystick.init()
            cls.controller = pygame.joystick.Joystick(0)
            cls.controller.init()
            # print("Gamepad connected")
            # Window.console.insert('1.0', "Gamepad Connected\n")
        except Exception as e:
            error_message = traceback.format_exc()
            # Window.console.insert('1.0', error_message)
            # Window.console.insert('1.0', "Gamepad not connected. Plug in Joystick and restart the program!\n")
