import sys
from tkinter import *
from time import sleep
import numpy as np
from random import randint
import argparse

sleep_time = 0.085

def print_grid():
    global grid
    for list in grid:
        print(list)
    print('\n')


def check_legal(element, location):
    global grid
    if element in grid[location[0]]:
        return False
    else:
        if element in [list[location[1]] for list in grid]:
            return False
        else:
            box_y = int(location[0] / 3) * 3
            box_x = int(location[1] / 3) * 3
            for y in range(box_y,box_y+3):
                for x in range(box_x,box_x+3):
                    if element == grid[y][x]:
                        return False
            return True

def check_location(location):
    global grid
    possible_values = []
    for i in range(1,10):
        if check_legal(i, location):
            possible_values.append(i)
    if len(possible_values) > 0:
        return possible_values
    else:
        return False

def simple_cell_solver(window,canvas):
    while True:
        global total_itrs
        global grid
        total_itrs += 1
        found_simple = False
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if grid[y][x] == 0:
                    possible_values = check_location((y,x))
                    if len(possible_values) == 1:
                        found_simple = True
                        grid[y][x] = possible_values[0]
                        if animate:
                            label = 'entry:{}{}'.format(y,x)
                            number = canvas.create_text(35+50*x, 35+50*y, font=("Purisa",'30','bold'),
                            text=grid[y][x],justify=CENTER, anchor=CENTER,fill='#3fba2f',
                            tag=label)
                            window.update()
                            sleep(sleep_time)
        if found_simple == False:
            return


def brute_solver(window,canvas):
    if not done:
        global total_itrs
        total_itrs += 1
        global grid
        global last_value
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if grid[y][x] == 0:
                    possible_values = check_location((y,x))
                    if possible_values == False:
                        return False
                    else:
                        for value in possible_values:
                            grid[y][x] = value
                            if animate:
                                label = 'entry:{}{}'.format(y,x)
                                number = canvas.create_text(35+50*x, 35+50*y, font=("Purisa",'30','bold'),
                                text=grid[y][x],justify=CENTER, anchor=CENTER,fill='#d12828',
                                tag=label)
                                window.update()
                                sleep(sleep_time)
                            brute_solver(window,canvas)
                            if grid[last_value[0]][last_value[1]] != 0:
                                return True
                            grid[y][x] = 0
                            if animate:
                                canvas.delete(number)
                                window.update()
                                sleep(sleep_time)
                        return True

def find_last(grid):
    for y in range(len(grid)-1,-1,-1):
        for x in range(len(grid[y])-1,-1,-1):
            if grid[y][x] == 0:
                return (y,x)
    return True

def make_base(window):
    global grid
    canvas = Canvas(window, width=470, height=470, bd=0, highlightthickness=0)
    for i in range(10):
        canvas.create_line(10, i*50+10, 460, i*50+10 )
        canvas.create_line(i*50+10, 10, i*50+10, 460 )
    for y in range(9):
        for x in range(9):
            if grid[y][x] != 0:
                label = 'entry:{}{}'.format(y,x)
                canvas.create_text(35+50*x, 35+50*y, font=("Purisa",'30','bold'),
                text=grid[y][x],justify=CENTER, anchor=CENTER,fill='#2622a3',
                tag=label)
    canvas.pack(fill=BOTH, expand=1)
    return canvas

#Base code provided by dataset host https://www.kaggle.com/datasets/bryanpark/sudoku?resource=download
def read_puzzels(filename,size):
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
                q = ord(q) - 54
            quizzes[i, j] = q
            # solutions[i, j] = s
    quizzes = quizzes.reshape((-1, size, size))
    # solutions = solutions.reshape((-1, 9, 9))
    return quizzes

def main():
    global grid
    global total_itrs
    global animate
    window = Tk()
    canvas = Canvas()
    if animate:
        window.title("Sudoku Solver")
        window.title = "Game"
        window.geometry("470x470")
        canvas = make_base(window)
    simple_cell_solver(window, canvas)
    global last_value
    last_value = find_last(grid)
    if brute_solver(window, canvas) == True or last_value == True:
        sleep(1)
        print("solved in {} interations".format(total_itrs))
        print_grid()
    else:
        print("No Solution Possible")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sudoku Solver")
    parser.add_argument("-a", "--animate", action="store_true",default=False,
                        help="Animates the solution")
    parser.add_argument("-f", "-file", default=False, help="Provide a filename with puzzles")
    parser.add_argument("-s", "-size", default=9,type=int, help="Puzzle size: enter 9 for a regular sudoku")
    args = parser.parse_args()
    animate = False
    if args.animate:
        animate = True
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
    if args.f != False:
        puzzles = read_puzzels(args.f,args.s)
        seed = randint(0,len(puzzles)-1)
        grid = puzzles[seed]
        print("Solving puzzle: {}".format(seed))
        print_grid()
    last_value = None
    total_itrs = 0
    done = False
    exit()
    main()
