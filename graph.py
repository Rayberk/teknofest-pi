import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import os

# Load the CSV data into a pandas DataFrame
def load_sensor_data(file_path):
    data = pd.read_csv(file_path)
    return data

# Function to plot individual graphs in separate windows
def plot_individual_graph(times, y_data, title, ylabel, window_size):
    total_points = len(times)

    # Create a separate figure for each graph
    fig, ax = plt.subplots(figsize=(10, 6))  # Create a new figure for the graph
    fig.canvas.manager.window.showMaximized()  # Maximize window for full-screen view

    ax.set_title(title)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel(ylabel)
    ax.set_xlim(times[0], times[window_size-1])  # Initial x-axis limits
    ax.set_ylim(min(y_data) * 10, max(y_data) * 10)  # 10x y-limits for the data
    
    # Initialize the line with the initial data
    line, = ax.plot(times[:window_size], y_data[:window_size], 'r-')

    # Function to update the graph as the slider is moved
    def update(val):
        idx = int(val)  # Get the slider value as an integer index
        start = idx
        end = idx + window_size

        # Update x-axis limits for the plot
        ax.set_xlim(times[start], times[end-1])

        # Update y-data for the line
        line.set_data(times[start:end], y_data[start:end])

        fig.canvas.draw_idle()  # Redraw the canvas

    # Add a slider below the plot
    ax_slider = plt.axes([0.2, 0.05, 0.65, 0.03], facecolor='lightgoldenrodyellow')
    slider = Slider(ax_slider, 'Scroll', 0, total_points - window_size, valinit=0, valstep=1)

    # Call update function when the slider is changed
    slider.on_changed(update)

    # Show the plot in a separate window
    plt.show()

# Function to plot all graphs together in a single window
def plot_combined_graph(times, data_map, titles, window_size):
    total_points = len(times)

    # Create a new figure for the combined plot
    fig, ax = plt.subplots(figsize=(10, 6))  # Create a new figure
    fig.canvas.manager.window.showMaximized()  # Maximize window for full-screen view

    ax.set_title("Combined Graph")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Values")
    ax.set_xlim(times[0], times[window_size-1])  # Initial x-axis limits

    # Plot all lines with different colors
    colors = ['r-', 'g-', 'b-', 'c-', 'm-', 'y-']  # Colors for the lines
    lines = []
    for i in range(6):
        line, = ax.plot(times[:window_size], data_map[i][:window_size], colors[i], label=titles[i])
        lines.append(line)

    ax.legend()  # Add a legend to distinguish the graphs

    # Function to update the graph as the slider is moved
    def update(val):
        idx = int(val)  # Get the slider value as an integer index
        start = idx
        end = idx + window_size

        # Update x-axis limits for the plot
        ax.set_xlim(times[start], times[end-1])

        # Update y-data for each line
        for i, line in enumerate(lines):
            line.set_data(times[start:end], data_map[i][start:end])

        fig.canvas.draw_idle()  # Redraw the canvas

    # Add a slider below the plot
    ax_slider = plt.axes([0.2, 0.05, 0.65, 0.03], facecolor='lightgoldenrodyellow')
    slider = Slider(ax_slider, 'Scroll', 0, total_points - window_size, valinit=0, valstep=1)

    # Call update function when the slider is changed
    slider.on_changed(update)

    # Show the plot in a separate window
    plt.show()

# Main function to handle plotting
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
    window_size = 250  # Number of points to show at once (adjustable)

    # Titles and labels for each plot
    titles = ["Accelerometer X", "Accelerometer Y", "Accelerometer Z",
              "Gyroscope X", "Gyroscope Y", "Gyroscope Z"]
    ylabels = ["Acceleration (g)", "Acceleration (g)", "Acceleration (g)",
               "Rotation (deg/s)", "Rotation (deg/s)", "Rotation (deg/s)"]

    # Data map to assign data to each graph
    data_map = [accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z]

    # Plot each graph in a separate window
    for i in range(6):
        plot_individual_graph(times, data_map[i], titles[i], ylabels[i], window_size)

    # Plot the combined graph (7th graph)
    plot_combined_graph(times, data_map, titles, window_size)

# Ask for file ID (last 4 digits)
file_id = input("Enter the last 4 digits of the sensor data file: ")
file_path = f'sensor_data_{file_id}.csv'

# Check if the file exists before proceeding
if os.path.exists(file_path):
    plot_scrollable_graph(file_path)
else:
    print(f"File 'sensor_data_{file_id}.csv' not found.")
