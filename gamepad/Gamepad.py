import pygame


class Gamepad:
    controller = None

    @classmethod
    def setup(cls):
        pygame.init()
        pygame.joystick.init()
        cls.controller = pygame.joystick.Joystick(0)
        cls.controller.init()

