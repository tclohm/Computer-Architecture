"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.register = [0] * 8
        self.ram = [0] * 256
        self.pc = 0

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
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

    def ram_read(self, MAR):
        # Memory Address Register, holds the memory address we're reading or writing
        if 0 <= MAR <= 255:
            return self.ram[MAR]
        else:
            return f"{MAR} invalid address"


    def ram_write(self, MAR, MDR):
        # Memory Data Register, holds the value to write or the value just read
        if 0 <= MAR <= 255:
            self.ram[MAR] = MDR
        else:
            return f"{MAR} invalid address"

    def run(self):
        """Run the CPU."""
        halted = False
        # halted instruction
        HLT = 0b00000001 # 1 bytes
        # Set the value of a register to an integer. Load Immediately
        LDI = 0b10000010 # 130 bytes
        # Print numeric value stored in the given register.
        PRN = 0b01000111 # 71 bytes

        while not halted:
            # Instruction Register, contains a copy of the currently executing instruction
            IR = self.ram[self.pc]
            if IR == HLT:
                print("Halting program")
                halted = True
                print("Halted")
            elif IR == LDI:
                address = self.ram_read(self.pc + 1)
                value = self.ram_read(self.pc + 2)
                self.register[address] = value
                self.pc = self.pc + 3
            elif IR == PRN:
                address = self.ram_read(self.pc + 1)
                print(self.register[address])
                self.pc = self.pc + 2
            else:
                print(f"Cannot read instruction, {IR} at address {self.pc}")
