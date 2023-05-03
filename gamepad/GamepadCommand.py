class GamepadCommand:
    def __init__(self, button_number, button_name):
        self.button_number = button_number
        self.button_name = button_name

    def __str__(self):
        return f"{self.button_name}[{self.button_number}] pressed"