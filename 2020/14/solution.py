#!/usr/bin/env python3

from collections import namedtuple
import re

def apply_zeros_mask(bitmask, value):
    """
    Applies all of the 0s from the provided bitmask to the value
    """

    # Creat a mask which 0s only in the same place as in the mask
    mask = 2 ** (len(bitmask)) - 1

    for bit_idx in range(len(bitmask)-1, -1, -1):
        if bitmask[bit_idx] == '0':
            mask = mask - (1 << (len(bitmask) - bit_idx - 1))

    return value & mask

def apply_ones_mask(bitmask, value):
    """
    Applies all of the 1s from the provided bitmask to the value
    """

    # Creat a mask which with 1s only in the same place as the mask
    mask = 0

    for bit_idx in range(len(bitmask)-1, -1, -1):
        if bitmask[bit_idx] == '1':
            mask = mask | (1 << (len(bitmask) - bit_idx - 1))

    return value | mask

def apply_mask(bitmask, value):
    """
    Applies the provided bitmask to the value and returns the new value
    """

    # Apply the 1s from the mask
    result = apply_ones_mask(bitmask, value)

    # Apply the 0s from the mask
    result = apply_zeros_mask(bitmask, result)

    return result

MaskInstruction = namedtuple("MaskInstruction", ["mask"])
WriteInstruction = namedtuple("WriteInstruction", ["address", "value"])

def parse_instruction(instruction_string):
    instruction_string = instruction_string.strip()

    if instruction_string.startswith("mask"):
        return MaskInstruction(instruction_string.split("=")[1].strip())
    else:
        tokens = instruction_string.split("=")

        address = int(re.findall(r"\d+", tokens[0])[0])
        value = int(tokens[1].strip())
        return WriteInstruction(address, value)

    return None

def get_instructions(filename):
    with open(filename) as in_file:
        return [parse_instruction(instruction) for instruction in in_file.readlines()]

def process_instructions(instructions, memory):
    mask = None
    for instruction in instructions:
        if isinstance(instruction, MaskInstruction):
            mask = instruction.mask
        else:
            memory[instruction.address] = apply_mask(mask, instruction.value)

    return memory

# Part 2
def process_instructions_address_mask(instructions, memory):
    mask = None
    for instruction in instructions:
        if isinstance(instruction, MaskInstruction):
            mask = instruction.mask
        else:
            addresses = get_addresses(instruction.address, mask)

            for address in addresses:
                memory[address] = instruction.value

    return memory

def get_memory_sum(memory):
    total = 0
    for address in memory:
        total += memory[address]

    return total

def bin_array_to_dec(bin_array):
    result = 0

    for idx, bit in enumerate(bin_array):
        pow_of_2 = len(bin_array) - idx - 1

        result += bit * 2**pow_of_2

    return result

def get_float_values(mask):
    """
    Returns a list of all the values which are possible with the given mask
    """

    unprocessed = [mask]
    result = []

    while unprocessed:
        mask = unprocessed.pop()

        if 'X' in mask:
            float_idx = mask.index('X')

            next_mask = mask[:]
            next_mask[float_idx] = 1
            unprocessed.append(next_mask)
            next_mask2 = mask[:]
            next_mask2[float_idx] = 0
            unprocessed.append(next_mask2)
        else:
            result.append(mask)

    return [bin_array_to_dec(val) for val in result]

def get_addresses(address, mask):
    """
    Returns a set of addresses based on the following rules

    If the bitmask bit is 0, the corresponding memory address bit is unchanged.
    If the bitmask bit is 1, the corresponding memory address bit is overwritten with 1.
    If the bitmask bit is X, the corresponding memory address bit is floating.
    """
    address_mask = []

    for bit_idx in range(len(mask)-1, -1, -1):
        current_mask_bit = mask[bit_idx]

        current_address_bit = address & 1
        address >>= 1

        if current_mask_bit == '0':
            address_mask.insert(0, current_address_bit)
        elif current_mask_bit == '1':
            address_mask.insert(0, 1)
        else:
            address_mask.insert(0, 'X')


    addresses = get_float_values(address_mask)
    return addresses

filename = 'input.txt'
memory = {}
instructions = get_instructions(filename)

#memory = process_instructions(instructions, memory)
#print(memory)

total = get_memory_sum(memory)
#print(total)


# Part 2
memory = process_instructions_address_mask(instructions, memory)

total = get_memory_sum(memory)
print(memory)
print(total)
