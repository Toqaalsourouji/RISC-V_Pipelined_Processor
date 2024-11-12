import random
import numpy as np

def reverse_dictionary_with_iterable(dictionary):
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
    LUI='0110111', AUIPC='0010111', JAL='1101111', BEQ='1100011', BNE='1100011', BLT='1100011',
    BGE='1100011', BLTU='1100011', BGEU='1100011', JALR='1100111', LB='0000011', LH='0000011',
    LW='0000011', LBU='0000011', LHU='0000011', ADDI='0010011', SLTI='0010011', ORI='0010011',
    XORI='0010011', ANDI='0010011', SLLI='0010011', SRLI='0010011', SRAI='0010011', SB='0100011',
    SH='0100011', SW='0100011', ADD='0110011', SUB='0110011', AND='0110011', OR='0110011', XOR='0110011',
    SLL='0110011', SLT='0110011', SLTU='0110011', SRL='0110011', SRA='0110011'
)

Funct_3 = dict(
    JALR='000', BEQ='000', BNE='001', BLT='100', BGE='101', BLTU='110', BGEU='111', LB='000',
    LH='001', LW='010', LBU='100', LHU='101', SB='000', SH='001', SW='010', ADDI='000',
    SLTI='010', XORI='100', ORI='110', ANDI='111', SLLI='001', SRLI='101', SRAI='101',
    ADD='000', SUB='000', SLL='001', SLT='010', SLTU='011', XOR='100', SRL='101', SRA='101',
    OR='110', AND='111'
)

Shift_imm_inst = {'SLLI', 'SRLI', 'SRAI'}
Load_inst = {'LW', 'LB', 'LH', 'LBU', 'LHU'}
Store_inst = {'SW', 'SB', 'SH'}

Link_inst_to_aType = reverse_dictionary_with_iterable(Instructions_Types)

def add_inst(binary, assembly):
    inst_binary.append(binary)
    inst_assembly.append(assembly)

def generate_R_type(name):
    opcode_inst = Opcodes[name]
    func3_inst = Funct_3[name]
    func7_inst = '0100000' if name in {'SUB', 'SRA'} else '0000000'

    rs1_decimal = random.choice(Regs)
    rs1_binary = f"{rs1_decimal:05b}"
    rs2_decimal = random.choice(Regs)
    rs2_binary = f"{rs2_decimal:05b}"
    rd_decimal = random.choice(Regs)
    rd_binary = f"{rd_decimal:05b}"

    instruction_binary = func7_inst + rs2_binary + rs1_binary + func3_inst + rd_binary + opcode_inst
    instruction_assembly = f"{name:10}\tx{rd_decimal}, x{rs1_decimal}, x{rs2_decimal}"

    add_inst(instruction_binary, instruction_assembly)

# Implement similar functions for I, S, SB, U, UJ types
# Code for generate_I_type, generate_S_type, etc. goes here...

def generate_inst(name):
    if Link_inst_to_aType[name] == 'R':
        generate_R_type(name)
    elif Link_inst_to_aType[name] == 'I':
        generate_I_type(name)
    elif Link_inst_to_aType[name] == 'S':
        generate_S_type(name)
    elif Link_inst_to_aType[name] == 'SB':
        generate_SB_type(name)
    elif Link_inst_to_aType[name] == 'U':
        generate_U_type(name)
    elif Link_inst_to_aType[name] == 'UJ':
        generate_UJ_type(name)

Test_Case_num = int(input('Enter the number of test cases to be generated: '))

for test_case in range(Test_Case_num):
    Reg_num = int(input('Enter the number of registers to be used (from 0 to 31): '))
    inst_num = int(input('Enter the number of instructions to be generated: '))

    Regs = np.random.randint(1, 32, Reg_num).tolist()
    Stored_mem_location = []
    inst_binary = []
    inst_assembly = []

    for insts in range(inst_num):
        inst_name = random.choice(list(Link_inst_to_aType.keys()))

        while inst_name in Load_inst and not Stored_mem_location:
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

    print("FINISHED TEST CASE " + str(test_case + 1))
