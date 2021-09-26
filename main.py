import random


class Board:
    def __init__(self, dim_size, num_bombs):
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        self.board = self.make_new_board()
        self.assign_values_to_board()

        self.dug = set()
        self.flagged = set()

    def make_new_board(self):
        board = [[' ' for _ in range(self.dim_size)] for _ in range(self.dim_size)]

        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size ** 2 - 1)
            row = loc // self.dim_size
            col = loc % self.dim_size

            if board[row][col] == '*':
                continue

            board[row][col] = '*'
            bombs_planted += 1

        return board

    def assign_values_to_board(self):
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':
                    continue
                self.board[r][c] = self.get_num_neighboring_bombs(r, c)

    def get_num_neighboring_bombs(self, row, col):
        num_neighboring_bombs = 0
        for r in range(max(0, row - 1), min(self.dim_size - 1, row + 1) + 1):
            for c in range(max(0, col - 1), min(self.dim_size - 1, col + 1) + 1):
                if r == row and c == col:
                    continue
                if self.board[r][c] == '*':
                    num_neighboring_bombs += 1

        return num_neighboring_bombs

    def dig(self, row, col):
        self.dug.add((row, col))

        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True

        for r in range(max(0, row - 1), min(self.dim_size - 1, row + 1) + 1):
            for c in range(max(0, col - 1), min(self.dim_size - 1, col + 1) + 1):
                if (r, c) in self.dug or (r, c) in self.flagged:
                    continue
                self.dig(r, c)

        return True

    def flag(self, row, col):
        self.flagged.add((row, col))

    def __str__(self):
        visible_board = []
        dms = self.dim_size - 1
        dim_digits = 0
        while dms > 0:
            dim_digits += 1
            dms //= 10

        for i in range(self.dim_size * 2):
            tech_row = []
            for j in range(self.dim_size * 2):
                tech_row.append(' ')
            visible_board.append(tech_row)

        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row, col) in self.dug:
                    visible_board[row * 2][col * 2] = str(self.board[row][col])
                elif (row, col) in self.flagged:
                    visible_board[row * 2][col * 2] = 'F'
                else:
                    visible_board[row * 2][col * 2] = '-'

        string_rep = 'x'
        string_rep += ' ' * dim_digits
        for i in range(self.dim_size):
            string_rep += str(i)
            string_rep += ' '
        string_rep += '\n'

        for c in range(0, self.dim_size * 2):
            for r in range(0, self.dim_size * 2):
                if r == 0 and c % 2 == 1:
                    string_rep += str(c // 2)
                    string_rep += ' ' * (dim_digits - c // 10 - 1)
                string_rep += visible_board[r - 1][c - 1]
            string_rep += '\n'

        return string_rep

    def save_game(self):
        f = open("game.txt", "w")
        board_str = ''
        for i in range(dim_size):
            board_str = ''
            for j in range(dim_size):
                board_str += str(self.board[i][j])
            board_str += '\n'
            f.write(board_str)
        f.close()


def play(dim_size, num_bombs):
    board = Board(dim_size, num_bombs)

    safe = True

    while len(board.dug) < board.dim_size ** 2 - num_bombs:
        print(board)
        print("Where to dig? Input column, row and action (open or flag):\n")
        user_input_x = int(input())
        user_input_y = int(input())
        user_input_action = input()
        row, col = user_input_x, user_input_y
        if row < 0 or row >= board.dim_size or col < 0 or col >= board.dim_size:
            print("Invalid location")
            continue

        if user_input_action == "open":
            safe = board.dig(row, col)
            if not safe:
                break
        elif user_input_action == "flag":
            board.flag(user_input_x, user_input_y)

    if safe:
        print("WIN")
        board.save_game()
    else:
        print("LOSS")
        board.dug = [(r, c) for r in range(board.dim_size) for c in range(board.dim_size)]
        print(board)
        board.save_game()

    pass


print("Enter board's dimension and number of bombs:\n")
dim_size = int(input())
num_bombs = int(input())
if num_bombs >= dim_size ** 2:
    print("Incorrect input\n")
else:
    play(dim_size, num_bombs)
