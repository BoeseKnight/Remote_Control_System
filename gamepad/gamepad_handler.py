import time
import traceback
from encoder import GamepadEncoder
from gamepad.gamepad_setup import Gamepad
from gamepad.gamepad_buttons import GamepadButtons, GamepadDpad, GamepadSticks
from gamepad.gamepad_command import GamepadCommand
import pygame
from commands import *

from window import Window


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
    def __handle_events(cls, stop_thread):
        axis_event = None
        button_event = None
        gamepad_events = pygame.event.get()
        for event in gamepad_events:
            # time.sleep(0.5)
            if stop_thread.is_set():
                print("Gamepad stopped")
                break
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
    def run(cls, stop_thread):
        cls.__initialization()
        print("Press PS button to quit:")
        end = False
        inner_commands = SendCommandsList()
        while end is False:
            # time.sleep(0.5)

            axis_event = None
            button_event = None
            while axis_event is None and button_event is None:
                # Get gamepad events
                axis_event, button_event = cls.__handle_events(stop_thread)
                if stop_thread.is_set():
                    print("Gamepad stopped2")
                    break
            if stop_thread.is_set():
                print("Gamepad stopped3")
                break
            end = cls.button[GamepadButtons.PS.value]
            action: GamepadCommand
            if axis_event is not None:
                action = GamepadCommand(axis_event, GamepadSticks(axis_event).name, cls.axis[axis_event])
                print(action)
            if button_event is not None:
                action = GamepadCommand(button_event, GamepadButtons(button_event).name)
                print(action)

            gamepad_encoder = GamepadEncoder()
            gamepad_encoder.set_command(action)
            inner_gamepad_command = gamepad_encoder.encode_command()
            if inner_gamepad_command is not None:
                inner_commands.append(inner_gamepad_command)
                print(inner_commands.get_list())
