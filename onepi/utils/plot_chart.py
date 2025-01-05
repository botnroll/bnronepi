import matplotlib.pyplot as plt
import numpy as np
import time


class PlotChart:
    def __init__(self, buffer_size=100):
        self.buffer_size = buffer_size
        self.reference_buffer = np.zeros(buffer_size)
        self.actual_buffer = np.zeros(buffer_size)

        # Create the plot
        self.fig, self.ax = plt.subplots()
        self.x = np.arange(buffer_size)
        (self.line1,) = self.ax.plot(
            self.x, self.reference_buffer, label="Reference Value"
        )
        (self.line2,) = self.ax.plot(self.x, self.actual_buffer, label="Actual Value")

        self.ax.set_ylim(0, 800)
        self.ax.legend()
        self.ax.set_title("Reference vs. Actual Values")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Values")
        self.ax.grid(True)

    def update_buffers(self, reference, actual):
        self.reference_buffer = np.roll(self.reference_buffer, -1)
        self.actual_buffer = np.roll(self.actual_buffer, -1)
        self.reference_buffer[-1] = reference
        self.actual_buffer[-1] = actual

        # Update the plot
        self.line1.set_ydata(self.reference_buffer)
        self.line2.set_ydata(self.actual_buffer)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def show_plot(self):
        plt.ion()
        plt.show()


# Example of using the class
def main():
    plotter = PlotChart()
    plotter.show_plot()

    for i in range(200):
        reference_value = np.sin(i * 0.1)  # Example reference data
        actual_value = np.sin(i * 0.1) + np.random.normal(
            0, 0.1
        )  # Example actual data with noise
        plotter.update_buffers(reference_value, actual_value)
        time.sleep(0.1)  # Simulation of your timer


if __name__ == "__main__":
    main()
