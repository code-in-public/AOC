#!/usr/bin/env python

from collections import namedtuple
from copy import deepcopy

Instruction = namedtuple("Instruction", ["op", "arg"])

def parse_instruction(instruction_string):
    """
    Parse the instruction string to return an instruction object
    """
    op, arg = instruction_string.split()

    instruction = Instruction(op, int(arg))

    return instruction

def read_program(filename):
    """
    Read in the program file and return a list of instructions
    """
    with open(filename) as in_file:
        instructions = in_file.readlines()

        return [parse_instruction(instruction.strip()) for instruction in instructions]

def get_alternative_program(in_instructions, idx):
    """
    Return an alternative program where a jmp has changed to noop or noop to jmp

    idx is the unique id for this alternative version of the application
    """

    nop_or_jmps_seen = 0

    instructions = deepcopy(in_instructions)

    for pc, instruction in enumerate(instructions):
        if instruction.op == "nop":
            if nop_or_jmps_seen == idx:
                # Swap the op
                instructions[pc] = Instruction("jmp", instruction.arg)
                return instructions

            nop_or_jmps_seen += 1

        if instruction.op == "jmp":
            if nop_or_jmps_seen == idx:
                # Swap the op
                instructions[pc] = Instruction("nop", instruction.arg)
                return instructions

            nop_or_jmps_seen += 1

    return instructions

def execute_once(instructions):
    """
    Execute the given set of instructions
    It returns if the program halted correctly
    """
    executed = set()

    acc = 0 # Accumulator
    pc = 0 # Program counter
    running = True

    while running:
        # Check that we are not looping
        if pc in executed:
            running = False
            print("Looped with accumulator value", acc)
            return False
        else:
            executed.add(pc)

            if pc == len(instructions):
                print("Halting correctly", pc, acc)
                return True

            instruction = instructions[pc]
            #print("Executing", pc, instruction, acc)

            if instruction.op == "nop":
                pc += 1

            if instruction.op == "acc":
                acc += instruction.arg
                pc += 1

            if instruction.op == "jmp":
                pc += instruction.arg


filename = "input.txt"

instructions = read_program(filename)

halted = False

alt_idx = 0

while not halted:
    alternative = get_alternative_program(instructions, alt_idx)
    halted = execute_once(alternative)

    alt_idx += 1
