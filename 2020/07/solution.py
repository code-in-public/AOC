#!/usr/bin/env python

from collections import namedtuple
import re

ColorCount = namedtuple("ColorCount", ['color', 'count'])

def process_rule_line(rule_line):
    """
    Process the provided rule line to extact the details

    The rule result is the parent bag, followed by a list of all the other bags it must contain
    """

    rule_parts = re.split(r'bags contain', rule_line)

    parent = rule_parts[0].strip()
    children = rule_parts[1].strip()
    child_list = []

    if children == "no other bags.":
        # No children
        return parent, child_list
    else:
        # Extract the number and color of the bag
        for child in [child.strip() for child in children.split(',')]:

            #TODO Use the named typle here
            matches = re.match(r"([0-9]*)\s(.*)\s", child)
            count = int(matches.group(1))
            color = matches.group(2)

            c = ColorCount(color = color, count=count)

            child_list.append(c)


    return parent, child_list

def read_rules(filename):
    """
    Read in the rules files

    Rules are in the following format:
    'X bags contain i Y bags, j Z bags,...'
    'X bags contain no other bags.'
    """

    with open(filename) as in_file:
        return [process_rule_line(rule_line.strip()) for rule_line in in_file]

class Bag():
    def __init__(self, color):
        self.color = color
        self.children = []

    def get_color(self):
        return self.color

    def add_child(self, child, count):
        for i in range(count):
            self.children.append(child)

    def get_tree_size(self):
        child_count = len(self.children)

        for child in self.children:
            child_count += child.get_tree_size()

        return child_count

    def print_bag_tree(self):
        print(self.color)
        for child in self.children:
            child.print_bag_tree()

    def can_contain_bag(self, bag_color):
        for child in self.children:
            if child.get_color() == bag_color or child.can_contain_bag(bag_color):
                return True

        return False

def get_bag_trees(rules):
    bag_dict = {}

    for rule in rules:
        color = rule[0]
        bag_dict[color] = Bag(color)

    for rule in rules:
        parent = bag_dict[rule[0]]
        child_names = rule[1]
        for child_color_count in child_names:
            child = bag_dict[child_color_count.color]
            parent.add_child(child, child_color_count.count)

    return bag_dict

def count_trees_containing(bag_dict, target):
    count = 0
    for color in bag_dict:
        bag = bag_dict[color]
        if bag.can_contain_bag(target):
            count += 1

    return count


filename = "input.txt"
rules = read_rules(filename)

bag_dict = get_bag_trees(rules)

# Part 1
# target = "shiny gold"
# print(count_trees_containing(bag_dict, target))

bag_dict["shiny gold"].print_bag_tree()
print(bag_dict["shiny gold"].get_tree_size())
print("--------")
