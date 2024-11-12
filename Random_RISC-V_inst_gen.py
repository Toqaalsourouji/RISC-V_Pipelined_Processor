import random
import numpy as np
import re

def reverse_dictionary_with_iterable(dictionary): # Function to reverse a dictionary keys with values
    reverse = {}
    for key, value in dictionary.items():
        for item in value:
            reverse[item] = key
    return reverse

Instructions_Types = dict(
    U={'LUI', 'AUIPC'},
    UJ={'JAL'},
    SB={'BEQ', 'BNE', 'BLT', 'BGE', 'BLTU', 'BGEU'},
    I={'JALR', 'LB', 'LH', 'LW', 'LBU', 'LHU', 'ADDI', 'SLTI', 'ORI', 'XORI', 'ANDI', 'SLLI', 'SRLI', 'SRAI'},
    S={'SB', 'SH', 'SW'},
    R={'ADD', 'SUB', 'AND', 'OR', 'XOR', 'SLL', 'SLT', 'SLTU', 'SRL', 'SRA'}
)

Opcodes = dict(
    LUI='0110111', AUIPC='0010111', JAL='1101111', BEQ='1100011', BNE='1100011',
    BLT='1100011', BGE='1100011', BLTU='1100011', BGEU='1100011', JALR='1100111',
    LB='0000011', LH='0000011', LW='0000011', LBU='0000011', LHU='0000011', ADDI='0010011',
    SLTI='0010011', SLTIU='0010011', ORI='0010011', XORI='0010011', ANDI='0010011',
    SLLI='0010011', SRLI='0010011', SRAI='0010011', SB='0100011', SH='0100011',
    SW='0100011', ADD='0110011', SUB='0110011', AND='0110011', OR='0110011',
    XOR='0110011', SLL='0110011', SLT='0110011', SLTU='0110011', SRL='0110011', SRA='0110011'
)

Funct_3 = dict(
    JALR='000', BEQ='000', BNE='001', BLT='100', BGE='101', BLTU='110', BGEU='111',
    LB='000', LH='001', LW='010', LBU='100', LHU='101', SB='000', SH='001', SW='010',
    ADDI='000', SLTI='010', SLTIU='011', XORI='100', ORI='110', ANDI='111', SLLI='001',
    SRLI='101', SRAI='101', ADD='000', SUB='000', SLL='001', SLT='010', SLTU='011',
    XOR='100', SRL='101', SRA='101', OR='110', AND='111'
)

Shift_imm_inst = {'SLLI', 'SRLI', 'SRAI'}
Load_inst = {'LW', 'LB', 'LH', 'LBU', 'LHU'}
Store_inst = {'SW', 'SB', 'SH'}

Link_inst_to_aType = reverse_dictionary_with_iterable(Instructions_Types)

Test_Case_num = 0
Stored_mem_location = []
inst_binary = []
inst_assembly = []
Regs = []
REGISTERS_TO_USE = [i for i in range(32)]

def add_inst(binary, assembly):
    inst_binary.append(binary)
    inst_assembly.append(assembly)

def generate_R_type(name):
    opcode_inst = Opcodes[name]
    func3_inst = Funct_3[name]

    if name == 'SUB' or name == 'SRA':
        func7_inst = '0100000'
    else:
        func7_inst = '0000000'

    rs1_decimal = random.choice(Regs)
    rs1_binary = "{0:05b}".format(rs1_decimal)
    rs2_decimal = random.choice(Regs)
    rs2_binary = "{0:05b}".format(rs2_decimal)
    rd_decimal = random.choice(REGISTERS_TO_USE)
    rd_binary = "{0:05b}".format(rd_decimal)

    instruction_binary = func7_inst + rs2_binary + rs1_binary + func3_inst + rd_binary + opcode_inst
    instruction_assembly = format(name, '10s') + "\tx" + str(rd_decimal) + ", x" + str(rs1_decimal) + ", x" + str(rs2_decimal)

    add_inst(instruction_binary, instruction_assembly)

def generate_I_type(name):
    opcode_inst = Opcodes[name]
    func3_inst = Funct_3[name]
    rs1_decimal = random.choice(Regs)
    rs1_binary = "{0:05b}".format(rs1_decimal)
    rd_decimal = random.choice(Regs)
    rd_binary = "{0:05b}".format(rd_decimal)

    if name in Shift_imm_inst:
        imm = '0100000' if name == 'SRAI' else '0000000'
        shamt_decimal = np.random.randint(0, 32)
        shamt_binary = "{0:05b}".format(shamt_decimal)
        instruction_binary = imm + shamt_binary + rs1_binary + func3_inst + rd_binary + opcode_inst
        instruction_assembly = format(name, '10s') + "\tx" + str(rd_decimal) + ", x" + str(rs1_decimal) + ", " + str(shamt_decimal)
    elif name in Load_inst:
        rs1_decimal = 0
        rs1_binary = "{0:05b}".format(rs1_decimal)
        imm_decimal = random.choice(Stored_mem_location)
        imm_binary = "{0:012b}".format(imm_decimal)
        instruction_binary = imm_binary + rs1_binary + func3_inst + rd_binary + opcode_inst
        instruction_assembly = format(name, '10s') + "\tx" + str(rd_decimal) + ", " + str(imm_decimal) + "(x" + str(rs1_decimal) + ")"
    else:
        imm_decimal = np.random.randint(0, 4095)
        imm_binary = "{0:012b}".format(imm_decimal)
        instruction_binary = imm_binary + rs1_binary + func3_inst + rd_binary + opcode_inst
        instruction_assembly = format(name, '10s') + "\tx" + str(rd_decimal) + ", x" + str(rs1_decimal) + ", " + str(imm_decimal)

    add_inst(instruction_binary, instruction_assembly)

def generate_S_type(name):
    opcode_inst = Opcodes[name]
    func3_inst = Funct_3[name]
    rs1_decimal = 0
    rs1_binary = "{0:05b}".format(rs1_decimal)
    rs2_decimal = random.choice(Regs)
    rs2_binary = "{0:05b}".format(rs2_decimal)
    imm_decimal = 2 * np.random.randint(0, 2047)
    imm_binary = "{0:012b}".format(imm_decimal)
    Stored_mem_location.append(imm_decimal)

    instruction_binary = imm_binary[0:7] + rs2_binary + rs1_binary + func3_inst + imm_binary[7:] + opcode_inst
    instruction_assembly = format(name, '10s') + "\tx" + str(rs2_decimal) + ", " + str(imm_decimal) + "(x" + str(rs1_decimal) + ")"

    add_inst(instruction_binary, instruction_assembly)

def generate_SB_type(name):
    opcode_inst = Opcodes[name]
    func3_inst = Funct_3[name]
    rs1_decimal = random.choice(Regs)
    rs1_binary = "{0:05b}".format(rs1_decimal)
    rs2_decimal = random.choice(Regs)
    rs2_binary = "{0:05b}".format(rs2_decimal)
    imm_decimal = np.random.randint(1, 4096)
    imm_binary = "{0:012b}".format(imm_decimal)
    instruction_binary = imm_binary[0] + imm_binary[2:8] + rs2_binary + rs1_binary + func3_inst + imm_binary[8:] + imm_binary[1] + opcode_inst
    instruction_assembly = format(name, '10s') + "\tx" + str(rs1_decimal) + ", x" + str(rs2_decimal) + ", " + str(imm_decimal)

    add_inst(instruction_binary, instruction_assembly)

def generate_U_type(name):
    opcode_inst = Opcodes[name]
    rd_decimal = random.choice(Regs)
    rd_binary = "{0:05b}".format(rd_decimal)
    imm_decimal = np.random.randint(0, 1048575)
    imm_binary = "{0:020b}".format(imm_decimal)

    instruction_binary = imm_binary + rd_binary + opcode_inst
    instruction_assembly = format(name, '10s') + "\tx" + str(rd_decimal) + ", " + str(imm_decimal)

    add_inst(instruction_binary, instruction_assembly)

def generate_UJ_type(name):
    opcode_inst = Opcodes[name]
    rd_decimal = random.choice(Regs)
    rd_binary = "{0:05b}".format(rd_decimal)
    imm_decimal = np.random.randint(1, 4096) * 4
    imm_binary = "{0:020b}".format(imm_decimal)

    instruction_binary = imm_binary[0] + imm_binary[10:] + imm_binary[9] + imm_binary[1:9] + rd_binary + opcode_inst
    instruction_assembly = format(name, '10s') + "\tx" + str(rd_decimal) + ", " + str(imm_decimal)

    add_inst(instruction_binary, instruction_assembly)

def generate_inst(name):
    if name in Instructions_Types['R']:
        generate_R_type(name)
    elif name in Instructions_Types['I']:
        generate_I_type(name)
    elif name in Instructions_Types['S']:
        generate_S_type(name)
    elif name in Instructions_Types['SB']:
        generate_SB_type(name)
    elif name in Instructions_Types['U']:
        generate_U_type(name)
    elif name in Instructions_Types['UJ']:
        generate_UJ_type(name)

if __name__ == "__main__":
    while int(Test_Case_num) < 1:
        Test_Case_num = int(input('Enter the number of test cases to be generated: '))

    for test_case in range(int(Test_Case_num)):
        Reg_num = 0
        inst_num = 0
        current_inst = 0
        Stored_mem_location.clear()
        inst_binary.clear()
        inst_assembly.clear()

        while int(inst_num) < 1:
            inst_num = int(input('Enter the number of instructions to be generated: '))

        while int(Reg_num) < 1 or int(Reg_num) > 32:
            Reg_num = int(input('Enter the number of registers to be used (from 0 to 31): '))

        Regs = np.random.randint(1, 32, int(Reg_num))
        Instructions_number = int(inst_num)

        for insts in range(inst_num):
            current_inst = insts
            inst_name = random.choice(list(Link_inst_to_aType.keys()))

            while inst_name in Load_inst and len(Stored_mem_location) == 0:
                inst_name = random.choice(list(Link_inst_to_aType.keys()))

            generate_inst(inst_name)

        binary_file = open(f"binary{test_case + 1}.txt", "w")
        assembly_file = open(f"assembly{test_case + 1}.s", "w")

        assembly_file.write(f'test{test_case + 1}.elf:     file format elf32-littleriscv\n\n\n')
        assembly_file.write('Disassembly of section .text:\n\n00000000 <main>:\n')

        for i in range(inst_num):
            binary_file.write(inst_binary[i] + "\n")
            assembly_file.write(inst_assembly[i] + "\n")

        binary_file.close()
        assembly_file.close()

        print(f"FINISHED TEST CASE {test_case + 1}")
