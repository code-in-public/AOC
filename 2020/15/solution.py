#!/usr/bin/env python3

def get_nth_answer(input, n):
    print("Getting nth solution", input, n)

    times_spoken = {}

    current_turn = 1
    last_number = None

    # Populate the time spoken dict and current turn
    for num in input:
        if num not in times_spoken:
            times_spoken[num] = []

        times_spoken[num].append(current_turn)

        current_turn += 1


    while current_turn <= n:
        previously_spoken_number = input[current_turn - 2]

        previously_spoken_times = times_spoken[previously_spoken_number]

        if previously_spoken_times == None:
            next_number = 0
        else:
            if (len(previously_spoken_times) == 1):
                next_number = 0
            else:
                next_number = previously_spoken_times[-1]-previously_spoken_times[-2]

        input.append(next_number)

        if next_number not in times_spoken:
            times_spoken[next_number] = []
        times_spoken[next_number].append(current_turn)

        current_turn += 1

    return input[-1]


tests = [
    [1, 3, 2],
    [2, 1, 3],
    [1, 2, 3],
    [2, 3, 1],
    [3, 2, 1],
    [2, 1, 3],
]

n = 30000000

#for input in tests:
#    print(get_nth_answer(input, n))

input = [19, 0, 5, 1, 10, 13]
print(get_nth_answer(input, n))
