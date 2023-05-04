from gamepad.Gamepad import Gamepad
from gamepad.GamepadButtons import GamepadButtons, GamepadDpad, GamepadSticks
from gamepad.GamepadCommand import GamepadCommand
import pygame


class GamepadHandler:
    axis = {}
    button = {}
    hat = {}

    @classmethod
    def __initialization(cls):
        Gamepad.setup()
        # Axes and buttons initialization
        for i in range(Gamepad.controller.get_numaxes()):
            cls.axis[i] = 0.0
        for i in range(Gamepad.controller.get_numbuttons()):
            cls.button[i] = False
        for i in range(Gamepad.controller.get_numhats()):
            cls.hat[i] = (0, 0)

    @classmethod
    def __handle_events(cls):
        axis_event = None
        button_event = None
        gamepad_events = pygame.event.get()
        for event in gamepad_events:
            if event.type == pygame.JOYAXISMOTION:
                cls.axis[event.axis] = round(event.value, 3)
                if cls.axis[event.axis] != 0:
                    axis_event = event.axis
            if event.type == pygame.JOYBUTTONDOWN:
                cls.button[event.button] = True
                button_event = event.button
            if event.type == pygame.JOYBUTTONUP:
                cls.button[event.button] = False
            if event.type == pygame.JOYHATMOTION:
                cls.hat[event.hat] = event.value
                button_event = GamepadDpad.get_direction(cls.hat[event.hat])
        return axis_event, button_event

    @classmethod
    def run(cls):
        cls.__initialization()
        print("Press PS button to quit:")
        end = False
        while end is False:
            axis_event = None
            button_event = None
            while axis_event is None and button_event is None:
                # Get gamepad events
                axis_event, button_event = cls.__handle_events()

            end = cls.button[GamepadButtons.PS.value]
            if axis_event is not None:
                action = GamepadCommand(axis_event, GamepadSticks(axis_event).name, cls.axis[axis_event])
                print(action)
            if button_event is not None:
                action = GamepadCommand(button_event, GamepadButtons(button_event).name)
                print(action)
