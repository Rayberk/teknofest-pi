import csv
import time
from mpu6050 import mpu6050
import Adafruit_CharLCD as LCD

# Initialize the MPU6050 sensor
sensor = mpu6050(0x68)

# Initialize the LCD (adjust pins according to your setup)
lcd_rs = 26
lcd_en = 19
lcd_d4 = 13
lcd_d5 = 6
lcd_d6 = 5
lcd_d7 = 11
lcd_columns = 16
lcd_rows = 2

lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)

# Function to write data to a CSV file
def record_gyroscope_data(duration):
    with open('gyroscope_data.csv', mode='w') as file:
        writer = csv.writer(file)
        writer.writerow(['Time', 'Accel_X', 'Accel_Y', 'Accel_Z', 'Gyro_X', 'Gyro_Y', 'Gyro_Z'])

        start_time = time.time()
        while time.time() - start_time < duration:
            accel_data = sensor.get_accel_data()
            gyro_data = sensor.get_gyro_data()

            current_time = time.time() - start_time
            writer.writerow([
                current_time,
                accel_data['x'], accel_data['y'], accel_data['z'],
                gyro_data['x'], gyro_data['y'], gyro_data['z']
            ])
            time.sleep(0.04)

# Display "Recording..." on the LCD
lcd.clear()
lcd.message("Recording...")

# Start recording gyroscope data for 10 seconds
record_duration = 10  # in seconds
record_gyroscope_data(record_duration)

# Display "Done" on the LCD after recording
lcd.clear()
lcd.message("Done")

# Cleanup
lcd.clear()
