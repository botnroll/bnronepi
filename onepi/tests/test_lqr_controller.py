import numpy as np
import time
import signal
from onepi.one import BnrOneA
from onepi.utils.lqr_controller import LQRController


one = BnrOneA(0, 0)  # object variable to control the Bot'n Roll ONE A

# function to stop the robot on exiting with CTRL+C
def stop_and_exit(sig, frame):
    print("Exiting application")
    one.stop()
    sys.exit(0)

signal.signal(signal.SIGINT, stop_and_exit)

# Example main program
def main():
    # System parameters
    # A = np.array([[0, 1], [0, -1]])
    # B = np.array([[0], [1]])
    # C = np.array([[1, 0]])
    # D = np.array([[0]])
    
    Kt = 0.01
    J = 0.01
    B = 0.01
    
    A = np.array([[0, 1], [0, -B/J]])
    B = np.array([[0], [Kt/J]])
    C = np.array([[1, 0]])
    D = np.array([[0]])

    # LQR design parameters
    Q = np.diag([0.1, 0.5])
    R = np.array([[0.1]])
    
    # Instantiate the LQR controller
    controller = LQRController(A, B, C, D, Q, R)
    
    # Control loop parameters
    dt = 0.01  # Time step
    t_final = 10  # Final time
    
    # Desired speed (reference speed in encoder pulses per second)
    desired_speed = 10
    current_speed = one.read_left_encoder()
    print("current_speed: ", current_speed)

    # Control loop
    for t in np.arange(0, t_final, dt):
        # Read the current speed from the encoder
        current_speed = one.read_left_encoder()
        
        # Update the controller with the current speed and desired speed
        x, u = controller.update(current_speed, desired_speed, dt)
        
        # Print state
        print(f"Time: {t:.2f}, Current Speed: {current_speed:.2f}, Control Input: {u}")
        
        # Simulate motor response (replace with actual motor control code)
        # Example: GPIO PWM signal to control motor speed
        # pwm.set_duty_cycle(u)
        one.move(-u, 0)

        time.sleep(dt)

    print("Finish")
    one.stop()

if __name__ == "__main__":
    main()