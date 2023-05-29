class GamepadCommand:
    def __init__(self, button_number, button_name, value=0.0):
        self.button_number = button_number
        self.button_name = button_name
        self.value = value

    def __str__(self):
        if self.value == 0:
            return f"{self.button_name}[{self.button_number}] pressed"
        else:
            return f"{self.button_name}[{self.button_number}] {self.value}"
