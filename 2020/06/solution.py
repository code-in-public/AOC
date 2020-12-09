#!/usr/bin/env python

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

def get_unique_chars(string_list):
    """
    Return the set of unique characters from the list of strings
    """
    unique_chars = set()

    for string in string_list:
        for char in string:
            unique_chars.add(char)

    return unique_chars

def get_num_unique_chars(string_list):
    return len(get_unique_chars(string_list))

def get_common_chars(string_list):
    """
    Return the characters which are found in all of the strings in the list
    """

    candidate_common_chars = set([char for char in string_list[0]])
    common_chars = candidate_common_chars

    for string in string_list[1:]:
        common_chars = set()
        for char in candidate_common_chars:
            if char in string:
                common_chars.add(char)

        candidate_common_chars = common_chars

    return common_chars

filename = "input.txt"

chunks = read_chunks_from_file(filename)

# Part 1
#print(sum([get_num_unique_chars(chunk) for chunk in chunks]))

# Part 2
print(sum([len(get_common_chars(chunk)) for chunk in chunks]))
