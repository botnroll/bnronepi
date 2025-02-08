import numpy as np
import control as ctrl
import time

class LQRController:
    def __init__(self, A, B, C, D, Q, R, damping=0.10):
        # System parameters
        self.A = A - damping * np.eye(A.shape[0])
        self.B = B
        self.C = C
        self.D = D
        self.sys = ctrl.StateSpace(A, B, C, D)
        
        # LQR design parameters
        self.Q = Q
        self.R = R
        
        # Compute the LQR controller
        self.K, self.S, self.E = ctrl.lqr(self.sys, Q, R)
        
        # Initial state
        self.x = np.zeros((A.shape[0],))
        self._setpoint = 0

    def compute_output(self, current_speed, dt=0.01):
        # Update the current speed in the state
        self.x[0] = current_speed
        
        # Desired state
        x_desired = np.array([self._setpoint, 0])
        
        # Error
        e = x_desired - self.x
        
        # Control input
        u = -np.dot(self.K, e)
        
        # Update state
        self.x = self.x + (self.A @ self.x + self.B @ u) * dt
        
        return self.x, -u
    
    def get_setpoint(self):
        return self._setpoint
    
    def change_setpoint(self, setpoint):
        self._setpoint = setpoint

    def set_lqr_params(self, Q, R):
        self.Q = Q
        self.R = R
        self.K, self.S, self.E = ctrl.lqr(self.sys, Q, R)
        

# Example function to read encoder speed (replace with actual encoder reading code)
def read_encoder_speed():
    # Simulate encoder speed reading
    return np.random.uniform(90, 110)  # Replace with actual encoder reading code

# Example main program
def main():
    # System parameters
    A = np.array([[0, 1], [0, -1]])
    B = np.array([[0], [1]])
    C = np.array([[1, 0]])
    D = np.array([[0]])
    
    # LQR design parameters
    Q = np.diag([1, 1])
    R = np.array([[1]])
    
    # Instantiate the LQR controller
    controller = LQRController(A, B, C, D, Q, R)
    
    # Control loop parameters
    dt = 0.01  # Time step
    t_final = 10  # Final time
    
    # Desired speed (reference speed in encoder pulses per second)
    desired_speed = 100
    
    # Control loop
    for t in np.arange(0, t_final, dt):
        # Read the current speed from the encoder
        current_speed = read_encoder_speed()

        # set the desired speed
        controller.change_setpoint(desired_speed)

        # Update the controller with the current speed and desired speed
        x, u = controller.compute_output(current_speed, dt)
        
        # Print state
        print(f"Time: {t:.2f}, Current Speed: {current_speed:.2f}, Control Input: {u}")
        
        # Simulate motor response (replace with actual motor control code)
        # Example: GPIO PWM signal to control motor speed
        # pwm.set_duty_cycle(u)
        
        time.sleep(dt)

if __name__ == "__main__":
    main()
