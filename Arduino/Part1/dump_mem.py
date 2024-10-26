import base64
import serial
import time

# Serial port configuration (adjust these parameters)
# For Windows use 'COMx' (e.g., 'COM3'), for Linux/Mac use '/dev/ttyUSB0'
SERIAL_PORT = 'COM11'
BAUD_RATE = 115200     # Adjust to match the Arduino's baud rate
TIMEOUT = 1            # Timeout for serial response (seconds)

# File to save the memory dump
OUTPUT_FILE = 'memory_dump.bin'


def dump_memory():
    try:
        # Open the serial port
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)
        time.sleep(2)
        print(f'Arduino Says -> {ser.readline()}')

        message = (bytes('dankmlacoguqo' + '\n', 'utf-8'))
        print(f'Sending -> {message}')
        ser.write(message)

        # Give the Arduino time to reset and prepare the command
        time.sleep(2)  # Wait for Arduino to be ready (optional)

        print(f'Arduino Says -> {ser.readline()}')

        print("Waiting for the menu to appear...")
        while True:
            line = ser.readline().decode('utf-8', errors='ignore')  # Read line by line
            print(line.strip())

            # Check if the menu has appeared
            if 'DEVELOPMENT MENU' in line:
                print("Found the menu, proceeding with memory dump.")
                break  # Exit the loop and proceed
        for i in range(3):
            print(f'Arduino Says -> {ser.readline()}')

        # Chose option from developer menu

        message = (bytes('1' + '\n', 'utf-8'))
        ser.write(message)
        time.sleep(1)

        for i in range(6):
            print(f'Arduino Says -> {ser.readline()}')

        # Chose memory location to dump
        # 0 - PROGMEM
        # 1 - EEPROM
        # 2 - SRAM

        message = (bytes('2' + '\n', 'utf-8'))
        ser.write(message)
        time.sleep(1)

        # Open a binary file for writing
        with open('memory_dump.bin', 'wb') as f:
            print("Writing memory contents to binary file...")
            while True:
                data = ser.readline()  # Read in chunks of 1024 bytes
                try:
                    if 'DEVELOPMENT MENU' in data.decode('utf-8'):
                        break
                except:
                    continue
                finally:
                    f.write(data)

        print("Memory dump complete.")

    except serial.SerialException as e:
        print(f"Error: {e}")
    finally:
        # Close the serial connection
        if ser.is_open:
            ser.close()


if __name__ == "__main__":
    dump_memory()
