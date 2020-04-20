"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.registers = [0] * 8
        self.pc = 0
        self.running = True

        self.dispatcher = {
            LDI: self.LDI,
            PRN: self.PRN,
            HLT: self.HLT,
            MUL: self.MUL
        }

    def LDI(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)

        self.registers[operand_a] = operand_b

        self.pc += 3

    def PRN(self):
        operand_a = self.ram_read(self.pc + 1)

        print(self.registers[operand_a])

        self.pc += 2

    def MUL(self):
        operand_a_1 = self.ram_read(self.pc + 1)
        operand_b_1 = self.ram_read(self.pc + 2)

        operand_a_2 = self.registers[operand_a_1]
        operand_b_2 = self.registers[operand_b_1]

        print(operand_a_2 * operand_b_2)

        self.pc += 3


    def HLT(self):
        self.running = False

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def load(self, file_path):
        """Load a program into memory."""
        address = 0

        with open(file_path, 'r') as f:
            for line in f.readlines():
                instruction = int(line.strip().split(' ')[0], 2)
                self.ram_write(address, instruction)

                address += 1
                

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
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
        """Run the CPU."""

        while self.running:
            ir = self.ram_read(self.pc)

            if ir in self.dispatcher:
                self.dispatcher[ir]()
            else:
                print(f'Unknown instruction: "{ir}".')
                self.running = False