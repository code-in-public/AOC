#!/usr/bin/env python3

def readExpenseReport(filename):
    with open(filename) as f:
        lines = f.readlines()

        return [int(line) for line in lines]

def getSumPair(value_list, target_sum):
    seen_values = {}

    for value in value_list:
        candidate = target_sum - value
        if candidate in seen_values:
            return candidate, value
        else:
            seen_values[value] = True

def getSumTriplet(value_list, target_sum):
    for i in range(len(value_list)):
        for j in range(len(value_list)):
            for k in range(len(value_list)):
                if (i == j) or (j == k) or (i == k):
                    continue
                else:
                    if value_list[i] + value_list[j] + value_list[k] == target_sum:
                        return value_list[i], value_list[j], value_list[k]

input_file = "input_day1.txt"
expenses = readExpenseReport(input_file)

target_value = 2020
#val1, val2 = getSumPair(expenses, target_value)

val1, val2, val3 = getSumTriplet(expenses, target_value)

print(val1 * val2 * val3)
