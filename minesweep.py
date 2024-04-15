import random
import re

# play the game

class Board():
    def __init__(self, dim_size, num_bombs):
        #save the data because we need them later
        self.dim_size = dim_size
        self.num_bombs = num_bombs
        self.board = self.make_new_board()
        self.assign_values_board()


        self.dug = set() # a set of tuple holding (row, col) every time it is a valid position

    def make_new_board(self):
        #lets make a 2d board since we dealing with rows and cols
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]

        #plant bombs
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size ** 2 - 1)
            row = loc // self.dim_size # we want to select a row
            col = loc % self.dim_size # we want to select an index in that row

            if board[row][col] == '*':
                #this means there's already a bomb in that location
                continue
            board[row][col] = '*'
            bombs_planted += 1
        return board

    def assign_values_board(self):
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == "*":
                    continue
                self.board[r][c] = self.get_num_neigh_bombs(r, c)

    def get_num_neigh_bombs(self, row, col):
        neigh_bombs = 0
        for r in range(max(0, row-1), min(self.dim_size-1, (row+1) + 1)):
            for c in range(max(0, col-1), min(self.dim_size-1, (col+1) + 1)):
                if r == row and c == col:
                    continue
                if self.board[r][c] == "*":
                    neigh_bombs += 1
        return neigh_bombs

    def dig(self, row, col):
        #dig at location
        #return True if successful dig else bomb dig

        #few scenarios
        #hit a bomb -> game over
        #dig at location with neighboring bombs -> finish dig
        #dig and if not neighboring bombs then dig neighbors -> recurse dig neighbors
        self.dug.add((row, col)) #keep tracks where we dug

        if self.board[row][col] == "*":
            return False
        elif self.board[row][col] > 0:
            return True
        # Self.board[row][col] == 0
        for r in range(max(0, row-1), min(self.dim_size-1, (row+1) + 1)):
            for c in range(max(0, col-1), min(self.dim_size-1, (col+1) + 1)):
                if (r, c) in self.dug:
                    continue #avoid multi digging in the same place

                self.dig(r, c)
        return True

    def __str__(self):
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = " "

        string_rep = ''
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key = len)
                )
            )

        # print the csv strings
        indices = [i for i in range(self.dim_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'

        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep


def play(dim_size=10, num_bombs=10):
    # Step 1: create the board and plant the bombs
    board = Board(dim_size, num_bombs)

    # Step 2: show the user the board and ask for where they want to dig
    # Step 3a: if location is a bomb, show game over message
    # Step 3b: if location is not a bomb, dig recursively until each square is at least
    #          next to a bomb
    # Step 4: repeat steps 2 and 3a/b until there are no more places to dig -> VICTORY!
    safe = True

    while len(board.dug) < board.dim_size ** 2 - num_bombs:
        print(board)
        # 0,0 or 0, 0 or 0,    0
        user_input = re.split(',(\\s)*', input("Where would you like to dig? Input as row,col: "))  # '0, 3'
        row, col = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= board.dim_size or col < 0 or col >= dim_size:
            print("Invalid location. Try again.")
            continue

        # if it's valid, we dig
        safe = board.dig(row, col)
        if not safe:
            # dug a bomb ahhhhhhh
            break # (game over rip)

    # 2 ways to end loop, lets check which one
    if safe:
        print("CONGRATULATIONS!!!! YOU ARE VICTORIOUS!")
    else:
        print("SORRY GAME OVER :(")
        # let's reveal the whole board!
        board.dug = [(r,c) for r in range(board.dim_size) for c in range(board.dim_size)]
        print(board)

if __name__ == "__main__":
    play()