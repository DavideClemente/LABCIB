import serial
import time
import timeit

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


# Function to send a password guess to Arduino and measure the response
def send_password_guess(password_guess):
    ser.reset_input_buffer()  # Clear serial buffer before sending
    ser.write(f"{password_guess}\n".encode())  # Send the password guess
    return ser.readline().decode().strip()

# Function to time how long it takes to send a password guess and get a response


def measure_response_time(password_guess, repeat=5):
    def wrapper():
        send_password_guess(password_guess)

    # Use timeit to get the average execution time over 'repeat' runs
    return timeit.timeit(wrapper, number=repeat) / repeat

# Function to determine the password length by checking response times for different lengths


def find_password_length(max_length=20):
    # Measure response time for an empty password
    baseline_time = measure_response_time("")
    print(
        f"Baseline response time (empty password): {baseline_time:.6f} seconds")

    potential_lengths = []

    for length in range(1, max_length + 1):
        # Create a password of "a" characters with the current length
        test_password = "a" * length
        response_time = measure_response_time(test_password)

        print(
            f"Password length {length}: Response time = {response_time:.6f} seconds")

        # If response time significantly increases, we've likely found the password length
        if response_time > baseline_time + 0.002:  # Adjust threshold as necessary
            potential_lengths.append(length)
            print(
                f"Possible password length detected at {length}: {response_time:.6f} seconds")

    if potential_lengths:
        # Return the length where the timing difference starts to be significant
        print(f"Detected potential password lengths: {potential_lengths}")
        return potential_lengths[0]  # Return the first detected length

    # If no timing difference is detected, return the max length as fallback
    print("No significant timing difference found.")
    return max_length


try:
    send_data('')  # Skip prompt for password
    time.sleep(2)

    print(f'Arduino says: {read_response()}')

    password_length = find_password_length()

    print(f"Detected password length: {password_length}")

except serial.SerialException as e:
    print(f"Serial connection error: {e}")
finally:
    if ser.is_open:
        ser.close()
