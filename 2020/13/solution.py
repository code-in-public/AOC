#!/usr/bin/env python3

def read_bus_schedule(filename):
    with open(filename) as in_file:
        lines = in_file.readlines()

        departure_time = int(lines[0].strip())
        bus_schedule = [int(time) if time != 'x' else None for time in lines[1].strip().split(',')]

        return departure_time, bus_schedule

def is_valid_contig_time(time, bus_schedule):
    for delta, bus_id in enumerate(bus_schedule):
        if bus_id:
            target_time = time + delta
            if target_time % bus_id != 0:
                return False

    return True

def get_largest_with_id(bus_schedule):
    largest = 0
    largest_id = 0

    for idx, bus_id in enumerate(bus_schedule):
        if bus_id and bus_id > largest:
            largest = bus_id
            largest_id = idx

    return largest_id, largest

def get_time_of_contig_departures(bus_schedule):
    print("Getting time of contiguous departures with schedule", bus_schedule)

    # Get a starting candidate time based on the largest bus id

    largest_id, largest = get_largest_with_id(bus_schedule)

    jump = largest - largest_id

    candidate_time = jump

    while True:
        if candidate_time % 1000000 == 0:
            print(candidate_time)
        if is_valid_contig_time(candidate_time, bus_schedule):
            return candidate_time
        candidate_time += largest


def get_earliest_bus(departure_time, bus_schedule):
    found = False

    bus_departure_time = departure_time

    while not found:
        for bus_interval in bus_schedule:
            if bus_interval and bus_departure_time % bus_interval == 0:
                return bus_departure_time, bus_interval

        bus_departure_time += 1

filename = "input.txt"

departure_time, bus_schedule = read_bus_schedule(filename)

# Part 1
# bus_departure_time, bus_id = get_earliest_bus(departure_time, bus_schedule)

#wait_time = bus_departure_time - departure_time

#print(wait_time, bus_id, " = ", wait_time * bus_id)

# Part 2
solution = get_time_of_contig_departures(bus_schedule)
print(solution)
