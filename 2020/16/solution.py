#!/usr/bin/env python3

from collections import namedtuple

def read_chunks_from_file(filename):
    """
    Read in chunked data from the given file and return the list of chunks
    Chunks of data are any set of lines seperated by empty lines.
    """

    chunks = []
    current_chunk = []

    with open(filename) as in_file:
        for line in in_file:
            if line.strip() == "":
                # Reached the end of the current chunk
                chunks.append(current_chunk)
                current_chunk = []
            else:
                # Add to the current chunk
                current_chunk.append(line.strip())

        if(current_chunk):
            chunks.append(current_chunk)

    return chunks

Range = namedtuple("Range", ["min_value", "max_value"])
ValidRange = namedtuple("ValidRange", ["name", "valid_ranges"])

def parse_range(range_data):

    ranges = []

    range_strings = range_data.split("or")

    for range_string in range_strings:
        range_values = [int(val.strip()) for val in range_string.split('-')]
        ranges.append(Range(range_values[0], range_values[1]))

    return ranges

def parse_valid_ranges(valid_range_data):
    results = []
    for valid_range_entry in valid_range_data:
        name, range_data = valid_range_entry.split(":")

        valid_ranges = parse_range(range_data)

        valid_range = ValidRange(name.strip(), valid_ranges)
        results.append(valid_range)

    return results

def parse_nearby_tickets(nearby_ticket_data):
    # Remove the heading
    nearby_ticket_data = nearby_ticket_data[1:]
    nearby_tickets = []

    for ticket in nearby_ticket_data:
        values = [int(val.strip()) for val in ticket.split(',')]
        nearby_tickets.append(values)

    return nearby_tickets

def is_valid_value(valid_ranges, value):
    for valid_range in valid_ranges:
        for valid_range in valid_range.valid_ranges:
            if value <= valid_range.max_value and value >= valid_range.min_value:
                return True
    return False

def get_invalid_ticket_values(valid_ranges, tickets):

    invalid_values = []
    for ticket in tickets:
        for value in ticket:
            if not is_valid_value(valid_ranges, value):
                invalid_values.append(value)

    return invalid_values

def is_valid_ticket(valid_ranges, ticket):
    for value in ticket:
        if not is_valid_value(valid_ranges, value):
            return False

    return True

def get_valid_tickets(valid_ranges, tickets):
    """
    Filters out all invalid tickets, return a list of only those which are
    """

    return [ticket for ticket in tickets if is_valid_ticket(valid_ranges, ticket)]

def parse_your_ticket(your_ticket_data):
    your_ticket_data = your_ticket_data[1:][0]

    values = [int(val.strip()) for val in your_ticket_data.split(',')]

    return values

def read_ticket_data(filename):
    chunks = read_chunks_from_file(filename)

    valid_range_data = chunks[0]
    your_ticket_data = chunks[1]
    nearby_ticket_data = chunks[2]

    valid_ranges = parse_valid_ranges(valid_range_data)
    nearby_tickets = parse_nearby_tickets(nearby_ticket_data)
    your_ticket = parse_your_ticket(your_ticket_data)

    return valid_ranges, nearby_tickets, your_ticket

def get_candidate_valid_ranges(valid_ranges):

    # Populate the initial set of candidate fields, assuming all valid ranges for all fields
    candidate_ranges = {}

    for field_idx in range(len(valid_ranges)):
        candidate_ranges[field_idx] = []
        for valid_range in valid_ranges:
            candidate_ranges[field_idx].append(valid_range)

    return candidate_ranges

def update_candidate_ranges_with_ticket(candidate_ranges, ticket):
    updated_candidate_ranges = {}

    for value_idx, value in enumerate(ticket):
        valid_ranges = []
        candidate_range_list = candidate_ranges[value_idx]
        for candidate_range in candidate_range_list:
            # Check if the candidate range fits the current value
            valid = is_valid_value([candidate_range], value)

            if valid:
                valid_ranges.append(candidate_range)
            else:
                pass

        #print("Valid ranges for value at", value_idx, "of", value, "is", valid_ranges)
        updated_candidate_ranges[value_idx] = valid_ranges

    return updated_candidate_ranges

def prune_candidate_ranges(candidate_ranges):
    #print("Candidate_ranges", candidate_ranges)

    changed = True

    while changed:
        changed = False
        finalized_ranges_names = set()
        idx = 0
        while idx < len(candidate_ranges):
            #print("Checking ", idx, candidate_ranges[idx])

            if len(candidate_ranges[idx]) == 1:
                #print("Found a match ", idx, candidate_ranges[idx][0])
                if candidate_ranges[idx][0].name not in finalized_ranges_names:
                    finalized_ranges_names.add(candidate_ranges[idx][0].name)
                    idx = 0
                    continue
            else:
                # Remove all of the single entry names from this list
                new_valid_ranges = []
                for valid_range in candidate_ranges[idx]:
                    if valid_range.name not in finalized_ranges_names:
                        new_valid_ranges.append(valid_range)
                    else:
                        changed = True

                candidate_ranges[idx] = new_valid_ranges

            idx += 1


    return candidate_ranges

def update_candidate_ranges_with_tickets(candidate_ranges, tickets):
    for ticket in tickets:
        candidate_ranges = update_candidate_ranges_with_ticket(candidate_ranges, ticket)

        #print("Updated candidate ranges are:")
        #for idx in candidate_ranges:
        #    print(idx, "-", [range.name for range in candidate_ranges[idx]])

        candidate_ranges = prune_candidate_ranges(candidate_ranges)

        #TODO Stop ealy if only 1 range exists per field

    return candidate_ranges

def identify_ticket_fields(valid_ranges, tickets):
    candidate_ranges = get_candidate_valid_ranges(valid_ranges)

    # Update the candidate ranges for each ticket
    candidate_ranges = update_candidate_ranges_with_tickets(candidate_ranges, tickets)

    return candidate_ranges

def print_candidates(candidate_ranges):
    for idx in candidate_ranges:
        print(idx, "-", [range.name for range in candidate_ranges[idx]])

def print_ticket(ticket_fields, ticket):
    total = 1
    for idx, ticket_value in enumerate(ticket):
        field_name = ticket_fields[idx][0].name

        if field_name.startswith("departure"):
            print(field_name, ticket_value)
            total *= ticket_value


    print(total)

#filename = "input_example_2.txt"
filename = "input.txt"
valid_ranges, nearby_tickets, your_ticket = read_ticket_data(filename)

# Part 1
#invalid_values = get_invalid_ticket_values(valid_ranges, nearby_tickets)
#print(sum(invalid_values))

# Part 2
valid_tickets = get_valid_tickets(valid_ranges, nearby_tickets)

ticket_fields = identify_ticket_fields(valid_ranges, valid_tickets)

print_ticket(ticket_fields, your_ticket)
