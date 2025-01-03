# Using the hex function
decimal_number = int(input("Enter the decimal Number: ")) * 100  # Input and multiply by 100
hexadecimal_value = hex(decimal_number)  # Convert decimal to hex (string)
print("Hexadecimal value:", hexadecimal_value)  # Print the hexadecimal string

# Convert the hexadecimal string back to an integer (excluding '0x' prefix)

num = int(hexadecimal_value, 16)

# Extract the two bytes
first_part = (num >> 8) & 0xFF  # Extract the first byte (most significant byte)
second_part = num & 0xFF  # Extract the second byte (least significant byte)

# Store the result in a list of integers
angle_byte = [first_part, second_part]

# Example packet
packet = [0xFF, 0xFE, 0x00, 0x07, 0x47, 0x01, 0x01, 0x00, 0x64]

# Insert the angle bytes into the packet at position 7
packet[7:7] = angle_byte
print(angle_byte)

# Display the packet with hexadecimal formatting
formatted_packet = "[" + ", ".join(hex(x) for x in packet) + "]"
print(formatted_packet)
