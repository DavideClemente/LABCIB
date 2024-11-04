from random import randint

import serial
import time

arduino_port = 'COM6'  # Adjust to your port, e.g., '/dev/ttyUSB0' for Linux
baud_rate = 115200
timeout_duration = .5  # Set timeout duration


def parse_otp_response(response):
    try:
        # Splits and extracts values based on known response structure
        received = int(response.split("got")[1].split(",")[0].strip())
        expected = int(response.split("was expecting")[1].strip())
        return received, expected
    except (IndexError, ValueError) as e:
        print("Error parsing OTP response:", e)
        return None, None


def send_number(number):
    ser.write(f"{number}\n".encode())
    time.sleep(0.1)


def send_number_and_check(arduino, number):
    # Send the number to the Arduino
    arduino.write(f"{number}\n".encode())
    # Wait for Arduino response
    response = arduino.readline().decode().strip()
    # Check if the response matches the expected number
    if response == str(number):
        print(f"Arduino confirmed: {number}")
        return True
    else:
        print(f"Arduino sent unexpected response: {response}")
        return False


def try_find_code(arduino: serial.Serial):  # Initialize serial communication with Arduino
    number_to_send = randint(0, 9999)  # Generate a random number between 0 and 9999
    sent_number = []
    continue_loop = True
    while continue_loop:
        send_number(number_to_send)
        _, expected = parse_otp_response(arduino.readline().decode().strip())
        print(f"Received: {expected}")
        if expected in sent_number:
            # Reverse the list and find the expected number's index
            reversed_sent = sent_number[::-1]
            index = reversed_sent.index(expected)
            next_number = reversed_sent[index - 1]
            send_number(next_number)
            arduino.readline().decode().strip()
            final_code = arduino.readline().decode().strip()
            print(f"Final Code: {final_code}")
            continue_loop = False  # Exit the loop after sending the correct next number
        else:
            sent_number.append(expected)



try:
    with serial.Serial(arduino_port, baud_rate, timeout=timeout_duration) as ser:
        time.sleep(2)
        ready_response = ser.read(1)
        print(f"Arduino Ready: {ready_response}")
        ser.readline()
        time.sleep(2)
        message = (bytes('alanrnwqgcqbtajikqmzoupuetdjesayulsaqmjqwilpuiyqtugieu' + '\n', 'utf-8'))
        print(f'Sending -> {message}')
        ser.write(message)
        response = ser.readline()
        time.sleep(1)
        response = ser.readline()
        while "Password:" not in response.decode():
            response = ser.readline()
        cc_password = (bytes('cncuubhdnjcmrtsjglthosedxqbdiyonkzmglqmtxwpbttirlwdmn' + '\n', 'utf-8'))
        ser.write(cc_password)
        time.sleep(0.1)
        response = ser.readline()
        while "OTP:" not in response.decode():
            response = ser.readline()
        try_find_code(ser)
except serial.SerialException as e:
    print(f"Serial connection error: {e}")
except Exception as e:
    print(f"Error: {e}")
