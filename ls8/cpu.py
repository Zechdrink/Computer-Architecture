"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU. """
        self.ram = [000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 0xF4

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

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        ADD = 0b10100000
        SUB = 0b10100001
        MUL = 0b10100010
        DIV = 0b10100011

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

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
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
        PRN = 0b1000111
        HLT = 0b0000001
        MUL = 0b10100010
        POP = 0b01000110
        PUSH = 0b01000101

        while on:
            IR = self.ram[self.pc]

            # get next two MDR's from the next two MAR's stored in ram incase instructions need it
            operand_1 = self.ram_read(self.pc + 1)
            operand_2 = self.ram_read(self.pc + 2)
            instruction = (IR >> 6)

                # Check LDI instruction
            alu_number = (IR & 0b00100000) >> 5

            if alu_number:
                self.alu(IR, operand_1, operand_2)

            if IR == LDI:
                self.reg[operand_1] = operand_2

            if IR == POP:
                self.handleStackPop()

            if IR == PUSH:
                self.handleStackPush()

            if IR == PRN:
                print(self.reg[operand_1])

            if IR == HLT:
                on = False

            self.pc += 1 + instruction




