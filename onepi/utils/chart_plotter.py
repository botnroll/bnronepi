import matplotlib.pyplot as plt
import numpy as np
import time


class ChartPlotter:
    def __init__(self, number_of_series=1, buffer_size=100, x_label="Iter", y_label="Value", title="Title", labels=[[]]):
        self.__buffer_size = buffer_size
        self.__number_of_series = number_of_series
        self.__serie = [[] for _ in range(number_of_series)]
        self.__serie_data = [[] for _ in range(number_of_series)]
        if len(labels) != number_of_series:
            labels = [[] for _ in range(number_of_series)]
        # Create the plot
        self.fig, self.ax = plt.subplots()
        self.x = np.arange(-buffer_size, 0, 1)
        for i in range(number_of_series):
            self.__serie_data[i] = np.zeros(buffer_size)
            (self.__serie[i],) = self.ax.plot(
                self.x, self.__serie_data[i], label=labels[i]
            )
        self.ax.set_ylim(0, 800)
        self.ax.legend()
        self.ax.set_title(title)
        self.ax.set_xlabel(x_label)
        self.ax.set_ylabel(y_label)
        self.ax.grid(True)

    def set_title(self, title):
        self.ax.set_title(title)

    def set_axis_labels(self, x_label, y_label):
        self.ax.set_xlabel(x_label)
        self.ax.set_ylabel(y_label)

    def set_series_labels(self, series_labels):
        if len(series_labels) != self.__number_of_series:
            print("Error. number of labels != number of series")
        else:
            for i in range(self.__number_of_series):
                self.__serie[i].set_label(series_labels[i])
            self.ax.legend()

    def set_y_limits(self, y_min = 0, y_max = 800):
        self.ax.set_ylim(y_min, y_max)

    def update_buffers(self, data):
        self.x = np.roll(self.x, -1)
        self.x[-1] = self.x[-2] + 1
        
        for i in range(self.__number_of_series):
            self.__serie_data[i] = np.roll(self.__serie_data[i], -1)
            self.__serie_data[i][-1] = data[i]    
            self.__serie[i].set_xdata(self.x)
            self.__serie[i].set_ydata(self.__serie_data[i])
        
        # Update the plot
        x_limits = self.ax.get_xlim()
        new_x_limits = (x_limits[0] + 1, x_limits[1] + 1)
        self.ax.set_xlim(new_x_limits)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def show_plot(self):
        plt.ion()
        plt.show()
    
    def close_plot(self):
        plt.close('all')


# Example of using the class
def main():
    chart_plotter = ChartPlotter(2)
    chart_plotter.set_y_limits(0, 20)
    chart_plotter.set_title("Temperature over Time")
    chart_plotter.set_axis_labels("Time (x0.1 s)", "Temperature (C)")
    chart_plotter.set_series_labels(["Reference", "Current Temperature"])
    chart_plotter.show_plot()

    for i in range(200):
        reference_value = 15 + np.sin(i * 0.1)  # Example reference data
        actual_value = reference_value + np.random.normal(
            0, 0.5
        )  # Example actual data with noise
        chart_plotter.update_buffers([reference_value, actual_value])
        print(reference_value, actual_value)
        time.sleep(0.1)  # Simulation of your timer
    
    time.sleep(2)


if __name__ == "__main__":
    main()
