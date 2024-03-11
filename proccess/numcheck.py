# x=len("11000000001111111111")
# z=11000000000111111111
# y=11000000000111111111
# print(z==y)
# print(x)

# def imm_to_bin(immediate, bits):
#     binary=[]
#     for i in range(bits):
#         binary.append(0)
    
#     if immediate < 0:
#         immediate=(2**bits +immediate)

#     i=bits-1
#     while (immediate!=0 and i>=0):
#         binary[i]=immediate%2
#         immediate=immediate//2
#         i-=1

#     b=""
#     for i in binary:
#         b+=str(i)
    
#     return b


# def extend_to_20_bits(number):
#     if number >= 0:
#         # Convert positive number to binary and extend to 20 bits
#         binary_str = format(number, '020b')
#     else:
#         # Convert negative number to binary and apply two's complement
#         binary_str = format((1 << 20) + number, '020b')
    
#     return binary_str

# print(imm_to_bin(20,-20))
# print(extend_to_20_bits(-20))



def check_for_virtual_halt_in_file(file_path):
    """
    Checks if the last line of the code in the file contains the Virtual Halt instruction (beq zero, zero, 0).
    Returns True if found, False otherwise.
    """
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()  # Read all lines from the file
            last_line = lines[-1].strip()  # Get the last line and remove leading/trailing whitespace
            
            # Check if the last line matches the Virtual Halt instruction
            return last_line == "beq zero,zero,0"
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return False

print(check_for_virtual_halt_in_file("input.txt"))