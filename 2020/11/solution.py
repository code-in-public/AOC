#!/usr/bin/env python3

def read_seating(filename):
    """
    Read the current seating state from file
    """

    with open(filename) as in_file:
        lines = in_file.readlines()

        return [[seat for seat in line.strip()] for line in lines]


neighbor_coords_cache = {}

def get_neighbor_coords(row, col, max_row, max_col):
    """
    Returns the valid neighbor coordinates
    """
    cache_key = (row, col, max_row, max_col)

    if cache_key not in neighbor_coords_cache:

        neighbor_row_deltas = [-1, 0, 1]
        neighbor_col_deltas = [-1, 0, 1]

        neighbor_coords = []

        for row_delta in neighbor_row_deltas:
            for col_delta in neighbor_col_deltas:
                if row_delta == col_delta and row_delta == 0:
                    # Dont add self to neighbors
                    pass
                else:
                    if (0 <= row+row_delta < max_row) and (0 <= col+col_delta < max_col):
                        neighbor_coords.append((row+row_delta, col+col_delta))

        neighbor_coords_cache[cache_key] = neighbor_coords

    return neighbor_coords_cache[cache_key]

def get_neighbors(seat_state, row, col):
    """
    Returns all 8 neighbors to the given row and col
    """
    neighbor_coords = get_neighbor_coords(row, col, len(seat_state), len(seat_state[0]))

    neighbors = []
    for neighbor_coord in neighbor_coords:
        neighbors.append(seat_state[neighbor_coord[0]][neighbor_coord[1]])

    return neighbors

seat_state_cache = {}

def get_next_seat_state(current_state, neighbor_state):
    """
    Returns the state of the seat based in the neighbours
    """

    # Perform a cache lookup
    cache_key = (current_state, ''.join(neighbor_state))

    if cache_key not in seat_state_cache:
        next_state = current_state

        if current_state == '.':
            # Empy space, never changes
            next_state = '.'
        elif current_state == 'L':
            # Seat in empty
            # If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
            if '#' not in neighbor_state:
                next_state = '#'

        elif current_state == '#':
            # Seat is occupied
            # If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
            # if neighbor_state.count('#') >= 4:
             if neighbor_state.count('#') >= 5:
                next_state = 'L'

        seat_state_cache[cache_key] = next_state

    return seat_state_cache[cache_key]

def get_next_seat_map_state(seat_state):
    """
    Performs the rules to get the next seat state
    """

    next_seat_state = []

    for seat_row_id in range(len(seat_state)):
        next_seat_state_row = []
        for seat_col_id in range(len(seat_state[seat_row_id])):
            #neighbors = get_neighbors(seat_state, seat_row_id, seat_col_id)
            neighbors = get_visible_neighbors(seat_state, seat_row_id, seat_col_id)
            current_state = seat_state[seat_row_id][seat_col_id]

            # Determine the next state of the given seat
            next_seat_state_row.append(get_next_seat_state(current_state, neighbors))
        next_seat_state.append(next_seat_state_row)

    return next_seat_state

def print_state(seat_map_state):
    print("------------------")
    for row in seat_map_state:
        print(row)

def get_stable_state(current_state):
    """
    Applied the state change rules until nothing changes between the states
    """

    changing_state = True

    while changing_state:
        #print_state(current_state)

        previous_state = current_state
        current_state = get_next_seat_map_state(current_state)

        changing_state = previous_state != current_state

    return current_state

def get_num_occupied_seats(seat_state):
    count = 0

    for row in seat_state:
        count += row.count('#')

    return count

def get_visible_seat_coords_in_direction(row, col, seat_state, row_delta, col_delta):
    # Returns the first visible seat in the given direction

    # TODO This can be cached

    while row < len(seat_state) and row >= 0 and col < len(seat_state[row]) and col >= 0:
        row += row_delta
        col += col_delta

        if row < len(seat_state) and row >= 0 and col < len(seat_state[row]) and col >= 0:
            candidate = seat_state[row][col]
            if candidate == 'L' or candidate == '#':
                return (row,col)

    return None


def get_visible_seat_coords(row, col, seat_state):
    # Returns 8 lists, each containing the coords of the seats visible in that direction

    deltas = [
        [-1, 0], # Up
        [-1, 1], # Up Right
        [0, 1], # Right
        [1, 1], # Down Righ
        [1, 0], # Down
        [1, -1], # Down Left
        [0, -1], # Left
        [-1, -1], # Up Left
    ]

    visible_seats = []

    for delta in deltas:
        row_delta = delta[0]
        col_delta = delta[1]
        visible_seats_in_direction = get_visible_seat_coords_in_direction(row, col, seat_state, row_delta, col_delta)

        visible_seats.append(visible_seats_in_direction)

    return visible_seats

def get_visible_neighbors(seat_state, row, col):
    """
    Returns a list of all the visible neighbors for the given seat
    """

    #print("Getting visible neighbors for row", row, "col", col, "Current state is ", seat_state[row][col])
    visible_seat_coords = get_visible_seat_coords(row, col, seat_state)

    #print("Neighbor coords are", visible_seat_coords)

    neighbors = []

    # Get the state of all of the visible states
    for coord in visible_seat_coords:
        if coord:
            neighbors.append(seat_state[coord[0]][coord[1]])

    return neighbors


filename = "input.txt"
current_state = read_seating(filename)


# Part 1
stable_state = get_stable_state(current_state)

print(get_num_occupied_seats(stable_state))
