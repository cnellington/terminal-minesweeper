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
        self.size = size
        self.flags_left = mines
        self.minefield = np.zeros(shape=(size, size)).astype(int)
        self.flags = np.zeros(shape=(size, size)).astype(int)
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
                    y_end = min(size, y+2)
                    x_start = max(0, x-1)
                    x_end = min(size, x+2)
                    window = self.minefield[y_start:y_end, x_start:x_end]
                    num_mines = int(np.sum(window))
                    self.board[y][x] = num_mines

    def reveal(self, x, y):
        if self.flags[y][x] == 1:
            return False
        if self.minefield[y][x] == 1:
            return True
        self.reveal_helper(x, y)
        return False

    def reveal_helper(self, x, y):
        if x < 0 or x >= self.size or y < 0 or y >= self.size or self.display[y][x] != 'X':
            return
        self.display[y][x] = f"{self.board[y][x]}"
        if self.board[y][x] == 0:
            for x_dir in range(-1, 2):
                for y_dir in range(-1, 2):
                    self.reveal_helper(x+x_dir, y+y_dir)

    def flag(self, x, y):
        if not self.flags[y][x] and self.display[y][x] == 'X':
            self.flags[y][x] = 1
            self.display[y][x] = 'F'
            self.flags_left -= 1
        else:
            self.flags[y][x] = 0
            self.display[y][x] = 'X'
            self.flags_left += 1

    def did_win(self):
        return np.array_equal(self.minefield, self.flags)

    def get_display(self):
        return self.display

    def get_minefield(self):
        return self.minefield

    def get_flags(self):
        return self.flags

    def get_board(self):
        return self.board

    def get_flags_left(self):
        return self.flags_left


def print_arr(arr):
    for y in range(len(arr)):
        line = f"{y} "
        for x in range(len(arr[0])):
            val = arr[y][x]
            if val == -1:
                val = 'M'
            line += f" {val}"
        print(line)
    line = "\n  "
    for x in range(len(arr[0])):
        line += f" {x}"
    print(line)


def get_move():
    move_line = input("flag(f)/check(c) x_coord y_coord: ")
    args = move_line.split(" ")
    if len(args) != 3:
        return get_move()
    try:
        move_type = args[0]
        move_x = int(args[1])
        move_y = int(args[2])
    except ValueError:
        return get_move()
    return move_type, move_x, move_y


def play_game(difficulty):
    print("generating board...")
    (mines, board_size) = difficulties[difficulty]
    print(f"mines: {mines}, board_size: {board_size}")
    game = Minesweeper(mines, board_size)
    while not game.did_win():
        print(f"FLAGS REMAINING: {game.get_flags_left()}")
        print_arr(game.get_display())
        move_type, move_x, move_y = get_move()
        if move_type == 'f':
            game.flag(move_x, move_y)
        if move_type == 'c':
            did_lose = game.reveal(move_x, move_y)
            if did_lose:
                break
    if game.did_win():
        print("\n###############################")
        print("#           You Win!          #")
        print("###############################")
    else:
        print("\n###############################")
        print("#             OOF             #")
        print("###############################")

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