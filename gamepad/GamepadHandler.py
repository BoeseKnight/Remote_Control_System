from gamepad.Gamepad import Gamepad
from gamepad.GamepadButtons import GamepadButtons, GamepadDpad, GamepadSticks
from gamepad.GamepadCommand import GamepadCommand
import pygame


class GamepadHandler:
    @classmethod
    def __initialization(cls):
        axis = {}
        button = {}
        hat = {}
        Gamepad.setup()
        # Axes and buttons initialization
        for i in range(Gamepad.controller.get_numaxes()):
            # print(Gamepad.controller.get_numaxes())
            axis[i] = 0.0
        for i in range(Gamepad.controller.get_numbuttons()):
            # print(Gamepad.controller.get_numbuttons())
            button[i] = False
        for i in range(Gamepad.controller.get_numhats()):
            hat[i] = (0, 0)
        return axis, button, hat

    @classmethod
    def run(cls):
        axis, button, hat = cls.__initialization()
        print("Press PS button to quit:")
        end = False
        while end is False:
            axis_event = None
            button_event = None
            while axis_event is None and button_event is None:
                # Get events
                gamepad_events = pygame.event.get()

                for event in gamepad_events:
                    if event.type == pygame.JOYAXISMOTION:
                        axis[event.axis] = round(event.value, 3)
                        if axis[event.axis] != 0:
                            # print(f"Axis: {event.axis}   Value: {axis[event.axis]}")
                            axis_event = event.axis
                    if event.type == pygame.JOYBUTTONDOWN:
                        button[event.button] = True
                        button_event = event.button
                        end = button[GamepadButtons.PS.value]
                    if event.type == pygame.JOYBUTTONUP:
                        button[event.button] = False
                    if event.type == pygame.JOYHATMOTION:
                        hat[event.hat] = event.value
                        button_event = GamepadDpad.get_direction(hat[0])
            if axis_event is not None:
                action = GamepadCommand(axis_event, GamepadSticks(axis_event).name, axis[axis_event])
                print(action)

            if button_event is not None:
                action = GamepadCommand(button_event, GamepadButtons(button_event).name)
                print(action)

            # # Limited to 30 frames per second to make the display not so flashy
            # clock = pygame.time.Clock()
            # clock.tick(30)
