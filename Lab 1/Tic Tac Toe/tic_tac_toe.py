import math

class TicTacToe:
    def __init__(self):
        self.board = []

    def create_board(self):
        self.board = [['-' for _ in range(3)] for _ in range(3)]

    def fix_spot(self, position, player):
        row = position // 3
        col = position % 3
        self.board[row][col] = player

    def is_spot_empty(self, position):
        row = position // 3
        col = position % 3
        return self.board[row][col] == '-'

    def is_player_win(self, player):
        n = len(self.board)

        # Check rows and columns
        for i in range(n):
            if all(self.board[i][j] == player for j in range(n)) or \
               all(self.board[j][i] == player for j in range(n)):
                return True

        # Check diagonals
        if all(self.board[i][i] == player for i in range(n)) or \
           all(self.board[i][n - 1 - i] == player for i in range(n)):
            return True

        return False

    def is_board_filled(self):
        for row in self.board:
            for item in row:
                if item == '-':
                    return False
        return True

    def show_board(self):
        print("\nCurrent Board:")
        for row in self.board:
            print(" ".join(row))
        print()

    def show_positions(self):
        print("\nPosition Map:")
        positions = [str(i) for i in range(9)]
        for i in range(0, 9, 3):
            print(" ".join(positions[i:i + 3]))
        print()

    def evaluate(self):
        if self.is_player_win('O'):
            return 1
        elif self.is_player_win('X'):
            return -1
        else:
            return 0

    def minimax(self, depth, is_maximizing):
        score = self.evaluate()

        # Base conditions
        if score == 1:
            return score
        if score == -1:
            return score
        if self.is_board_filled():
            return 0

        if is_maximizing:
            best = -math.inf
            for i in range(9):
                if self.is_spot_empty(i):
                    self.fix_spot(i, 'O')
                    best = max(best, self.minimax(depth + 1, False))
                    self.fix_spot(i, '-')  # Undo move
            return best
        else:
            best = math.inf
            for i in range(9):
                if self.is_spot_empty(i):
                    self.fix_spot(i, 'X')
                    best = min(best, self.minimax(depth + 1, True))
                    self.fix_spot(i, '-')  # Undo move
            return best

    def find_best_move(self):
        best_val = -math.inf
        best_move = -1

        for i in range(9):
            if self.is_spot_empty(i):
                self.fix_spot(i, 'O')
                move_val = self.minimax(0, False)
                self.fix_spot(i, '-')
                if move_val > best_val:
                    best_move = i
                    best_val = move_val

        return best_move

    def start(self):
        self.create_board()
        player = 'X'
        computer = 'O'

        print("Welcome to Tic Tac Toe!")
        print("You are 'X' and the computer is 'O'.")
        self.show_positions()

        while True:
            self.show_board()
            try:
                position = int(input("Enter position (0–8): "))
            except ValueError:
                print("Invalid input! Enter a number between 0 and 8.")
                continue

            if position < 0 or position > 8:
                print("Invalid position! Enter between 0 and 8.")
                continue

            if not self.is_spot_empty(position):
                print("That spot is already taken! Choose another.")
                continue

            self.fix_spot(position, player)

            if self.is_player_win(player):
                self.show_board()
                print("You win!")
                break

            if self.is_board_filled():
                self.show_board()
                print("It's a draw!")
                break

            print("Computer is making its move...")
            best_move = self.find_best_move()
            self.fix_spot(best_move, computer)
            print(f"Computer chose position {best_move}")

            if self.is_player_win(computer):
                self.show_board()
                print("Computer wins!")
                break

            if self.is_board_filled():
                self.show_board()
                print("It's a draw!")
                break


# Start the game
tic_tac_toe = TicTacToe()
tic_tac_toe.start()
