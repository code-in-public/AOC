#!/usr/bin/env python

def read_input(filename):
    with open(filename) as in_file:
        return [int(line.strip()) for line in in_file.readlines()]

def is_valid_value(preamble, value):
    """
    Determines if the val is valid with the given preamble
    """

    seen = set()

    for preamble_val in preamble:
        target = value - preamble_val

        if target in seen:
            return True
        else:
            seen.add(preamble_val)

    return False

def get_invalid_value(data, preamble_size):
    """
    Retuns the first invalid value in the provided data
    """
    for idx in range(len(data)-preamble_size):
        preamble = data[idx:idx+preamble_size]
        candidate = data[idx+preamble_size]

        if not is_valid_value(preamble, candidate):
            return candidate

def get_contig_range(data, target_sum):
    """
    Returns a contiguos range of values in the data which sum to the given sum
    """

    print("Target sum", target_sum)
    possible_sums = []

    list_len = None
    last_idx = None

    for end_idx, val in enumerate(data):
        # Add the current value
        sums = [val]

        # Add the previous values
        if end_idx - 1 >= 0:
            previous_sums = possible_sums[end_idx-1]

            for start_idx, previous_sum in enumerate(previous_sums):
                new_sum = val + previous_sum
                sums.append(new_sum)

                if new_sum == target_sum:
                    list_len = start_idx + 2
                    last_idx = end_idx + 1

        possible_sums.append(sums)

    return data[last_idx-list_len:last_idx]

def get_encryption_weakness(data, preamble_size):
    invalid_val = get_invalid_value(data, preamble_size)

    contig_range = get_contig_range(data, invalid_val)

    print(contig_range)
    print(sum(contig_range))

    contig_range.sort()

    return(contig_range[0] + contig_range[-1])

# Test cases
data = [i for i in range(1,26)]

get_invalid_value(data + [26], 25)
get_invalid_value(data + [49], 25)
get_invalid_value(data + [100], 25)
get_invalid_value(data + [50], 25)

filename = "input_example.txt"
data = read_input(filename)
preamble_size = 5
print(get_encryption_weakness(data, preamble_size))

filename = "input.txt"
data = read_input(filename)
preamble_size = 25
print(get_encryption_weakness(data, preamble_size))

#print(invalid_val)

# 35 -> 35
# 20 -> 20, 55 (20 + 35)
# 15 -> 15, 35 (15 + 20), 70 (15 + 55)
#
