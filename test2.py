import serial
import time

def calculate_checksum(packet):
    checksum = ~sum(packet[2:]) & 0xFF
    return checksum

def send_packet(serial_port, packet):
    # checksum = calculate_checksum(packet)
    # packet.append(checksum)
    serial_port.write(bytearray(packet))
    print(f"Sent: {packet}")

def receive_response(serial_port, buffer_size=64):
    response = serial_port.read(buffer_size)
    print(f"Received: {list(response)}")
    return response

def reset_device(serial_port):
    # Reset command (example, update as needed)
    reset_packet = [0xFF, 0xFE, 0x00, 0x02, 0xF1, 0x0C]
    send_packet(serial_port, reset_packet)
    time.sleep(0.5)

def CCW_180(serial_port):
    # Reset command (example, update as needed)
    reset_packet = [0xFF, 0xFE, 0x00, 0x07, 0x2F, 0x01, 0x00, 0x46, 0x50, 0x00, 0x32]
    send_packet(serial_port, reset_packet)
    time.sleep(0.5)

def CW_180(serial_port):
    # Reset command (example, update as needed)
    reset_packet = [0xFF, 0xFE, 0x00, 0x07, 0x2E, 0x01, 0x01, 0x46, 0x50, 0x00, 0x32]
    send_packet(serial_port, reset_packet)
    time.sleep(0.5)

def CW_360(serial_port):
    # Reset command (example, update as needed)
    reset_packet = [ 0xFF, 0xFE, 0x00, 0x06, 0x98, 0x02, 0x01, 0x8C, 0xA0, 0x32]
    send_packet(serial_port, reset_packet)
    time.sleep(0.5)

def main():
    ser = serial.Serial(
        port='COM10',          # Update with your COM port
        baudrate=115200,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=1
    )

    try:
        # Ensure the serial port is open
        if not ser.is_open:
            ser.open()

        print("Resetting device...")
        reset_device(ser)
        

        # Example 1: Set ID0 to 115,200 bps
        print("Setting ID0 to 115,200 bps...")
        packet = [0xFF, 0xFE, 0x00, 0x03, 0xE8, 0x07, 0x0D]
        send_packet(ser, packet)
        time.sleep(0.1)

        # Example 2: Send Ping to ID0
        print("Sending Ping to ID0...")
        packet = [0xFF, 0xFE, 0x00, 0x02, 0x2D, 0xD0]
        send_packet(ser, packet)
        time.sleep(0.1)


        CCW_180(ser)
        time.sleep(10)
        reset_device(ser)

        CW_180(ser)
        time.sleep(10)
        #CW_360(ser)
       
        print("Receiving response...")
        response = receive_response(ser)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if ser.is_open:
            ser.close()
        print("Serial port closed.")

if __name__ == "__main__":
    main()
