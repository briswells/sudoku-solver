import sys
from tk import *
from time import sleep, time
import numpy as np
from random import randint, sample
import argparse
from math import sqrt
import matplotlib.pyplot as plt
sleep_time = 0.065

def average(list):
    return sum(list) / len(list)

def print_grid():
    global grid
    for list in grid:
        print(list)
    print('\n')

#check if a number can be placed in a cell
def check_legal(element, location):
    global grid
    global args
    scale_factor = int(sqrt(args.s)) #Updates box size based on grid size
    if element in grid[location[0]]: #Checks row for val
        return False
    else:
        if element in [list[location[1]] for list in grid]: #Checks col for val
            return False
        else: #checks box for val
            box_y = int(location[0] / scale_factor) * scale_factor
            box_x = int(location[1] / scale_factor) * scale_factor
            for y in range(box_y,box_y+scale_factor):
                for x in range(box_x,box_x+scale_factor):
                    if element == grid[y][x]:
                        return False
            return True

#finds all nums that can go into cell
def check_location(location):
    global grid
    global args
    global possible_grid
    possible_values = []
    for i in range(1,args.s+1):
        if check_legal(i, location):
            possible_values.append(i)
    if len(possible_values) > 0:
        return possible_values
    else:
        return False

#Recursive function that tries all possiblities until solution is found
def brute_solver():
    if not done:
        global total_itrs
        global grid
        global last_value
        total_itrs += 1
        for y in range(len(grid)): #loops through grid until blank cell is found
            for x in range(len(grid[y])):
                if grid[y][x] == 0:
                    possible_values = check_location((y,x))
                    if possible_values == False:
                        return False
                    else:
                        for value in possible_values:
                            grid[y][x] = value #Places val into cell
                            brute_solver() #recurs with updated grid
                            if grid[last_value[0]][last_value[1]] != 0:
                                return True #if grid is completed returns true
                            grid[y][x] = 0 #undo's grid update and continues to next possible val
                        return True

#Finds the last blank value in grid
def find_last(grid):
    for y in range(len(grid)-1,-1,-1):
        for x in range(len(grid[y])-1,-1,-1):
            if grid[y][x] == 0:
                return (y,x)
    return True

#Reads in puzzle files and parses them into grid
#Base code provided by dataset host https://www.kaggle.com/datasets/bryanpark/sudoku?resource=download
#Then modified to accept more grid types
def read_puzzles(filename,size):
    num_lines = sum(1 for line in open(filename))
    quizzes = np.zeros((num_lines-1, size**2), np.int32)
    solutions = np.zeros((num_lines-1, size**2), np.int32)
    for i, line in enumerate(open(filename, 'r').read().splitlines()[1:]):
        quiz, solution = line.split(",")
        for j, q_s in enumerate(zip(quiz, solution)):
            q, s = q_s
            try:
                q = int(q)
            except ValueError:
                q = ord(q) - 55
            quizzes[i, j] = q
            # solutions[i, j] = s
    quizzes = quizzes.reshape((-1, size, size))
    return quizzes

def main():
    global grid
    global total_itrs
    global args
    global last_value
    ave_time = []
    ave_iters = []
    puzzles = read_puzzles(args.f,args.s)
    if args.f != False: #reads in puzzle files and solves random puzzle
        samples = sample(range(0,len(puzzles)-1), args.i)

    for i in range(args.i):
        if args.f != False:
            grid = puzzles[samples[i]]
            print_grid()
        total_itrs = 0
        start_time = time() #starts timer here to avoid IO distorting data
        last_value = find_last(grid) #Finds last blank, returns true if simple solver filled grid
        brute_solver()
        print("Solved problem {}".format(i))
        ave_time.append(time() - start_time)
        ave_iters.append(total_itrs)
        print_grid()
    print("Solve {} puzzles".format(args.i))
    print("Average runtime: %s seconds" % (average(ave_time)))
    print("Solved in an average of {} interations".format(average(ave_iters)))
    plt.hist(ave_time)
    plt.savefig('{}_{}.png'.format(ave_time,args.i))
    plt.hist(ave_iters)
    plt.savefig('{}_{}.png'.format(ave_iters,args.i))

if __name__ == "__main__":
    #Parces command line args
    parser = argparse.ArgumentParser(description="Sudoku Solver")
    parser.add_argument("-a", "--animate", action="store_true",default=False,
                        help="Animates the solution")
    parser.add_argument("-f", "-file", default=False, help="Provide a filename with puzzles")
    parser.add_argument("-s", "-size", default=9,type=int, help="Puzzle size: enter 9 for a regular sudoku")
    parser.add_argument("-i", "-iters", default=1,type=int, help="Number of Puzzles to be tested")
    args = parser.parse_args()
    puzzles = []
    #Base grids for tested matrix sizes
    if args.s == 9:
        grid = [[3, 0, 6, 5, 0, 8, 4, 0, 0],
              [5, 2, 0, 0, 0, 0, 0, 0, 0],
              [0, 8, 7, 0, 0, 0, 0, 3, 1],
              [0, 0, 3, 0, 1, 0, 0, 8, 0],
              [9, 0, 0, 8, 6, 3, 0, 0, 5],
              [0, 5, 0, 0, 9, 0, 6, 0, 0],
              [1, 3, 0, 0, 0, 0, 2, 5, 0],
              [0, 0, 0, 0, 0, 0, 0, 7, 4],
              [0, 0, 5, 2, 0, 6, 3, 0, 0]]
    if args.s == 16:
        grid =[[9,0,0,6,0,0,14,3,5,0,0,0,0,13,0,0],
            [0,0,0,16,0,7,0,0,8,0,0,0,5,6,0,0],
            [4,0,0,0,8,0,12,0,2,0,6,0,0,16,0,0],
            [0,14,11,0,0,0,0,0,4,0,3,7,0,0,0,0],
            [15,0,14,0,6,0,0,1,0,0,0,0,0,0,0,0],
            [0,0,4,0,0,0,3,0,0,9,0,0,7,14,0,12],
            [0,0,0,0,2,0,8,14,6,0,12,0,0,0,0,0],
            [0,12,8,0,7,9,16,5,0,3,11,0,0,0,6,0],
            [0,8,0,15,0,0,0,0,0,0,0,3,2,0,0,5],
            [3,1,0,0,14,15,0,0,13,0,0,0,0,9,11,0],
            [5,0,0,12,0,11,0,0,0,0,16,0,0,0,13,4],
            [11,7,13,0,0,0,4,0,0,0,15,0,0,0,0,0],
            [0,15,0,3,0,0,11,13,16,0,14,0,0,0,0,9],
            [7,0,0,0,5,0,0,6,0,0,0,2,0,0,1,0],
            [1,0,16,13,4,0,0,0,0,5,0,0,0,11,8,0],
            [0,0,5,0,0,8,1,0,0,0,9,11,3,4,0,0]]
    last_value = None
    total_itrs = 0 #Counts total runs through matrix
    done = False
    main()
