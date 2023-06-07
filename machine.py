from machine_language import *

commands = {'inc', 'dec', 'print', 'label', 'jzero', 'jnzero', 'stop', 'scan'}

def immediate(value):
    return Address(AddressMode.IMMEDIATE, value)


def direct(value):
    return Address(AddressMode.DIRECT, value)


def indirect(value):
    return Address(AddressMode.INDIRECT, value)

class ProgramMemory:
    memory: list[int]
    def __init__(self, memory_size: int):
        self.memory = [0] * memory_size
    def getMemoryAddress(self, address: Address) -> int:
        match address.mode:
            case AddressMode.DIRECT:
                return address.value
            case AddressMode.INDIRECT:
                return self.memory[address.value]
    def setValueInAddress(self, address: Address, value: int) -> None:
        if (address.mode != AddressMode.IMMEDIATE):
            self.memory[self.getMemoryAddress(address)] = value
    def getValueFromAddress(self, address: Address) -> int:
        if (address.mode == AddressMode.IMMEDIATE):
            return address.value
        else:
            return self.memory[self.getMemoryAddress(address)]

def execute_program(program):
    return execute_instructions(parse_program(program))

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

def parse_jzero(value_address: str, jump_address: int) -> Instruction:
    parsed_value_address = parse_address(value_address)
    return Instruction(InstructionType.JZERO, [parsed_value_address, immediate(jump_address)])

def parse_jnzero(value_address: str, jump_address: int) -> Instruction:
    parsed_value_address = parse_address(value_address)
    return Instruction(InstructionType.JNZERO, [parsed_value_address, immediate(jump_address)])

def parse_scan(address: str):
    parsed_address = parse_address(address)
    return Instruction(InstructionType.SCAN, [parsed_address])


def parse_program(program: str) -> list[Instruction]:
    parsed_program = []
    labels = {}
    program_lines = program.split('\n')
    instruction_counter = 0
    for program_line in program_lines:
        unpacked_program_line = program_line.strip().split(' ')
        command = unpacked_program_line[0].lower()
        if (command == "label"):
            labels[unpacked_program_line[1]] = instruction_counter
        elif command in commands:
            instruction_counter += 1
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
            case "jzero":
                parsed_program.append(parse_jzero(unpacked_program_line[1], labels[unpacked_program_line[2]]))
                instruction_counter += 1
            case "jnzero":
                parsed_program.append(parse_jnzero(unpacked_program_line[1], labels[unpacked_program_line[2]]))
                instruction_counter += 1
            case "scan":
                parsed_program.append(parse_scan(unpacked_program_line[1]))
                instruction_counter += 1
            case default:
                dupa = "dupa"
    return parsed_program



def execute_instructions(instructions: list[Instruction]) -> str:
    memory = ProgramMemory(256)
    input_buf = []
    buf_idx = 0
    program_result = ""
    i = 0
    while (i < len(instructions)):
        instruction = instructions[i]
        match instruction.type:
            case InstructionType.INC:
                address = instruction.args[0]
                old_value = memory.getValueFromAddress(address)
                memory.setValueInAddress(address, old_value + 1)
            case InstructionType.DEC:
                address = instruction.args[0]
                old_value = memory.getValueFromAddress(address)
                memory.setValueInAddress(address, old_value - 1)
            case InstructionType.STOP:
                break
            case InstructionType.PRINT:
                address = instruction.args[0]
                program_result += str(memory.getValueFromAddress(address)) 
                program_result += "\n"
            case InstructionType.JZERO:
                value_address, jump_address = instruction.args
                if (memory.getValueFromAddress(value_address) == 0):
                    i = jump_address.value - 1
            case InstructionType.JNZERO:
                value_address, jump_address = instruction.args
                if (memory.getValueFromAddress(value_address) != 0):
                    i = jump_address.value - 1
            case InstructionType.SCAN:
                address = instruction.args[0]
                if (len(input_buf) == buf_idx):
                    input_buf = [int(x) for x in input().split()]
                    buf_idx = 0
                value = input_buf[buf_idx]
                buf_idx += 1
                memory.setValueInAddress(address, value)
        i += 1
    return program_result

expected = [Instruction(InstructionType.JZERO, [
                        immediate(0), immediate(0)])]
program = """
        jzero .0 foo
        print @0
        label foo
        print @0
        """
#print(execute_program(program))