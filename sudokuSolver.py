import sys
from tkinter import *
from time import sleep
import numpy as np
from random import randint
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

#Code Provided by dataset host https://www.kaggle.com/datasets/bryanpark/sudoku?resource=download
def read_puzzels(filename):
    num_lines = sum(1 for line in open(filename))
    quizzes = np.zeros((num_lines, 81), np.int32)
    solutions = np.zeros((num_lines, 81), np.int32)
    for i, line in enumerate(open(filename, 'r').read().splitlines()[1:]):
        quiz, solution = line.split(",")
        for j, q_s in enumerate(zip(quiz, solution)):
            q, s = q_s
            quizzes[i, j] = q
            # solutions[i, j] = s
    quizzes = quizzes.reshape((-1, 9, 9))
    # solutions = solutions.reshape((-1, 9, 9))
    return quizzes



def main():
    global grid
    global total_itrs
    window = Tk()
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
    puzzles = read_puzzels('HardestDatabase.txt')
    seed = randint(0,len(puzzles)-1)
    print("Solving puzzle: {}".format(seed))
    grid = puzzles[seed]
    last_value = None
    total_itrs = 0
    done = False
    main()
