#!/usr/bin/env python3

import re

# Reads in chunks of raw passport data from the input file
def read_file(filename):
    passport_data = []
    # Read the passport data from the file
    with open(filename) as file:
        lines = file.readlines()

        current_passport = []

        for line in lines:
            if line == '\n':
                passport_data.append(current_passport)

                current_passport = []
            else:
                current_passport.append(line)

        passport_data.append(current_passport)

    return passport_data

# Parse the raw passport data to remove newlines and extract the fields on the same line
def parse_passport_data(passport_data):
    parsed_data = []
    for raw_passport in passport_data:

        parsed_passport_fields = []

        for line in raw_passport:
            for field in line.strip().split():
                parsed_passport_fields.append(field)

        parsed_data.append(parsed_passport_fields)

    return parsed_data

# Convert the parsed passport data into passport dicts
def get_passport_dicts(parsed_passport_data):
    passport_dicts = []
    for passport_array in parsed_passport_data:
        passport_dict = {}
        for field_and_value in passport_array:
            field, value = field_and_value.split(':')

            passport_dict[field] = value

        passport_dicts.append(passport_dict)

    return passport_dicts

def validate_range(name, value, min_value, max_value):

    value_int = int(value)

    if value_int >= min_value and value_int <= max_value:
        return True
    else:
        print("Invalid range for ", name, value)
        return False

def validate_birth_year(birth_year):
    return validate_range("Birth year", birth_year, 1920, 2002)

def validate_issue_year(issue_year):
    return validate_range("Issue year", issue_year, 2010, 2020)

def validate_expiration_year(expiration_year):
    return validate_range("Expiration year", expiration_year, 2020, 2030)

def validate_height(height):
    # Extract the unit
    if height[-2:] == "cm":
        height = height[:-2]
        return validate_range("Height in CM", height, 150, 193)

    if height[-2:] == "in":
        height = height[:-2]
        return validate_range("Height in INCH", height, 59, 76)

    print("Invalid height unit", height)
    return False

def validate_hair_colour(colour):
    # a # followed by exactly six characters 0-9 or a-f.
    if len(re.findall(r"^#[0-9a-f]{6}$",colour)) == 1:
        return True
    else:
        print("Invalid hair color", colour)
        return False

def validate_eye_colour(colour):
    # exactly one of: amb blu brn gry grn hzl oth.

    valid_eye_colours = [
        "amb",
        "blu",
        "brn",
        "gry",
        "grn",
        "hzl",
        "oth",
    ]

    if colour in valid_eye_colours:
        return True
    else:
        print("Invalid eye color", colour)
        return False

def validate_passport_id(passport_id):
    # a nine-digit number, including leading zeroes.
    if len(re.findall(r"^[0-9]{9}$", passport_id)) == 1:
        return True
    else:
        print("Invalid passport id", passport_id)
        return False

# Determines if a password is valid
def is_valid(passport_dict):
    required_fields = [
        "byr", # Birth year
        "iyr", # Issue year
        "eyr", # Expiration year
        "hcl", # Hair colour
        "hgt", # Height
        "ecl", # Eye Color
        "pid", # Passport id
        #"cid",
    ]

    for required_field in required_fields:
        if required_field not in passport_dict:
            print("Invalid", passport_dict, " Missing ", required_field)
            return False

    # Validate Values
    if (validate_birth_year(passport_dict["byr"]) and
        validate_issue_year(passport_dict["iyr"]) and
        validate_expiration_year(passport_dict["eyr"]) and
        validate_height(passport_dict["hgt"]) and
        validate_hair_colour(passport_dict["hcl"]) and
        validate_eye_colour(passport_dict["ecl"]) and
        validate_passport_id(passport_dict["pid"])
    ):
        print("Valid", passport_dict)
        return True

    return False

# Returns only the valid passports
def get_valid_passports(passport_dicts):
    return [passport_dict for passport_dict in passport_dicts if is_valid(passport_dict)]

def get_valid_passport_count(filename):
    passport_data = read_file(filename)
    parsed_passport_data = parse_passport_data(passport_data)

    passport_dicts = get_passport_dicts(parsed_passport_data)

    valid_passports = get_valid_passports(passport_dicts)

    return len(valid_passports)

all_invalid_filename = "input_day4_example_invalid.txt"
print(get_valid_passport_count(all_invalid_filename))

all_valid_filename = "input_day4_example_valid.txt"
print(get_valid_passport_count(all_valid_filename))

filename = "input_day4.txt"
print(get_valid_passport_count(filename))
