#dictionary -->  instruction:(func 3,opcode,func7)
Rtype={
    "add":("000","0110011","0000000"),
    "sub":("000","0110011","0100000"),
    "sll":("001","0110011","0000000"),
    "slt":("010","0110011","0000000"),
    "sltu":("011","0110011","0000000"),
    "xor":("100","0110011","0000000"),
    "srl":("101","0110011","0000000"),
    "or":("110","0110011","0000000"),
    "and":("111","0110011","0000000")
}

#dictionary -->  instruction:(func 3,opcode)
Itype={
    "lw":("010","0000011"),
    "addi":("000","0010011"),
    "sltiu":("011","0010011"),
    "jalr":("000","1100111")
}

#dictionary -->  instruction:(func 3,opcode)
Stype={
    "sw":("010","0100011")
}

#dictionary -->  instruction:(func 3,opcode)
Btype={
    "beq": ("000", "1100011"),
    "bne": ("001", "1100011"),
    "blt": ("100", "1100011"),
    "bge": ("101", "1100011"),
    "bltu": ("110", "1100011"),
    "bgeu": ("111", "1100011")
}

#dictionary -->  instruction:(opcode)
Utype={
    "lui":("0110111"),
    "auipc":("0010111")
}

#dictionary -->  instruction:(opcode)
Jtype={
    "jal":("1101111"),
}


register_address= {
    "zero": "00000",      #zero Hard-wired zero 
    "ra": "00001",      #ra   Return Adress
    "sp": "00010",      #sp   Stack pointer
    "gp": "00011",      #gp   Global pointer
    "tp": "00100",      #tp   Thread pointer
    "t0": "00101",      #t0   Temporary reg

    "t1": "00110",      #t1,t2  temporaries
    "t2": "00111",

    "s0": "01000",      #s0,s1   saved registers
    "fp": "01000",
    "s1": "01001",      

    "a0": "01010",     #a0,a1  Function arguments/ returnvalues
    "a1": "01011",

    "a2": "01100",     #a2-a7  Function Arguments
    "a3": "01101",
    "a4": "01110",#incorrect value assumption
    "a5": "01111",
    "a6": "10000",
    "a7": "10001",

    "s2": "10010",     #s2-s11  saved registers
    "s3": "10011",
    "s4": "10100",
    "s5": "10101",
    "s6": "10110",
    "s7": "10111",
    "s8": "11000",
    "s9": "11001",
    "s10": "11010",
    "s11": "11011",

    "t3": "11100",     #t3-t6    temporatries
    "t4": "11101",
    "t5": "11110",
    "t6": "11111"
}

# *******************************************************

labels={}
# *******************************************************


# *******************************************************
#takes the code as input and passes it line by line 

#pc=0


def imm_to_bin(immediate, bits):
    try:
        if immediate < -(1 << (bits - 1)) or immediate >= (1 << (bits - 1)):
            raise ValueError(f"{immediate} is out of range ")

        binary = ['0'] * bits  # Initialize binary representation with all zeros

        if immediate < 0:
            # Convert negative immediate to two's complement representation
            immediate = (1 << bits) + immediate

        # Convert the immediate value to binary
        for i in range(bits - 1, -1, -1):
            binary[i] = str(immediate & 1)  # Extract least significant bit
            immediate >>= 1  # Right shift to move to the next bit
        
        return ''.join(binary)  # Convert the binary list to a string and return

    except Exception as e:
        print(f"Error: {e}")
        raise ValueError


def scan_labels(text):
    code = text.split("\n")
    for line in code:
        line=line.strip()
        inst = line.split()
        if inst=="":  # Skip empty lines
            continue

        instruction = inst[0].strip('"')
        if instruction[-1] == ':':  # Check if it's a label
            label = instruction[:-1]  # remove : from label name
            labels[label] = None      # replace None with sp when it will be added

def format_code(text):
    code = text.split("\n")
    output=''
    scan_labels(text)

    for line in code:
        # print(line)
        line=line.strip()
        inst = line.split()
        if not inst:  # Skip empty lines
            continue
        
        instruction = inst[0].strip('"')  # Extract the instruction

        if instruction[-1] == ':':  # Check if it's a label
            if len(inst) == 1:
                continue
            else:
                inst = inst[1::]
                instruction=inst[0]

        if len(inst) >= 1:  # Check if there are operands present
            if '(' in inst[1] and ')' in inst[1]:
                x = inst[1].split(",")
                rd = x[0]  # Extract the destination register
                imm, rs1 = x[1].split("(")  
                rs1 = rs1.strip(')').strip('"')  
                operands = [rd, rs1, imm] 
            else:
                operands = inst[1].strip('"').split(",")  # Split the operands directly

               
                if len(operands) < 3:
                    # Pad the operands with None values if necessary
                    operands.extend([None] * (3 - len(operands)))
        else:
            operands=[]

        
        output=output+assembly_language(instruction, operands)
        # if wanna print with space '\n'
    return output



def virtualhalt(file_path):
   #checks the last line of the code and if its a virtual halt returns true otherwise false 
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()  # Read all lines from the file
            last_line = lines[-1].strip()  # Get the last line and remove leading/trailing whitespace
            
            if ':' in last_line:             #if there is a label only consider the part after the colon
                last_instruction = last_line.split(':')[-1].strip()
                return last_instruction == "beq zero,zero,0"
            else:
                return last_line == "beq zero,zero,0"
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return False




# ********************************************************************************

def assembly_language(instruction, operands):

    if instruction in Rtype:
        funct3, opcode, funct7 = Rtype[instruction]

    elif instruction in Itype:
        funct3, opcode = Itype[instruction]

    elif instruction in Stype:
        funct3, opcode = Stype[instruction]

    elif instruction in Btype:
        funct3, opcode = Btype[instruction]

    elif instruction in Utype:
        opcode = Utype[instruction]

    elif instruction in Jtype:
        opcode = Jtype[instruction]

    else:
        return "Error: Instruction Not in ISA"

    binary_operand = []  # to convert operands to binary
          
    for op in operands:
        if op in register_address:
            binary_operand.append(register_address[op])
        else:
            binary_operand.append(op)
    
    
    # Rtype - add rd,rs1,rs2
    if instruction in ["add", "sub", "sll", "slt", "sltu", "xor", "srl", "or", "and"]:
        rd,rs1,rs2=binary_operand

        rtypeval=funct7+rs2+rs1+funct3+rd+opcode
        return rtypeval

    # Itype - jalr rd,rs1,imm       lw rd,imm(rs1)
    elif instruction in ["lw","addi","sltiu","jalr"]:
        rd= binary_operand[0]
        rs1= binary_operand[1]
        imm=imm_to_bin(int(binary_operand[2]),12)
        
        itypeval=imm + rs1 + funct3 + rd + opcode
        return itypeval

    # Stype - sw rs2,imm(rs1)
    elif instruction=="sw":
        rs2= binary_operand[0]
        rs1= binary_operand[1]
        imm=imm_to_bin(int(binary_operand[2]),12)
        
        stypeval=imm[0:7] + rs2 + rs1 + funct3 +imm[7:12] + opcode

        return stypeval


    elif instruction in ["beq", "bne", "blt", "bge", "bltu", "bgeu"]:
        if operands == ["zero", "zero", "0"] and instruction == ["beq"]:
        # Virtual halt instruction detected, return its binary representation
            return "0000000000000000000000000"+opcode  # Binary representation of beq zero,zero,0x00000000
    
        rs1 = binary_operand[0]
        rs2 = binary_operand[1]
        imm = imm_to_bin(int(binary_operand[2]),16)  # Assuming 16-bit immediate value

        # Extract bits from the immediate value
        immsign = imm[0]  # Bit 11
        immfirst = imm[5:11]  # Bits 4 to 1
        immlast = imm[11:]  # Bits 10 to 5

        # Encoding B-type instruction fields
        btypeval     = immsign + immfirst + rs2 + rs1 + funct3 + immlast + opcode

        return btypeval



    # Utype - auipc rd,imm
    
    elif instruction in ["lui","auipc"]:
        rd= binary_operand[0]
        imm=imm_to_bin(int(binary_operand[1]),32)

        utypeval=imm[0:20] + rd + opcode  

        return utypeval

    # Jtype - jal rd,imm
   
    elif instruction=="jal":
        rd= binary_operand[0]
        imm=imm_to_bin(int(binary_operand[1]),20) 
         
        immsign=imm[0]   
        immfirst=imm[9:19]
        immlast=imm[0:9]
        
        jtypeval=immsign[0] + immfirst + immlast + rd + opcode 

        return jtypeval
    # + rd + opcode

# *****************************************************************

# *****************************************************************

input_file = open("input.txt", "r")
output_file = open("output.txt", "w")

# Read the input file
file_path = "input.txt"
with open(file_path, 'r') as input_file:
    lines = input_file.readlines()  # Read all lines from the input file
    
    # Check if the last line contains the Virtual Halt instruction
    if virtualhalt(file_path):
        # If Virtual Halt is found, proceed with conversion
        with open("output.txt", "w") as output_file:
            # Iterate through each line in the input file
            for line in lines:
                # Remove any leading or trailing whitespace
                line = line.strip()
                if not line:
                    continue
                # Call the format_code function and write the formatted line to the output file
                formatted_output = format_code(line)
                print(formatted_output)
                output_file.write(formatted_output + "\n")
        print("Conversion completed successfully.")
    else:
        print("Virtual Halt instruction not found in the last line. Conversion aborted.")


# *****************************************************************

