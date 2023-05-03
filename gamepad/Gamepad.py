import pygame


class Gamepad:
    controller = None

    @classmethod
    def setup(cls):
        pygame.init()
        pygame.joystick.init()
        cls.controller = pygame.joystick.Joystick(0)
        cls.controller.init()
        print("Name" + str(cls.controller.get_name()))
        print("Buttons" + str(cls.controller.get_numbuttons()))
        print("Axes" + str(cls.controller.get_numaxes()))
        print("Hats"+str(cls.controller.get_numhats()))
        # while True:
        #     for event in pygame.event.get():
        #         if event.type == pygame.JOYBUTTONDOWN:
        #             print(f'Gamepadd button {event.button} pressed')
