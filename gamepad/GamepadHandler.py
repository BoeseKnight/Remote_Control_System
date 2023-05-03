from gamepad.Gamepad import Gamepad
from gamepad.GamepadButtons import GamepadButtons, GamepadDpad
from gamepad.GamepadCommand import GamepadCommand
import pygame


class GamepadHandler:
    @classmethod
    def run(cls):
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

        print("Press PS button to quit:")
        end = False
        while end is False:
            isAction = False
            exact_event = None
            while isAction is False and exact_event is None:
                # Get events
                gamepad_events = pygame.event.get()

                for event in gamepad_events:
                    if event.type == pygame.JOYAXISMOTION:
                        axis[event.axis] = round(event.value, 3)
                        # print(event.axis)
                        # isAction = True
                        # exact_event = event.axis
                    elif event.type == pygame.JOYBUTTONDOWN:
                        button[event.button] = True
                        isAction = True
                        exact_event = event.button
                        end = button[GamepadButtons.PS.value]
                    elif event.type == pygame.JOYBUTTONUP:
                        button[event.button] = False
                    elif event.type == pygame.JOYHATMOTION:
                        hat[event.hat] = event.value
                        exact_event = GamepadDpad.get_direction(hat[0])
            action = GamepadCommand(exact_event, GamepadButtons(exact_event).name)
            print(action)

            # Limited to 30 frames per second to make the display not so flashy
            clock = pygame.time.Clock()
            clock.tick(30)
