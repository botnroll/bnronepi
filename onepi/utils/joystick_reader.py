import pygame

class JoystickReader:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()

        self.joystick_count = pygame.joystick.get_count()
        if self.joystick_count == 0:
            raise Exception("No joysticks connected.")
        
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
        print(f"Joystick name: {self.joystick.get_name()}")

    def get_axis_values(self):
        pygame.event.pump()
        axis_1_value = self.joystick.get_axis(1)
        axis_3_value = self.joystick.get_axis(3)
        return axis_1_value, axis_3_value

# Example usage
if __name__ == "__main__":
    joystick_reader = JoystickReader()
    
    while True:
        axis_1, axis_3 = joystick_reader.get_axis_values()
        print(f"Axis 1: {axis_1:.2f}, Axis 3: {axis_3:.2f}", end='\r')
