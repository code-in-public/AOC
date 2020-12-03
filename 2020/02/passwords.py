#!/usr/bin/env python3

# Parse the password file lines
def parsePassword(passwordLine):
    p_range, p_char, password = passwordLine.strip().split(" ")

    p_range_min, p_range_max = p_range.split("-")
    p_char = p_char[0]

    return int(p_range_min), int(p_range_max), p_char, password

# Read in the password files
def readPasswordFile(filename):
    with open(filename) as f:
        lines = f.readlines()

        return [parsePassword(line) for line in lines]

# Validate a given password
def validatePassword(p_min, p_max, p_char, password):
    # Determine how many times the character occured

    p_occurances = [char for char in password if char == p_char]
    p_char_count = len(p_occurances)

    is_valid = p_char_count >= p_min and p_char_count <= p_max
    return is_valid

# Validate the password based on policy v2
def validatePasswordV2(idx_1, idx_2, p_char, password):
    # Get the characters at the indexes
    p_char_1 = password[idx_1-1]
    p_char_2 = password[idx_2-1]

    is_valid = p_char_1 != p_char_2 and (p_char_1 == p_char or p_char_2 == p_char)

    return is_valid

def getValidPasswords(filename):
    passwordEntries = readPasswordFile(filename)
    valid_passwords = []
    for entry in passwordEntries:
        if validatePasswordV2(entry[0], entry[1], entry[2], entry[3]):
            valid_passwords.append(entry[3])

    return valid_passwords

filename = "input_day2.txt"
print(len(getValidPasswords(filename)))
