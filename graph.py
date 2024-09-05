import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import os

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

    # Titles and labels for each plot
    titles = ["Accelerometer X", "Accelerometer Y", "Accelerometer Z",
              "Gyroscope X", "Gyroscope Y", "Gyroscope Z"]
    ylabels = ["Acceleration (g)", "Acceleration (g)", "Acceleration (g)",
               "Rotation (deg/s)", "Rotation (deg/s)", "Rotation (deg/s)"]

    # Data map to assign data to each graph
    data_map = [accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z]

    # Create a separate figure for each plot
    for i in range(6):
        fig, ax = plt.subplots(figsize=(10, 6))  # Create a new figure for each graph
        ax.set_title(titles[i])
        ax.set_xlabel("Time (s)")
        ax.set_ylabel(ylabels[i])
        ax.set_xlim(times[0], times[window_size-1])  # Initial x-axis limits
        ax.set_ylim(min(data_map[i])*10, max(data_map[i])*10)  # 10x y-limits
        
        # Initialize the line with the initial data
        line, = ax.plot(times[:window_size], data_map[i][:window_size], 'r-')

        # Function to update the graph as the slider is moved
        def update(val, line=line, ax=ax, i=i):
            idx = int(val)  # Get the slider value as an integer index
            start = idx
            end = idx + window_size

            # Update x-axis limits for the plot
            ax.set_xlim(times[start], times[end-1])

            # Update y-data for the line
            line.set_data(times[start:end], data_map[i][start:end])

            fig.canvas.draw_idle()  # Redraw the canvas

        # Add a slider below the plot
        ax_slider = plt.axes([0.2, 0.05, 0.65, 0.03], facecolor='lightgoldenrodyellow')
        slider = Slider(ax_slider, 'Scroll', 0, total_points-window_size, valinit=0, valstep=1)

        # Call update function when the slider is changed
        slider.on_changed(update)

        # Show the plot in a separate window
        fig.canvas.manager.window.showMaximized()  # Maximize window for full-screen view
        plt.show()

# Ask for file ID (last 4 digits)
file_id = input("Enter the last 4 digits of the sensor data file: ")
file_path = f'sensor_data_{file_id}.csv'

# Check if the file exists before proceeding
if os.path.exists(file_path):
    plot_scrollable_graph(file_path)
else:
    print(f"File 'sensor_data_{file_id}.csv' not found.")
