import serial
import time

def dec_hex(number):
    
    hexadecimal_value = hex(number)
    num = int(hexadecimal_value, 16)

# Extract the two bytes
    first_part = (num >> 8) & 0xFF  # Extract the first byte (most significant byte)
    second_part = num & 0xFF  # Extract the second byte (least significant byte)

# Store the result in a list of integers
    angle_byte = [first_part, second_part]
    print(angle_byte)
    return angle_byte

def calculate_checksum(packet):
    """
    Calculate the checksum by summing all bytes in the packet
    (except header and checksum itself), performing a bitwise NOT, and keeping the least significant byte.
    """
    checksum = ~sum(packet) & 0xFF
    print("CheckSum: ", checksum)
    return checksum

def send_packet(serial_port, packet):
    serial_port.write(bytearray(packet))
    print(f"Sent: {packet}")

def receive_response(serial_port, buffer_size=64):
    """
    Read the response from the serial port.
    """
    response = serial_port.read(buffer_size)
    print(f"Received: {list(response)}")
    return response

def reset_device(serial_port):
    # Reset command (example, update as needed)
    reset_packet = [0xFF, 0xFE, 0x00, 0x02, 0xF1, 0x0C]
    send_packet(serial_port, reset_packet)
    time.sleep(0.5)

def bps_115200(serial_port):
    reset_packet = [0xFF, 0xFE, 0x00, 0x03, 0xE8, 0x07, 0x0D]
    send_packet(serial_port, reset_packet)
    time.sleep(0.5)

def ping_IDO(serial_port):
    reset_packet = [0xFF, 0xFE, 0x00, 0x02, 0x2D, 0xD0]
    send_packet(serial_port, reset_packet)
    time.sleep(0.5)
def CCW_90(serial_port):
    # Reset command (example, update as needed)
    packet = [0xFF, 0xFE, 0x00, 0x07, 0x47, 0x01, 0x01, 0x00, 0x64]
    number = int(input("Enter the decimal Number:  "))*100
    angle_byte = dec_hex(number)
    packet[7:7] = angle_byte
    print(angle_byte)
    formatted_packet = "[" + ", ".join(hex(x) for x in packet) + "]"
    checksum_byte = calculate_checksum(formatted_packet)
    packet.insert(4, checksum_byte)
    reset_packet = "[ " + ", ".join(f"0x{byte:02X}" for byte in packet) + " ]"
    
    send_packet(serial_port, reset_packet)
    time.sleep(3)

def CW_90(serial_port):
    # Reset command (example, update as needed)
    reset_packet = [0xFF, 0xFE, 0x00, 0x07, 0x48, 0x01, 0x00, 0x23, 0x28, 0x00, 0x64]
    send_packet(serial_port, reset_packet)
    time.sleep(3)
def CCW_180(serial_port):
    # Reset command (example, update as needed)
    reset_packet = [0xFF, 0xFE, 0x00, 0x07, 0xFD, 0x01, 0x00, 0x46, 0x50, 0x00, 0x64]
    send_packet(serial_port, reset_packet)
    time.sleep(1)

def CW_180(serial_port):
    # Reset command (example, update as needed)
    reset_packet = [0xFF, 0xFE, 0x00, 0x07, 0xFC, 0x01, 0x01, 0x46, 0x50, 0x00, 0x64]
    send_packet(serial_port, reset_packet)
    time.sleep(1)

def CW_360(serial_port):
    # Reset command (example, update as needed)
    reset_packet = [ 0xFF, 0xFE, 0x00, 0x06, 0x98, 0x02, 0x01, 0x8C, 0xA0, 0x32]
    send_packet(serial_port, reset_packet)
    time.sleep(0.5)

def main():
    # Configure the serial port
    ser = serial.Serial(
        port='COM10',          # Update to your serial port (e.g., COM1, COM2, etc.)
        baudrate=115200,      # Communication speed
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=1
    )

    if not ser.is_open:
        ser.open()

    try:
         # Ensure the serial port is open
        if not ser.is_open:
            ser.open()

        print("Resetting device...")
        reset_device(ser)
        time.sleep(1)
        bps_115200(ser)
        time.sleep(1)
        ping_IDO(ser)
        time.sleep(1)
        
        CCW_90(ser)
        time.sleep(5)
        reset_device(ser)

        CW_90(ser)
        time.sleep(5)
        #CW_360(ser)
       
        print("Receiving response...")
        response = receive_response(ser)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        ser.close()

if __name__ == "__main__":
    main()
