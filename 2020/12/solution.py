#!/usr/bin/env python3

from collections import namedtuple

Instruction = namedtuple("Instruction", ["action", "value"])
Position = namedtuple("Position", ["east", "north"])

PositionAndOrientation = namedtuple("PositionAndOrientation", ["position", "orientation"])

def parse_instruction(instruction_string):
    instruction_string = instruction_string.strip()
    return Instruction(action = instruction_string[0], value = int(instruction_string[1:]))

def read_navigation_instructions(filename):
    with open(filename) as in_file:
        return [parse_instruction(instruction) for instruction in in_file.readlines()]

def perform_instruction(current_position_and_orientation, instruction):
    # Moving in given direction
    # Flip the direction and value
    if instruction.action == 'S':
        instruction = Instruction('N', instruction.value * -1)

    if instruction.action == 'W':
        instruction = Instruction('E', instruction.value * -1)

    if instruction.action == 'N':
        new_pos = Position(current_position_and_orientation.position.east,
                           current_position_and_orientation.position.north + instruction.value)
        new_orient = current_position_and_orientation.orientation

        return PositionAndOrientation(new_pos, new_orient)

    if instruction.action == 'E':
        new_pos = Position(current_position_and_orientation.position.east + instruction.value,
                           current_position_and_orientation.position.north)
        new_orient = current_position_and_orientation.orientation

        return PositionAndOrientation(new_pos, new_orient)

    # Turning
    if instruction.action == 'L':
        instruction = Instruction('R', instruction.value * -1)

    if instruction.action == 'R':
        directions = ['E', 'S', 'W', 'N']
        current_direction_idx = directions.index(current_position_and_orientation.orientation)

        num_right_angles = int(instruction.value / 90)

        new_direction_idx = (current_direction_idx + num_right_angles)%4

        new_orient = directions[new_direction_idx]
        new_pos = Position(current_position_and_orientation.position.east,
                           current_position_and_orientation.position.north)

        return PositionAndOrientation(new_pos, new_orient)

    # Moving forward
    if instruction.action == 'F':
        orientation = current_position_and_orientation.orientation

        new_instruction = Instruction(action=orientation, value=instruction.value)
        return(perform_instruction(current_position_and_orientation, new_instruction))

    return current_position_and_orientation

def perform_instructions(current_position_and_orientation, instructions):
    for instruction in instructions:
        current_position_and_orientation = perform_instruction(current_position_and_orientation, instruction)

    return current_position_and_orientation

def get_manhattan_distance(position_and_orientation):
    position = position_and_orientation.position

    return abs(position.east) + abs(position.north)

def perform_wp_instruction(ship_pos, wp_pos, instruction):
    print(instruction)

    # Moving in given direction
    # Flip the direction and value
    if instruction.action == 'S':
        instruction = Instruction('N', instruction.value * -1)

    if instruction.action == 'W':
        instruction = Instruction('E', instruction.value * -1)

    if instruction.action == 'N':
        new_wp_pos = Position(wp_pos.east,
                              wp_pos.north + instruction.value)

        return ship_pos, new_wp_pos

    if instruction.action == 'E':
        new_wp_pos = Position(wp_pos.east + instruction.value,
                              wp_pos.north)

        return ship_pos, new_wp_pos

    # Turning
    if instruction.action == 'L':
        instruction = Instruction('R', (instruction.value * -1) + 360)

    if instruction.action == 'R':
        remaining_rotation = instruction.value
        while remaining_rotation > 0:
            print("Rotating 90")

            wp_pos = Position(wp_pos.north, wp_pos.east*-1)
            remaining_rotation -= 90

        return ship_pos, wp_pos

    # Moving to toward the Waypoint a number of times
    if instruction.action == 'F':
        new_ship_pos = Position(ship_pos.east + (wp_pos.east * instruction.value),
                                ship_pos.north + (wp_pos.north * instruction.value))

        return new_ship_pos, wp_pos


def perform_wp_instructions(ship_pos, wp_pos, instructions):
    print(instructions)
    for instruction in instructions:
        ship_pos, wp_pos = perform_wp_instruction(ship_pos, wp_pos, instruction)
        print("After instruction - ship:", ship_pos, " way point: ", wp_pos)

    return ship_pos, wp_pos

filename = "input.txt"

instructions = read_navigation_instructions(filename)
current_position_and_orientation = PositionAndOrientation(Position(0,0), 'E')

new_p_and_o = perform_instructions(current_position_and_orientation, instructions)

#print(new_p_and_o)
#print(get_manhattan_distance(new_p_and_o))

# Part 1
filename = "input.txt"
instructions = read_navigation_instructions(filename)

ship_pos = Position(east = 0, north = 0)
wp_pos = Position(east = 10, north = 1)

end_ship_pos, end_wp_pos = perform_wp_instructions(ship_pos, wp_pos, instructions)

print(abs(end_ship_pos.east) + abs(end_ship_pos.north))
