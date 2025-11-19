import math
import random

# Use an external "real" board only for the main game loop; recursive functions use state parameters.
board = [" " for _ in range(9)]  # 3x3 board

def print_board(state):
    print("\n")
    for i in range(3):
        print(" " + " | ".join(state[i*3:(i+1)*3]))
        if i < 2:
            print("---+---+---")
    print("\n")

def is_winner(state, player):
    win_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    return any(all(state[i] == player for i in combo) for combo in win_combinations)

def is_full(state):
    return " " not in state

def actions(state):
    return [i for i in range(9) if state[i] == " "]

def result(state, action, player):
    new_state = state.copy()
    new_state[action] = player
    return new_state

def utility(state):
    if is_winner(state, "O"):
        return +1
    elif is_winner(state, "X"):
        return -1
    else:
        return 0

def terminal_test(state):
    return is_winner(state, "X") or is_winner(state, "O") or is_full(state)

# --- Alpha-Beta Functions ---
def max_value(state, alpha, beta):
    if terminal_test(state):
        return utility(state)
    v = -math.inf
    for a in actions(state):
        v = max(v, min_value(result(state, a, "O"), alpha, beta))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v

def min_value(state, alpha, beta):
    if terminal_test(state):
        return utility(state)
    v = math.inf
    for a in actions(state):
        v = min(v, max_value(result(state, a, "X"), alpha, beta))
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v

def alpha_beta_search(state):
    best_score = -math.inf
    best_action = None
    if not actions(state):
        return None
    for a in actions(state):
        value = min_value(result(state, a, "O"), -math.inf, math.inf)
        if value > best_score:
            best_score = value
            best_action = a
    # Fallback: if something goes wrong, return a random legal move
    if best_action is None:
        legal = actions(state)
        return random.choice(legal) if legal else None
    return best_action

# --- Game Loop ---
def human_move():
    while True:
        try:
            move = int(input("Enter your move (1-9): ")) - 1
        except ValueError:
            print("Please enter a number 1-9.")
            continue
        if move < 0 or move > 8:
            print("Move out of range. Choose 1-9.")
            continue
        if board[move] != " ":
            print("Cell already taken. Try another.")
            continue
        return move

def choose_first():
    while True:
        ans = input("Who goes first? (me/ai) [me]: ").strip().lower()
        if ans == "" or ans.startswith("m"):
            return "me"
        if ans.startswith("a"):
            return "ai"
        print("Type 'me' or 'ai' (or press Enter for me).")

def main():
    global board
    board = [" " for _ in range(9)]
    print("Welcome to Tic-Tac-Toe! You are X, AI is O.")
    first = choose_first()
    print_board(board)

    while True:
        if first == "me":
            # Human turn
            move = human_move()
            board[move] = "X"
            print_board(board)
            if is_winner(board, "X"):
                print("You win!")
                break
            if is_full(board):
                print("It's a draw!")
                break

            # AI turn
            print("AI is thinking...")
            ai_move = alpha_beta_search(board)
            if ai_move is None:
                print("AI could not find a move — it's a draw.")
                break
            board[ai_move] = "O"
            print_board(board)
            if is_winner(board, "O"):
                print("AI wins!")
                break
            if is_full(board):
                print("It's a draw!")
                break

        else:  # AI first
            print("AI is thinking...")
            ai_move = alpha_beta_search(board)
            if ai_move is None:
                print("AI could not find a move — it's a draw.")
                break
            board[ai_move] = "O"
            print_board(board)
            if is_winner(board, "O"):
                print("AI wins!")
                break
            if is_full(board):
                print("It's a draw!")
                break

            # Human turn
            move = human_move()
            board[move] = "X"
            print_board(board)
            if is_winner(board, "X"):
                print("You win!")
                break
            if is_full(board):
                print("It's a draw!")
                break

if __name__ == "__main__":
    main()
