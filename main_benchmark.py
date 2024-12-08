import sys
import math
import os
import numpy as np
import random

def is_local():
    return os.name == 'nt'

def log(*args):
    if is_local():
        print(*args)

class TapePos:
    def __init__(self, wrap, distance, index):
        self.band = wrap//52
        self.wrap = wrap
        self.distance = distance
        self.index = index
        self.direction = wrap%2


def calc_move_cost(from_pos, to_pos):
    time_cost = 0.0
    if from_pos.band != to_pos.band:
        time_cost += 4
    if from_pos.wrap != to_pos.wrap:
        time_cost += 1
    wrap = to_pos.wrap
    if to_pos.direction == 0:
        anchor_distance = math.floor(to_pos.distance / 30) * 30
        if from_pos.distance < anchor_distance:
            time_cost += (anchor_distance - from_pos.distance) / 8 + (to_pos.distance - anchor_distance) / 2
        elif from_pos.distance <= to_pos.distance:
            time_cost += (to_pos.distance - from_pos.distance) / 2
        else:
            time_cost += (from_pos.distance - anchor_distance) / 8 + (to_pos.distance - anchor_distance) / 2
            time_cost += 2.5
    else:
        anchor_distance = math.ceil(to_pos.distance / 30) * 30
        if from_pos.distance > anchor_distance:
            time_cost += (from_pos.distance - anchor_distance) / 8 + (anchor_distance - to_pos.distance) / 2
        elif from_pos.distance >= to_pos.distance:
            time_cost += (from_pos.distance - to_pos.distance) / 2
        else:
            time_cost += (anchor_distance - from_pos.distance) / 8 + (anchor_distance - to_pos.distance) / 2
            time_cost += 2.5
    return time_cost


def output_move(output_file, from_pos, to_pos):
    output_file.write(f"begin {from_pos.wrap} {from_pos.distance} 0 0\n")
    time_cost = 0.0
    if from_pos.band != to_pos.band:
        time_cost += 4
    if from_pos.wrap != to_pos.wrap:
        time_cost += 1
        output_file.write(f"wrap {from_pos.wrap} {from_pos.distance} {to_pos.wrap} {from_pos.distance}\n")
    wrap = to_pos.wrap
    if to_pos.direction == 0:
        anchor_distance = math.floor(to_pos.distance / 30) * 30
        if from_pos.distance < anchor_distance:
            time_cost += (anchor_distance - from_pos.distance) / 8 + (to_pos.distance - anchor_distance) / 2
            output_file.write(f"anchor {wrap} {from_pos.distance} {wrap} {anchor_distance}\n")
            output_file.write(f"move {wrap} {anchor_distance} {wrap} {to_pos.distance}\n")
        elif from_pos.distance <= to_pos.distance:
            time_cost += (to_pos.distance - from_pos.distance) / 2
            output_file.write(f"move {wrap} {from_pos.distance} {wrap} {to_pos.distance}\n")
        else:
            time_cost += (from_pos.distance - anchor_distance) / 8 + (to_pos.distance - anchor_distance) / 2
            time_cost += 2.5
            output_file.write(f"anchor {wrap} {from_pos.distance} {wrap} {anchor_distance}\n")
            output_file.write(f"move {wrap} {anchor_distance} {wrap} {to_pos.distance}\n")
    else:
        anchor_distance = math.ceil(to_pos.distance / 30) * 30
        if from_pos.distance > anchor_distance:
            time_cost += (from_pos.distance - anchor_distance) / 8 + (anchor_distance - to_pos.distance) / 2
            output_file.write(f"anchor {wrap} {from_pos.distance} {wrap} {anchor_distance}\n")
            output_file.write(f"move {wrap} {anchor_distance} {wrap} {to_pos.distance}\n")
        elif from_pos.distance >= to_pos.distance:
            time_cost += (from_pos.distance - to_pos.distance) / 2
            output_file.write(f"move {wrap} {from_pos.distance} {wrap} {to_pos.distance}\n")
        else:
            time_cost += (anchor_distance - from_pos.distance) / 8 + (anchor_distance - to_pos.distance) / 2
            time_cost += 2.5
            output_file.write(f"anchor {wrap} {from_pos.distance} {wrap} {anchor_distance}\n")
            output_file.write(f"move {wrap} {anchor_distance} {wrap} {to_pos.distance}\n")
    output_file.write(f"end 0 0 {to_pos.wrap} {to_pos.distance}\n")
    return time_cost


tape_pos_list = []

def read():
    if is_local():
        sys.stdin = open('input.txt', 'r')
    global tape_pos_list
    tape_pos_num = int(input())
    for i in range(tape_pos_num):
        inp = input().split()
        w = int(inp[0])
        d = float(inp[1])
        tape_pos_list += [TapePos(w, d, i)]
    tape_pos_list += [TapePos(0, 0, tape_pos_num)]
    

def save_shedule(tour):
    output_file = open("schedule_benchmark.txt", 'w')
    global tape_pos_list
    num = len(tour)
    cost = 0
    for i in range(num):
        j = i + 1
        if j == num :
            j = 0
        cost += output_move(output_file, tape_pos_list[tour[i]], tape_pos_list[tour[j]])
    output_file.write(f"cost {cost} 0 0 0")
    output_file.close()
        

def solve():
    global tape_pos_list
    tape_pos_num = len(tape_pos_list)
    log("Tape Pos Num:", tape_pos_num)

    tape_pos_sorted = []
    for pos in tape_pos_list:
        tape_pos_sorted.append(pos)
    tape_pos_sorted = sorted(tape_pos_sorted, key=lambda x: (x.distance, x.wrap))
    best_tour = [x.index for x in tape_pos_sorted]
    log("Best tour:", best_tour)
    print(' '.join(str(x) for x in best_tour[1:]))
    if is_local():
        save_shedule(best_tour)

if __name__ == "__main__":
    read()
    solve()