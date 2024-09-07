import time
import csv
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import mpu6050
import random
import string
import signal
import sys
import threading

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

# Function
