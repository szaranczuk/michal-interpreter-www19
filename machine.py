from machine_language import *


def execute_program(program):
    execute_instructions(parse_program(program))


def parse_program(program):
    """Convert program written as string into list of instructions"""
    return NotImplemented


def execute_instructions(instructions):
    """Execute the program and return the result."""
    return NotImplemented
