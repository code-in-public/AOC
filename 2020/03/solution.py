#!/usr/bin/env python3

def parse_line(line):
    return [char for char in line]

# Read the file contents and return a list of things
def read_file(filename):
    with open(filename) as file:
        lines = file.readlines();

        return [parse_line(line.strip()) for line in lines]

def follow_path(slope_map, row_delta, col_delta):
    row = row_delta
    col = col_delta

    visited = []

    while row < len(slope_map):

        visited.append(slope_map[row][col])

        row += row_delta
        col = (col + col_delta) % len(slope_map[0])

    return visited

def count_trees(path):
    tree = '#'

    return len([loc for loc in path if loc == tree])

def get_tree_counts(slope_map, path_options):
    path_tree_counts = []
    for path_option in path_options:
        path = follow_path(slope_map, path_option[0], path_option[1])

        path_tree_counts.append(count_trees(path))

    return path_tree_counts

filename = "input_day3.txt"
slope_map = read_file(filename)

path_options = [
    [1, 1],
    [1, 3],
    [1, 5],
    [1, 7],
    [2, 1],
]

tree_counts = get_tree_counts(slope_map, path_options)

total = 1
for count in tree_counts:
    total *= count

print(total)
