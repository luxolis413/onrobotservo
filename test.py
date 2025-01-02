import serial
import time

def calculate_checksum(packet):
    """
    Calculate the checksum by summing all bytes in the packet
    (except header and checksum itself), performing a bitwise NOT, and keeping the least significant byte.
    """
    checksum = ~sum(packet) & 0xFF
    print("CheckSum: ", checksum)
    packet.insert(4, checksum)
    return checksum

def send_packet(serial_port, packet):
    """
    Send a packet through the serial port.
    """
    checksum = calculate_checksum(packet)
    # Convert the modified data to a formatted string with commas and brackets
    hex_data = "[ " + ", ".join(f"0x{byte:02X}" for byte in packet) + " ]"

    print(f"Modified Data (Hexadecimal Array): {hex_data}")
    print(f"Checksum Byte: 0x{checksum:02X}")
    print(f"Sent: {packet}")

def receive_response(serial_port, buffer_size=64):
    """
    Read the response from the serial port.
    """
    response = serial_port.read(buffer_size)
    print(f"Received: {list(response)}")
    return response

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
        # Turn On the servo
        packet = [0xFF, 0xFE, 0x00, 0x03, 0x25, 0xD7, 0x00 ]
        # Example 1: Set ID0 to 115,200 bps
        packet = [0xFF, 0xFE, 0x00, 0x03, 0xE8, 0x07, 0x0D] 
        send_packet(ser, packet)
        time.sleep(0.1)

        # Example 2: Send Ping to ID0
        packet = [0xFF, 0xFE, 0x00, 0x02, 0x2D, 0xD0]
        send_packet(ser, packet)
        time.sleep(0.1)

        # Example 3: Move to 180 degrees at 5 RPM in CCW
        packet = [0xFF, 0xFE, 0x00, 0x07, 0x2F, 0x01, 0x00, 0x46, 0x50, 0x00, 0x32]
        # time.sleep(5)
        # packet = [0xFF, 0xFE, 0x00, 0x06, 0x98, 0x02, 0x01, 0x8C, 0xA0, 0x32]
        # time.sleep(5)
        #packet = [0xFF, 0xFE, 0x00, 0x06, 0xD9, 0x04, 0xFE, 0xFE, 0x00, 0x20]
        send_packet(ser, packet)
        time.sleep(0.1)

        # Reading response (if any)
        response = receive_response(ser)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        ser.close()

if __name__ == "__main__":
    main()
