def calculate_checksum(data_bytes):
    checksum = ~sum(data_bytes[2:]) & 0xFF
    return checksum

# Example usage
#data = [0xFF, 0xFE, 0x00, 0x07, 0x01, 0x00, 0x46, 0x50, 0x00, 0x32]  # Original data 180 cw
data = [0xFF, 0xFE, 0x00, 0x07, 0x01, 0x01, 0x46, 0x50, 0x00, 0x32]
#data = [0xFF, 0xFE, 0x00, 0x03, 0x07, 0x0D]  # 115200
#data = [0xFF, 0xFE, 0x00, 0x02,  0xD0] # ping

# Calculate the checksum
checksum_byte = calculate_checksum(data)

# Insert the checksum byte at the 5th position (index 4)
data.insert(4, checksum_byte)

# Convert the modified data to a formatted string with commas and brackets
hex_data = "[ " + ", ".join(f"0x{byte:02X}" for byte in data) + " ]"

print(f"Modified Data (Hexadecimal Array): {hex_data}")
print(f"Checksum Byte: 0x{checksum_byte:02X}")
