# Caleb Ellington
# 11/10/2019
# For Ruby

import random
import numpy as np

# difficulty: (mines, board_size)
difficulties = {0: (1, 1),
                1: (9, 10),
                2: (40, 13),
                3: (99, 20),
                4: (500, 40)
                }

class Minesweeper():

    def __init__(self, mines, size):
        self.minefield = np.zeros(shape=(size, size)).astype(int)
        self.display = [['X' for x in range(size)] for y in range(size)]
        self.board = np.zeros(shape=(size, size)).astype(int)
        # generate minefield
        while mines > 0:
            (x, y) = (random.randint(0, size-1), random.randint(0, size-1))
            if self.minefield[y][x] != 1:
                self.minefield[y][x] = 1
                mines -= 1
        # generate board
        for y in range(size):
            for x in range(size):
                if self.minefield[y][x] == 1:
                    self.board[y][x] = -1
                else:
                    y_start = max(0, y-1)
                    y_end = min(size-1, y+2)
                    x_start = max(0, x-1)
                    x_end = min(size-1, x+2)
                    window = self.minefield[y_start:y_end, x_start:x_end]
                    num_mines = int(np.sum(window))
                    self.board[y][x] = num_mines

    def reveal(self, x, y):
        raise NotImplementedError

    def flag(self, x, y):
        raise NotImplementedError

    def get_display(self):
        return self.display

    def get_mines(self):
        return self.minefield

    def get_board(self):
        return self.board


def print_arr(arr):
    for y in range(len(arr)):
        line = f"{y} "
        for x in range(len(arr)):
            val = arr[y][x]
            if val == -1:
                val = 'M'
            line += f" {val}"
        print(line)
    line = "\n  "
    for x in range(len(arr)):
        line += f" {x}"
    print(line)


def play_game(difficulty):
    print("generating board...")
    (mines, board_size) = difficulties[difficulty]
    print(f"mines: {mines}, board_size: {board_size}")
    game = Minesweeper(mines, board_size)
    print_arr(game.get_board())
    print()
    print_arr(game.get_display())
    print()

def difficulty_select():
    valid_difficulties = [0, 1, 2, 3, 4]
    difficulty = input("Difficulty level (1,2,3): ")
    try:
        difficulty = int(difficulty)
    except ValueError:
        print(f"\"{difficulty}\"... SeLeCt A dIfFiCuLtY")
    if not difficulty in valid_difficulties:
        return difficulty_select()
    return difficulty


def main():
    option_select = input("New game (n) or quit (q): ")
    while option_select != 'q':
        print("\n###############################")
        print("#   Welcome to Minesweeper!   #")
        print("###############################")
        difficulty = difficulty_select()
        play_game(difficulty)
        option_select = input("New game (n) or quit (q): ")
    print("Thanks for playing! Goodbye")
    exit(0)

main()