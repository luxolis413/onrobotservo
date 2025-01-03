packet = [0xFF, 0xFE, 0x00, 0x07, 0x47, 0x01, 0x01, 0x00, 0x64]
hex_values = [0x13, 0x88]

# Insert the values at positions 7 and 8
packet[7:7] = hex_values

# Display the packet with hexadecimal formatting
print("[" + ", ".join(hex(x) for x in packet) + "]")
