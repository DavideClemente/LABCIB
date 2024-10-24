import base64
import serial
import time

# Serial port configuration (adjust these parameters)
SERIAL_PORT = 'COM7'  # For Windows use 'COMx' (e.g., 'COM3'), for Linux/Mac use '/dev/ttyUSB0'
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
            print(line.strip())  # (Optional) Print the user agreement or other output

            # Check if the menu has appeared
            if 'DEVELOPMENT MENU' in line:
                print("Found the menu, proceeding with memory dump.")
                break  # Exit the loop and proceed
        for i in range(3):
            print(f'Arduino Says -> {ser.readline()}')

        message = (bytes('1' + '\n', 'utf-8'))
        ser.write(message)
        time.sleep(1)
        
        for i in range(6):
            print(f'Arduino Says -> {ser.readline()}')
        #print(f'Arduino Says -> {ser.readline()}')
        #print(f'Arduino Says -> {ser.readline()}')
        
        message = (bytes('1' + '\n', 'utf-8'))
        ser.write(message)
        time.sleep(1)
        print(f'Arduino Says -> {ser.readline()}')
        print(f'Arduino Says -> {ser.readline()}')

        # Send the command to dump memory (replace with your command, e.g., '1')
        #ser.write(b'1')  # Sending the command '1' to trigger memory dump
        
        # Open the file to save the dump
        # with open(OUTPUT_FILE, 'wb') as f:
        while True:
            print(ser.readall())  # Read line by line
          # Read line by line

            # Check if the menu has appeared
            # try:
            #     if 'DEVELOPMENT MENU' in line.decode('utf-8'):
            #         print("Found the menu, proceeding with memory dump.")
            #         break  # Exit the loop and proceed
            # except:
            #     pass
            # finally:
            #f.write(line)
        
        print("Memory dump complete.")
        
    except serial.SerialException as e:
        print(f"Error: {e}")
    finally:
        # Close the serial connection
        if ser.is_open:
            ser.close()

def binary_to_ascii(file_path):
    with open(file_path, 'rb') as binary_file:
        # Read the binary file
        binary_data = binary_file.read()

        # Decode the binary data into ASCII, ignoring errors
        ascii_data = binary_data.decode('base64', errors='ignore')

        print(ascii_data)

def binary_to_base64(file_path, output_file='memory_dump_base64.txt'):
    # Read the binary file
    with open(file_path, 'rb') as binary_file:
        binary_data = binary_file.read()

        # Encode the binary data to Base64
        base64_encoded = base64.b64encode(binary_data)

        # Convert the Base64 bytes to a string
        base64_string = base64_encoded.decode('utf-8')

        # Write the Base64 string to a text file (optional)
        with open(output_file, 'w') as out_file:
            out_file.write(base64_string)

        print(f"Base64 encoding complete. Output saved to {output_file}")




if __name__ == "__main__":
    dump_memory()
    # Use the function on your memory dump
    binary_to_base64('memory_dump.bin')
