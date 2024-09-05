import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import mpu6050

sensor = mpu6050.mpu6050(0x68, bus=1)


def get_accel_data():
    # Read accelerometer raw values and scale to g-forces
    accel_x = mpu6050.get_accel_data().x / 16384.0
    accel_y = mpu6050.get_accel_data().y / 16384.0
    accel_z = mpu6050.get_accel_data().z / 16384.0
    return accel_x, accel_y, accel_z

# Data collection setup
sample_rate = 1 / 25  # 25 samples per second
time_window = 10      # 10 seconds of data for the graph
data_length = int(25 * time_window)

# Initialize lists for storing data
times = [0] * data_length
accel_x_data = [0] * data_length
accel_y_data = [0] * data_length
accel_z_data = [0] * data_length

# Initialize the plot
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8))

ax1.set_title("Accelerometer X-axis")
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Acceleration (g)")
ax1.set_ylim([-2, 2])

ax2.set_title("Accelerometer Y-axis")
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Acceleration (g)")
ax2.set_ylim([-2, 2])

ax3.set_title("Accelerometer Z-axis")
ax3.set_xlabel("Time (s)")
ax3.set_ylabel("Acceleration (g)")
ax3.set_ylim([-2, 2])

# Create line objects for the graphs
line_x, = ax1.plot(times, accel_x_data, 'r-')
line_y, = ax2.plot(times, accel_y_data, 'g-')
line_z, = ax3.plot(times, accel_z_data, 'b-')

def update_graph(frame):
    global times, accel_x_data, accel_y_data, accel_z_data

    # Get new accelerometer data
    accel_x, accel_y, accel_z = get_accel_data()
    
    # Update the data lists
    times.append(time.time() - start_time)
    accel_x_data.append(accel_x)
    accel_y_data.append(accel_y)
    accel_z_data.append(accel_z)

    # Keep only the last 'data_length' points
    times = times[-data_length:]
    accel_x_data = accel_x_data[-data_length:]
    accel_y_data = accel_y_data[-data_length:]
    accel_z_data = accel_z_data[-data_length:]

    # Update the line data for the plot
    line_x.set_data(times, accel_x_data)
    line_y.set_data(times, accel_y_data)
    line_z.set_data(times, accel_z_data)

    # Adjust the x-axis limits to always show the last 'time_window' seconds
    ax1.set_xlim([times[0], times[-1]])
    ax2.set_xlim([times[0], times[-1]])
    ax3.set_xlim([times[0], times[-1]])

    return line_x, line_y, line_z

# Start time for the x-axis
start_time = time.time()

# Animate the graphs, updating every 40ms (~25 fps)
ani = FuncAnimation(fig, update_graph, interval=40)

# Display the plot
plt.tight_layout()
plt.show()
