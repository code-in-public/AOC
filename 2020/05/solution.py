#!/usr/bin/env python

import math

def getPartionIndex(partion, size, front_char, back_char):
    front = 0
    back = size - 1
    mid = (front + back)/2

    #print(front, mid, back)

    for ch in partion:
        if ch == front_char:
            back = math.floor(mid)
        if ch == back_char:
            front = math.ceil(mid)

        mid = (front + back)/2

        #print(front, mid, back)

    return front

def getSeatId(partion):

    num_rows = 128
    num_cols = 8

    row = getPartionIndex(partion, num_rows, 'F', 'B')
    col = getPartionIndex(partion, num_cols, 'L', 'R')

    return (row * 8) + col

def getSeatIds(partions):
    return [getSeatId(partion) for partion in partions]

def getPartions(filename):
    with open(filename) as file:
        partions = file.readlines()

        return [partion.strip() for partion in partions]


def findMissingSeatId(seatIds):
    for idx,seatId in enumerate(seatIds):
        if (idx > 0 and idx < len(seatIds) -1):
            if (seatIds[idx - 1] != seatIds[idx] - 1):
                print(seatIds[idx - 1])
                print(seatIds[idx])
                print(seatIds[idx + 1])

filename = "input.txt"

seatIds = getSeatIds(getPartions(filename))
seatIds.sort()

findMissingSeatId(seatIds)
