import time
import csv
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import mpu6050
import random
import string
import signal
import sys

sensor = mpu6050.mpu6050(0x68, bus=1)

def get_sensor_data():
    # Read accelerometer and gyroscope data
    accel_data = sensor.get_accel_data()
    gyro_data = sensor.get_gyro_data()
    
    # Scale accelerometer raw values to g-forces
    accel_x = accel_data["x"] 
    accel_y = accel_data["y"] 
    accel_z = accel_data["z"] 
    
    # Get gyroscope data (degrees per second)
    gyro_x = gyro_data["x"] 
    gyro_y = gyro_data["y"] 
    gyro_z = gyro_data["z"] 
    
    return accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z

# Data collection setup
sample_rate = 1 / 25  # 25 samples per second
time_window = 10      # 10 seconds of data for the graph
data_length = int(25 * time_window)

# Initialize lists for storing data
times = [0] * data_length
accel_x_data = [0] * data_length
accel_y_data = [0] * data_length
accel_z_data = [0] * data_length
gyro_x_data = [0] * data_length
gyro_y_data = [0] * data_length
gyro_z_data = [0] * data_length

# Initialize the plot
fig, axes = plt.subplots(2, 3, figsize=(12, 8))  # 2x3 grid

# Flatten the axes for easy indexing
axes = axes.flatten()

# Setting up titles and labels
titles = ["Accelerometer X-axis", "Accelerometer Y-axis", "Accelerometer Z-axis", 
          "Gyroscope X-axis", "Gyroscope Y-axis", "Gyroscope Z-axis"]
ylabels = ["Acceleration (g)", "Acceleration (g)", "Acceleration (g)", 
           "Rotation (deg/s)", "Rotation (deg/s)", "Rotation (deg/s)"]

lines = []
for i, ax in enumerate(axes):
    ax.set_title(titles[i])
    ax.set_xlabel("Time (s)")
    ax.set_ylabel(ylabels[i])
    ax.set_ylim([-2, 2] if i < 3 else [-250, 250])
    lines.append(ax.plot(times, [0] * data_length, 'r-')[0])

# Function to update the plot data
def update_graph(frame):
    global times, accel_x_data, accel_y_data, accel_z_data, gyro_x_data, gyro_y_data, gyro_z_data

    # Get new sensor data
    accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z = get_sensor_data()
    
    # Append the new data
    times.append(time.time() - start_time)
    accel_x_data.append(accel_x)
    accel_y_data.append(accel_y)
    accel_z_data.append(accel_z)
    gyro_x_data.append(gyro_x)
    gyro_y_data.append(gyro_y)
    gyro_z_data.append(gyro_z)

    # Keep only the last 'data_length' points
    times = times[-data_length:]
    accel_x_data = accel_x_data[-data_length:]
    accel_y_data = accel_y_data[-data_length:]
    accel_z_data = accel_z_data[-data_length:]
    gyro_x_data = gyro_x_data[-data_length:]
    gyro_y_data = gyro_y_data[-data_length:]
    gyro_z_data = gyro_z_data[-data_length:]

    # Update the line data for the plot
    lines[0].set_data(times, accel_x_data)
    lines[1].set_data(times, accel_y_data)
    lines[2].set_data(times, accel_z_data)
    lines[3].set_data(times, gyro_x_data)
    lines[4].set_data(times, gyro_y_data)
    lines[5].set_data(times, gyro_z_data)

    # Adjust the x-axis limits to always show the last 'time_window' seconds
    for ax in axes:
        ax.set_xlim([times[0], times[-1]])

    return lines

# Generate a unique ID for the CSV file
def generate_unique_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))

# Save data to CSV
def save_data_to_csv():
    unique_id = generate_unique_id()
    filename = f'sensor_data_{unique_id}.csv'
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Time", "Accel X", "Accel Y", "Accel Z", "Gyro X", "Gyro Y", "Gyro Z"])
        for i in range(len(times)):
            writer.writerow([times[i], accel_x_data[i], accel_y_data[i], accel_z_data[i],
                             gyro_x_data[i], gyro_y_data[i], gyro_z_data[i]])
    print(f"Data saved to {filename}")

# Function to handle clean up on exit
def handle_exit(signum, frame):
    print("Shutting down sensor and saving data...")
    save_data_to_csv()
    plt.close(fig)
    sys.exit(0)

# Handle shutdown on interrupt (Ctrl+C) or close event
signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)

# Start time for the x-axis
start_time = time.time()

# Animate the graphs, updating every 40ms (~25 fps)
ani = FuncAnimation(fig, update_graph, interval=40)

# CSV saving functionality on window close
def on_close(event):
    save_data_to_csv()

# Connect the window close event to the save function
fig.canvas.mpl_connect('close_event', on_close)

# Display the plot
plt.tight_layout()
plt.show()
