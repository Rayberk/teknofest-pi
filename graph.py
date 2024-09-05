import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Load the CSV data into a pandas DataFrame
def load_sensor_data(file_path):
    data = pd.read_csv(file_path)
    return data

# Plot scrollable graph
def plot_scrollable_graph(file_path):
    # Load the data from CSV
    data = load_sensor_data(file_path)

    # Extract data columns
    times = data["Time"]
    accel_x = data["Accel X"]
    accel_y = data["Accel Y"]
    accel_z = data["Accel Z"]
    gyro_x = data["Gyro X"]
    gyro_y = data["Gyro Y"]
    gyro_z = data["Gyro Z"]

    # Total data points and window size
    total_points = len(times)
    window_size = 250  # Number of points to show at once (adjustable)

    # Create figure and axes for the subplots (2 rows, 3 columns)
    fig, axes = plt.subplots(2, 3, figsize=(12, 8))
    plt.subplots_adjust(bottom=0.2)  # Add space for the slider

    # Titles and labels for each axis
    titles = ["Accelerometer X", "Accelerometer Y", "Accelerometer Z",
              "Gyroscope X", "Gyroscope Y", "Gyroscope Z"]
    ylabels = ["Acceleration (g)", "Acceleration (g)", "Acceleration (g)",
               "Rotation (deg/s)", "Rotation (deg/s)", "Rotation (deg/s)"]

    # Flatten axes for easier access
    axes = axes.flatten()

    # Initialize lines for each subplot
    lines = []
    for i, ax in enumerate(axes):
        ax.set_title(titles[i])
        ax.set_xlabel("Time (s)")
        ax.set_ylabel(ylabels[i])
        ax.set_xlim(times[0], times[window_size-1])  # Initial x-axis limits
        lines.append(ax.plot(times[:window_size], [0]*window_size, 'r-')[0])

    # Assign the right data to each line
    data_map = [accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z]

    # Update the lines with the initial data (first window_size points)
    for i, line in enumerate(lines):
        line.set_ydata(data_map[i][:window_size])

    # Function to update the graph as the slider is moved
    def update(val):
        idx = int(val)  # Get the slider value as an integer index
        start = idx
        end = idx + window_size

        # Update x-axis limits for all plots
        for ax in axes:
            ax.set_xlim(times[start], times[end-1])

        # Update y-data for all lines
        for i, line in enumerate(lines):
            line.set_data(times[start:end], data_map[i][start:end])

        fig.canvas.draw_idle()  # Redraw the canvas

    # Add a slider below the plot
    ax_slider = plt.axes([0.2, 0.05, 0.65, 0.03], facecolor='lightgoldenrodyellow')
    slider = Slider(ax_slider, 'Scroll', 0, total_points-window_size, valinit=0, valstep=1)

    # Call update function when the slider is changed
    slider.on_changed(update)

    # Show the plot
    plt.show()

# Usage
# Replace 'sensor_data_XXXX.csv' with the actual filename
file_path = 'sensor_data_XXXX.csv'
plot_scrollable_graph(file_path)
