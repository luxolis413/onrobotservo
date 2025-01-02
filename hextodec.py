# Function to convert Hexadecimal to Decimal
def hex_to_decimal(hex_num):
    return int(hex_num, 16)

# Function to convert Decimal to Hexadecimal
def decimal_to_hex(decimal_num):
    return hex(decimal_num)

# Function to convert arrays of Hexadecimal to Decimal
def convert_hex_array_to_decimal(hex_array):
    return [hex_to_decimal(h) for h in hex_array]

# Function to convert arrays of Decimal to Hexadecimal
def convert_decimal_array_to_hex(decimal_array):
    return [decimal_to_hex(d) for d in decimal_array]

# Taking input from the user for an array of hexadecimal numbers
hex_array_input = input("Enter an array of Hexadecimal numbers (comma-separated): ")
hex_array = hex_array_input.split(',')

# Convert Hexadecimal array to Decimal array
decimal_result_array = convert_hex_array_to_decimal(hex_array)
print(f"Hexadecimal to Decimal conversion: {decimal_result_array}")

# Taking input from the user for an array of decimal numbers
decimal_array_input = input("Enter an array of Decimal numbers (comma-separated): ")
decimal_array = [int(d) for d in decimal_array_input.split(',')]

# Convert Decimal array to Hexadecimal array
hex_result_array = convert_decimal_array_to_hex(decimal_array)
print(f"Decimal to Hexadecimal conversion: {hex_result_array}")

def calculate_checksum(packet):
    """
    Calculate the checksum by summing all bytes in the packet
    (except header and checksum itself), performing a bitwise NOT, and keeping the least significant byte.
    """
    checksum = ~sum(packet[2:]) & 0xFF
    return checksum
