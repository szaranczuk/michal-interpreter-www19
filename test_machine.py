from machine import *
from machine_language import *

import unittest


def immediate(value):
    return Address(AddressMode.IMMEDIATE, value)


def direct(value):
    return Address(AddressMode.DIRECT, value)


def indirect(value):
    return Address(AddressMode.INDIRECT, value)


class TestParser(unittest.TestCase):
    def test_empty_program_has_no_instructions(self):
        program = ''
        instructions = parse_program(program)
        self.assertEqual(instructions, [])

    def test_program_with_one_instruction(self):
        program = 'inc .1'
        instructions = parse_program(program)
        expected = [Instruction(InstructionType.INC, [immediate(1)])]
        self.assertEqual(instructions, expected)

    def test_empty_lines_are_ignored(self):
        program = """
        inc .1

        inc .2
        """
        instructions = parse_program(program)
        expected = [
            Instruction(InstructionType.INC, [immediate(1)]),
            Instruction(InstructionType.INC, [immediate(2)])
        ]
        self.assertEqual(instructions, expected)

    def test_labels_are_ignored(self):
        program = """
        inc .1
        label foo
        inc .2
        """
        instructions = parse_program(program)
        expected = [
            Instruction(InstructionType.INC, [immediate(1)]),
            Instruction(InstructionType.INC, [immediate(2)]),
        ]
        self.assertEqual(instructions, expected)


    def test_immediate_address_mode(self):
        program = 'inc .1'
        instructions = parse_program(program)
        expected = [Instruction(InstructionType.INC, [immediate(1)])]
        self.assertEqual(instructions, expected)

    def test_direct_address_mode(self):
        program = 'inc @1'
        instructions = parse_program(program)
        expected = [Instruction(InstructionType.INC, [direct(1)])]
        self.assertEqual(instructions, expected)

    def test_indirect_address_mode(self):
        program = 'inc *1'
        instructions = parse_program(program)
        expected = [Instruction(InstructionType.INC, [indirect(1)])]
        self.assertEqual(instructions, expected)


class TestMachine(unittest.TestCase):
    def test_memory_starts_filled_with_zeros(self):
        program = """
        print @0
        print @1
        """
        result = execute_program(program)
        self.assertEqual(result, '0\n0\n')

    def inc_increments_value(self):
        program = """
        inc @0
        print @0
        """
        result = execute_program(program)
        self.assertEqual(result, '1\n')

    def test_dec_decrements_value(self):
        program = """
        dec @0
        print @0
        """
        result = execute_program(program)
        self.assertEqual(result, '-1\n')

    def test_program_starts_on_stop(self):
        program = """
        stop
        print @0
        """
        result = execute_program(program)
        self.assertEqual(result, '')

    def test_immediate_address_mode_returns_value(self):
        program = """
        print .1
        """
        result = execute_program(program)
        self.assertEqual(result, '1\n')

    def test_direct_address_mode_returns_value_from_memory(self):
        program = """
        inc @0
        print @0
        """
        result = execute_program(program)
        self.assertEqual(result, '1\n')

    def test_indirect_address_mode_returns_value_from_referenced_cell(self):
        program = """
        inc @0
        dec *0
        print @1
        """
        result = execute_program(program)
        self.assertEqual(result, '-1\n')

    def test_jzero_jumps_to_label_if_value_is_zero(self):
        program = """
        jzero .0 foo
        print @0
        label foo
        print @0
        """
        result = execute_program(program)
        self.assertEqual(result, '0\n')

    def test_jzero_does_not_jump_to_label_if_value_is_not_zero(self):
        program = """
        jzero .1 foo
        print @0
        label foo
        print @0
        """
        result = execute_program(program)
        self.assertEqual(result, '0\n0\n')


    def jnzero_jumps_to_label_if_value_is_not_zero(self):
        program = """
        jnzero .1 foo
        print @0
        label foo
        print @0
        """
        result = execute_program(program)
        self.assertEqual(result, '0\n')

    def test_jnzero_does_not_jump_to_label_if_value_is_zero(self):
        program = """
        jnzero .0 foo
        print @0
        label foo
        print @0
        """
        result = execute_program(program)
        self.assertEqual(result, '0\n0\n')

    def test_jumping_between_many_labels(self):
        program = """
        jzero .0 start
        label foo
        inc @0
        inc @0
        label start
        jzero @0 foo        
        print @0
        """
        result = execute_program(program)
        self.assertEqual(result, '2\n')