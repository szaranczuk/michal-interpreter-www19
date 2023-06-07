from machine_language import *

def immediate(value):
    return Address(AddressMode.IMMEDIATE, value)


def direct(value):
    return Address(AddressMode.DIRECT, value)


def indirect(value):
    return Address(AddressMode.INDIRECT, value)

#Zgadza sie, ukradlem, ale tylko frajer by nie skorzystal

def execute_program(program):
    execute_instructions(parse_program(program))


labels = {}

def parse_address(address: str) -> Address:
    match address[0]:
        case '.':
            parsed_address = immediate(int(address[1:]))
        case '@':
            parsed_address = direct(int(address[1:]))
        case '*':
            parsed_address = indirect(int(address[1:]))
    return parsed_address

def parse_inc(address: str) -> Instruction:
    parsed_address = parse_address(address)
    return Instruction(InstructionType.INC, [parsed_address])

def parse_dec(address: str) -> Instruction:
    parsed_address = parse_address(address)
    return Instruction(InstructionType.DEC, [parsed_address])

def parse_stop() -> Instruction:
    return Instruction(InstructionType.STOP, [])

def parse_print(address: str) -> Instruction:
    parsed_address = parse_address(address)
    return Instruction(InstructionType.PRINT, [parsed_address])

def make_label(name: str, address: int) -> None:
    labels[name] = address

def parse_jzero(address: str, label: str) -> Instruction:
    parsed_address = parse_address(address)
    return Instruction(InstructionType.JZERO, [parsed_address, immediate(labels[label])])

def parse_jnzero(address: str, label: str) -> Instruction:
    parsed_address = parse_address(address)
    return Instruction(InstructionType.JNZERO, [parsed_address, immediate(labels[label])])


def parse_program(program: str) -> list[Instruction]:
    parsed_program = []
    program_lines = program.split('\n')
    instruction_counter = 0
    for program_line in program_lines:
        unpacked_program_line = program_line.strip().split(' ')
        command = unpacked_program_line[0].lower()
        match command:
            case "inc":
                parsed_program.append(parse_inc(unpacked_program_line[1]))
                instruction_counter += 1
            case "dec":
                parsed_program.append(parse_dec(unpacked_program_line[1]))
                instruction_counter += 1
            case "stop":
                parsed_program.append(parse_stop())
                instruction_counter += 1
            case "print":
                parsed_program.append(parse_print(unpacked_program_line[1]))
                instruction_counter += 1
            case "label":
                make_label(unpacked_program_line[1], instruction_counter)
            case "jzero":
                parsed_program.append(parse_jzero(unpacked_program_line[1], unpacked_program_line[2]))
                instruction_counter += 1
            case "jnzero":
                parsed_program.append(parse_jnzero(unpacked_program_line[1], unpacked_program_line[2]))
                instruction_counter += 1
            case default:
                dupa = "dupa"
    return parsed_program

def execute_instructions(instructions: list[Instruction]) -> str:
    memory = [0]*256
    program_result = ""
    for i in range(len(instructions)):
        instruction = instructions[i]
        match instruction.type:
            case InstructionType.INC:
                memory[instruction.args[0]] += 1
            case InstructionType.DEC:
                memory[instruction.args[0]] -= 1
            case InstructionType.STOP:
                break
            case InstructionType.PRINT:
                program_result += str(memory[instruction.args[0]]) 
                program_result += '\n'
            case InstructionType.JZERO:
                value_address, jump_address = instruction.args
                if (memory[value_address] == 0):
                    i = jump_address - 1
            case InstructionType.JNZERO:
                value_address, jump_address = instruction.args
                if (memory[value_address] != 0):
                    i = jump_address - 1
    return program_result

expected = [Instruction(InstructionType.JZERO, [
                        immediate(0), immediate(0)])]
#print(parse_program(program))