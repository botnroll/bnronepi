import time
import math
import numpy as np
import matplotlib.pyplot as plt

from onepi.utils.chart_plotter import ChartPlotter

duration = 180
# Generate time values
t = np.linspace(0, 1, duration)

# Generate the sinusoidal signal
signal = 15 + 2*np.sin(10*t)

# Generate the noise
noise = np.random.normal(size=t.shape)

# Add noise to the signal
noisy_signal = signal + noise

def test_plotter():
    number_of_series = 3
    series_labels = ["Reference", "Room Temperature", "External Temperature"]
    chart_plotter = ChartPlotter(number_of_series)
    chart_plotter.set_axis_labels("Time (s)", "Temperature (C)")
    chart_plotter.set_title("Temperature control")
    chart_plotter.set_series_labels(series_labels)
    chart_plotter.set_y_limits(0, 20)
    chart_plotter.show_plot()

    for i in range(duration):
        print(signal[i], noisy_signal[i], noisy_signal[i]*0.7)
        data = [signal[i], noisy_signal[i], noisy_signal[i]*0.7]
        chart_plotter.update_buffers(data)
        time.sleep(0.1)
    
    time.sleep(3)

def main():
    test_plotter()

if __name__ == "__main__":
    main()
