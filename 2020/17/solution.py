#!/usr/bin/env python

from collections import namedtuple

Point = namedtuple("Point", ["x", "y", "z"])

def get_neighboring_points(point):
    """
    Returns a list of neighboring points
    """

    # TODO This method needs a cache

    deltas = [-1, 0, 1]
    neighbors = []

    for x_delta in deltas:
        for y_delta in deltas:
            for z_delta in deltas:
                if x_delta == 0 and y_delta == 0 and z_delta == 0:
                    pass
                else:
                    neighbors.append(Point(point.x + x_delta, point.y + y_delta, point.z + z_delta))

    return neighbors

def is_active_point(point, active_cells):
    return point in active_cells

def is_active_in_next_state(point, active_cells):
    #print("Checking point:", point)

    # Get the active neighbours around the cell
    neighboring_points = get_neighboring_points(point)

    #print("Neigboirng points are ", neighboring_points)
    #print("Active cells are", active_cells)

    active_neighbors = []

    for neighbor in neighboring_points:
        if is_active_point(neighbor, active_cells):
            active_neighbors.append(neighbor)

    if is_active_point(point, active_cells):
        if len(active_neighbors) == 2 or len(active_neighbors) == 3:
            return True
    else:
        if len(active_neighbors) == 3:
            return True

    return False

def get_next_state(active_cells):
    """
    Returns the next set of active cells based on the cells which are currently active

    If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active. Otherwise, the cube becomes inactive.
    If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active. Otherwise, the cube remains inactive.
    """

    new_active_cells = []

    # All of the points, active and not, which may change state
    points_to_visit = set(active_cells)

    # Add all neighboring points
    for point in active_cells:
        neighbors = get_neighboring_points(point)

        for neighbor in neighbors:
            points_to_visit.add(neighbor)

    for point in points_to_visit:
       if is_active_in_next_state(point, active_cells):
           new_active_cells.append(point)

    return new_active_cells


def read_initial_state(filename):
    """
    Reads in the initial game state from the given file
    """
    z = 0
    active_cell = '#'

    active_cells = set()

    with open(filename) as in_file:
        lines = in_file.readlines()

        for row_idx, row in enumerate(lines):
            row = row.strip()
            for col_idx, cell in enumerate(row):
                if cell == active_cell:
                    active_cells.add(Point(col_idx, row_idx, z))

    return active_cells

def print_cells(active_cells):
    min_x = 99999
    min_y = 99999
    min_z = 99999

    max_x = -999999
    max_y = -999999
    max_z = -999999

    for active_cell in active_cells:
        min_x = min(min_x, active_cell.x)
        min_y = min(min_y, active_cell.y)
        min_z = min(min_z, active_cell.z)

        max_x = max(max_x, active_cell.x)
        max_y = max(max_y, active_cell.y)
        max_z = max(max_z, active_cell.z)

    max_x += 1
    max_y += 1
    max_z += 1

    for z in range(min_z, max_z):
        print("z =", z)

        for y in range(min_y, max_y):
            row = []
            for x in range(min_x, max_x):
                if Point(x, y, z) in active_cells:
                    row.append('#')
                else:
                    row.append('.')
            print(''.join(row))


filename = "input.txt"
active_cells = read_initial_state(filename)
print_cells(active_cells)

max_cycles = 6
for cycle_count in range(1,max_cycles + 1):
    active_cells = get_next_state(active_cells)
    print("After cycle", cycle_count)
    print(len(active_cells))
    #print_cells(active_cells)
