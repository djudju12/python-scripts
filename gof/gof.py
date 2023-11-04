#!/usr/bin/python3
import random
from time import sleep
import os


ALIVE_CODE = "\N{ESC}[47m  \u001b[0m"
DEAD_CODE = "  "

ALIVE = 1
DEAD = 0

COLS, ROWS = os.get_terminal_size()
COLS = int(COLS / 2)

TOTAL_GENS = 300

def random_board(rows, cols, density):
    board = [[DEAD for _ in range(cols)] for _ in range(rows)]
    for row in range(rows):
        for col in range(cols):
            if random.random() < density:
                board[row][col] = ALIVE

    return board

INIT_BOARD = [[DEAD for _ in range(COLS)] for _ in range(ROWS)]

X, Y = int(ROWS/2)-2, int(COLS/2)-5

INIT_BOARD[X+0][Y+2] = ALIVE
INIT_BOARD[X+1][Y+2] = ALIVE
INIT_BOARD[X+2][Y+2] = ALIVE
INIT_BOARD[X+2][Y+1] = ALIVE
INIT_BOARD[X+1][Y+0] = ALIVE

INIT_BOARD[X+3][Y+11] = ALIVE
INIT_BOARD[X+4][Y+9]  = ALIVE
INIT_BOARD[X+4][Y+10] = ALIVE
INIT_BOARD[X+5][Y+10] = ALIVE
INIT_BOARD[X+5][Y+11] = ALIVE

BOARD = INIT_BOARD

def printboard():
    for row in range(ROWS):
        for col in range(COLS):
            if BOARD[row][col] == ALIVE:
                print(ALIVE_CODE, end="")
            else:
                print(DEAD_CODE, end="")
        print()

def count_neighbors(row, col):
    count = 0
    for i in range(-1, 2, 1):
        for j in range(-1, 2, 1):
            nb_row = row + i
            nb_col = col + j

            if (nb_row, nb_col)  == (row, col):
                continue

            if nb_col >= COLS or nb_col < 0:
                continue

            if nb_row >= ROWS or nb_row < 0:
                continue

            if BOARD[nb_row][nb_col] == ALIVE:
                count += 1

            if count > 3:
                return count

    return count

def next_gen():
    global BOARD
    NEXT_BOARD = [[DEAD for _ in range(COLS)] for _ in range(ROWS)]
    for row in range(ROWS):
        for col in range(COLS):
            nb_c = count_neighbors(row, col)
            if nb_c == 3:
                NEXT_BOARD[row][col] = ALIVE
            elif nb_c == 2 and BOARD[row][col] == ALIVE:
                NEXT_BOARD[row][col] = ALIVE

    BOARD = NEXT_BOARD

def clear():
    print("\033[H\033[2J\033[3J")

def gof(total):
    clear()
    while True:
        printboard()

        if total == 0:
            break

        next_gen()
        total -= 1
        sleep(0.1)
        clear()

def main():
    global BOARD, INIT_BOARD
    while True:
        gof(TOTAL_GENS)
        BOARD = INIT_BOARD


main()