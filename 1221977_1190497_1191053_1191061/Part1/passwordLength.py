import serial
import time
import matplotlib.pyplot as plt
from collections import defaultdict

# Configure serial connection
arduino_port = 'COM6'  # Adjust to your port, e.g., '/dev/ttyUSB0' for Linux
baud_rate = 115200
timeout_duration = 0.1  # Increased timeout for better stability
plt.switch_backend('TkAgg')  # or 'Agg' if running headless (without GUI)
iterations = 50


# Function to measure response time from sending data to receiving the full response
def measure_response_time(data, arduino: serial.Serial):
    try:
        arduino.reset_input_buffer()  # Clear the serial buffer
        arduino.reset_output_buffer()
        message = (bytes(data + '\n', 'utf-8'))
        start_time = time.time()
        arduino.write(message)  # Send data to Arduino
        while arduino.in_waiting == 0:
            continue
        end_time = time.time()
        elapsed_time = end_time - start_time
        response = arduino.readline().decode('utf-8').strip()
        arduino.readline()
        print(f"Sent: {data}, Received: {response}, Time: {elapsed_time:.6f} seconds")
        return elapsed_time
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


# Function to record response times for each string length across multiple iterations
def record_response_times(password_length, reader: serial.Serial = None, samples_per_iteration=5):
    times_per_length = defaultdict(list)
    for _ in range(iterations):
        print(f"Iteration: {_ + 1}/{iterations}")
        for length in password_length:
            test_string = "a" * length  # Create a string of 'a's with the current length
            times = []
            for _ in range(samples_per_iteration):
                elapsed_time = measure_response_time(test_string, reader)
                if elapsed_time:
                    times.append(elapsed_time)
            filtered_times = remove_outliers(times)
            avg_time = sum(filtered_times) / len(filtered_times)
            print(f"String Length: {length}, Avg. Time: {avg_time:.6f} seconds")
            times_per_length[length].append(avg_time)
    return times_per_length


# Main function with Arduino connection management
try:
    with serial.Serial(arduino_port, baud_rate, timeout=timeout_duration) as ser:
        time.sleep(2)  # Allow time for Arduino to initialize

        baselineMessage = (bytes("" + '\n', 'utf-8'))
        ser.write(baselineMessage)  # Send data to Arduino
        ready_response = ser.read(1)
        print(f"Arduino Ready: {ready_response}")
        time.sleep(2)
        lengths = range(1, 21)  # String lengths from 1 to 20
        response_times_per_length = record_response_times(lengths, ser)

        # Dictionary to store total points for each string length
        points_per_length = {length: 0 for length in lengths}

        for i in range(iterations):
            iteration_times = {length: response_times_per_length[length][i] for length in lengths}

            sorted_lengths = sorted(iteration_times.items(), key=lambda x: x[1])

            # print the slowest of each iteration
            slowest_length, slowest_time = sorted_lengths[-1]
            print(f'\nIteration {i + 1} - Slowest string length is {slowest_length} with {slowest_time:.6f} seconds.')

            # Assign points (1 for fastest, 20 for slowest)
            for rank, (length, _) in enumerate(sorted_lengths, start=1):
                points_per_length[length] += rank  # The higher the rank, the fewer points (slower = more points)

        # Sort lengths by total points (the ones with the least points are the fastest on average)
        sorted_by_points = sorted(points_per_length.items(), key=lambda x: x[1])

        slowest_length, slowest_points = sorted_by_points[-1]
        print(f'\nThe slowest string length is {slowest_length} with {slowest_points} points.')

        # Print results
        print("String Lengths sorted by their total points (least points = fastest on average):")
        for length, points in sorted_by_points:
            print(f'String Length {length}: {points} points')

        lengths, total_points = zip(*sorted_by_points)

        # Plot the graph of total points vs string length
        plt.figure(figsize=(10, 6))
        plt.bar(lengths, total_points, color='b', label="Total Points (Less = Faster)")

        # Add titles and labels
        plt.title("Total Points vs String Length (Lower Points = Faster on Average)")
        plt.xlabel("String Length")
        plt.ylabel("Total Points")

        plt.xticks(range(1, 21))
        plt.grid(True)

        # Show the legend and plot
        plt.legend()
        plt.show()

except serial.SerialException as e:
    print(f"Serial connection error: {e}")
except Exception as e:
    print(f"Error: {e}")
