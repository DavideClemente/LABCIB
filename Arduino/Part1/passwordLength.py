import serial
import time
import itertools
import string

# Configure serial connection
arduino_port = 'COM10'  # Adjust to your port, e.g., '/dev/ttyUSB0' for Linux
baud_rate = 115200
timeout_duration = 1  # Set timeout duration

ser = serial.Serial(arduino_port, baud_rate, timeout=timeout_duration)
time.sleep(2)


def send_data(string):
    ser.write(bytes(string + '\n', 'utf-8'))
    time.sleep(0.1)


def read_response():
    return ser.readline().decode('utf-8').strip()


try:
    send_data('')  # Skip prompt for password
    time.sleep(2)

    print(f'Arduino says: {read_response()}')

except serial.SerialException as e:
    print(f"Serial connection error: {e}")
finally:
    if ser.is_open:
        ser.close()