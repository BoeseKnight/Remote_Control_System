from window.main_window import app_log
import pygame


class Gamepad:
    controller = None

    @classmethod
    @app_log
    def setup(cls):
        try:
            pygame.init()
            pygame.joystick.init()
            cls.controller = pygame.joystick.Joystick(0)
            cls.controller.init()
            return "Gamepad Connected"
        except Exception as e:
            return f"{e}\n-----------"
