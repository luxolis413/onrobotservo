import serial
import time

def calculate_checksum(packet):
    """
    Calculate the checksum by summing all bytes in the packet
    (except header and checksum itself), performing a bitwise NOT, and keeping the least significant byte.
    """
    checksum = ~sum(packet[2:]) & 0xFF
    return checksum

def send_packet(serial_port, packet):
    """
    Send a packet through the serial port.
    """
    checksum = calculate_checksum(packet)
    packet.append(checksum)
    serial_port.write(bytearray(packet))
    print(f"Sent: {packet}")

def receive_response(serial_port, buffer_size=64):
    """
    Read the response from the serial port.
    """
    response = serial_port.read(buffer_size)
    print(f"Received: {list(response)}")
    return response

def rotate(serial_port, direction, degrees, speed):
    """
    Rotate the device to a specific position.
    :param serial_port: Serial port object.
    :param direction: 0x01 (CW) or 0x00 (CCW).
    :param degrees: Degrees to rotate.
    :param speed: Speed in 0.1 RPM units.
    """
    position = int(degrees * 100)  # Convert to 0.01-degree units
    position_high = (position >> 8) & 0xFF
    position_low = position & 0xFF
    speed_high = (speed >> 8) & 0xFF
    speed_low = speed & 0xFF

    # Construct packet
    packet = [
        0xFF, 0xFE,  # Header
        0x00,        # Device ID
        0x07,        # Data size
        0x2F,        # Mode: Position Control
        0x01,        # Mode for Position and Speed
        direction,   # Direction: 0x01 = CW, 0x00 = CCW
        position_high, position_low,  # Target position
        speed_high, speed_low         # Speed
    ]
    send_packet(serial_port, packet)
    time.sleep(2)  # Wait for movement to complete
    return receive_response(serial_port)

def main():
    # Configure the serial port
    ser = serial.Serial(
        port='COM9',          # Update to your serial port
        baudrate=115200,      # Communication speed
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=1
    )

    if not ser.is_open:
        ser.open()

    try:
        # Rotate 90° CW
        print("Rotating 90° CW...")
        rotate(ser, direction=0x01, degrees=90, speed=50)  # Speed = 5.0 RPM

        # Rotate 90° CCW
        print("Rotating 90° CCW...")
        rotate(ser, direction=0x00, degrees=90, speed=50)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        ser.close()

if __name__ == "__main__":
    main()
