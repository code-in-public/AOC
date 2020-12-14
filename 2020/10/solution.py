#!/usr/bin/env python3

def get_adapters(filename):
    with open(filename) as in_file:
        adapters = [int(adapter.strip()) for adapter in in_file.readlines()]
        adapters.sort()

        return adapters


def get_delta_counts(value_list):
    print(value_list)
    delta_counts = {}

    for idx in range(1, len(value_list)):
        delta = value_list[idx] - value_list[idx-1]

        if delta in delta_counts:
            delta_counts[delta] += 1
        else:
            delta_counts[delta] = 1

    return delta_counts

cache = {}

def get_num_arrangements(start, options, end, current_path):
    """
    Returns the number of ways that the options can be arranged to get from the start to end using the options
    """

    cache_key = (start, end)

    if cache_key in cache:
        return cache[cache_key]

    jump_size = 3

    # Get the valid options
    valid_options = [option for option in options if option - start <= jump_size and option > start]

    if (valid_options):
        count = 0
        # With options
        for option in valid_options:
            current_path.append(option)
            count += get_num_arrangements(option, options, end, current_path)
            current_path.pop()

        cache[cache_key] = count
    else:
        # Base cases
        if (end - start <= jump_size):
            #print("start", start, "end", end, "Current -", current_path)
            cache[cache_key] = 1
        else:
            cache[cache_key] = 0

    return cache[cache_key]

def get_delta_counts(adapters):
    # Add the device and outlet
    adapters.insert(0,0)
    adapters.append(adapters[-1]+3)

    delta_counts = get_delta_counts(adapters)
    print(delta_counts[1] * delta_counts[3])

    return delta_counts

filename = "input.txt"

# Part 1
adapters = get_adapters(filename)
#adapters = [1, 4, 5, 6]
end = adapters[-1]+3

# Part 2
print("Done ---", get_num_arrangements(0, adapters, end, []))
