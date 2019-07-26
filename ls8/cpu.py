"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU. """
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 0xF4
        self.FL = None

    # pop code 0b01000110
    # push code 01000101
    # prn code 

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR
        
    def handleStackPush(self):
        self.sp -= 1
        regNum = self.ram[self.pc + 1]
        value = self.reg[regNum]
        self.ram[self.sp] = value


    def handleStackPop(self):
        value = self.ram[self.sp]
        regNum = self.ram[self.pc + 1]
        self.reg[regNum] = value
        self.sp += 1

    def handleCALL(self, operand_1):
        return_address = self.pc + 2
        self.sp -= 1
        self.ram[self.sp] = return_address
 
        register_num = self.ram[self.pc + 1]
        subroutine_address = self.reg[register_num]
 
        self.pc = subroutine_address


    def load(self):
        """Load a program into memory."""

        address = 0

        lines = None

        try:
            lines = open(sys.argv[1]).readlines()

        except FileNotFoundError:
            print(f"{sys.argv[1]} Not Found.")
            sys.exit(2)

        for line in lines:
            if line[0].startswith('0') or line[0].startswith('1'):
                # print(line[:8]) #Prints the binary number
                # print(int(line[:8], 2), "binary converter") #converts the binary numbers on the page into normal numbers
                #normal numbers are then added to the ram at the index/address and the index increments.
                self.ram[address] = int(line[:8], 2)
                address += 1

    def alu(self, op, reg_a = None, reg_b = None):
        """ALU operations."""

        ADD = 0b10100000
        SUB = 0b10100001
        MUL = 0b10100010
        DIV = 0b10100011
        CMP = 0b10100111

        if op == ADD:
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        elif op == SUB:
            self.reg[reg_a] -= self.reg[reg_b]

        elif op == MUL:
            self.reg[reg_a] *= self.reg[reg_b]

        elif op == DIV:
            if self.reg[reg_b] == 0:
                print("Error: You are not allowed to divide a number by 0.")
                sys.exit()
            else:
                self.reg[reg_a] /= self.reg[reg_b]
        # `FL` bits: `00000LGE`
        # Equal = E 1 otherwise 0
        # A < B = L 1 otherwise 0
        # A > B = G 1 otherwise 0
        elif op == CMP:
            if self.reg[reg_a] == self.reg[reg_b]:
                self.FL = 0b00000001
                    
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.FL = 0b00000010
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.FL = 0b00000100

        else:
            raise Exception("Unsupported ALU operation")


    def RET(self):
        return_address = self.ram[self.sp]
 
        self.pc = return_address

    def JMP(self, operand_1):
        self.pc = self.reg[operand_1]

    def JEQ(self, operand_1, instruction):
        if self.FL == 1:
            self.JMP(operand_1)
        else:
            self.pc += 1 + instruction

    def JNE(self, operand_1, instruction):
        if self.FL != 1:
            self.JMP(operand_1)
        else:
            self.pc += 1 + instruction
     
    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            self.FL,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        on = True

        LDI = 0b10000010
        PRN = 0b01000111

        HLT = 0b00000001
        POP = 0b01000110
        PUSH= 0b01000101
        CALL= 0b01010000
        RET = 0b00010001

        JMP = 0b01010100
        JEQ = 0b01010101
        JNE = 0b01010110

        while on:
            IR = self.ram[self.pc]

            # Meanings of the bits in the first byte of each instruction: `AABCDDDD`

            # * `AA` Number of operands for this opcode, 0-2
            # * `B` 1 if this is an ALU operation
            # * `C` 1 if this instruction sets the PC
            # * `DDDD` Instruction identifier

            # get next two MDR's from the next two MAR's stored in ram incase instructions need it
            operand_1 = self.ram_read(self.pc + 1)
            operand_2 = self.ram_read(self.pc + 2)
            instruction = (IR >> 6)

                # Check LDI instruction
            alu_number = (IR & 0b00100000) >> 5

            if alu_number == 1:
                self.alu(IR, operand_1, operand_2)
                self.pc += 1 + instruction     

            elif IR == LDI:
                self.reg[operand_1] = operand_2
                self.pc += 1 + instruction

            elif IR == PRN:
                print(self.reg[operand_1])
                self.pc += 1 + instruction

            elif IR == JMP:
                self.JMP(operand_1)

            
            elif IR == JEQ:
                self.JEQ(operand_1, instruction)

            elif IR == JNE:
                self.JNE(operand_1, instruction)


            # elif IR == POP:
            #     self.handleStackPop()
            #     self.pc += 1 + instruction

            # elif IR == PUSH:
            #     self.handleStackPush()
            #     self.pc += 1 + instruction

            # elif IR == CALL:
            #     self.handleCALL(operand_1)

            # elif IR == RET:
            #     self.RET()
            

            elif IR == HLT:
                on = False
                print('Ending LOOP')
                sys.exit()

            

            




