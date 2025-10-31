from copy import deepcopy

class Puzzle:
    def __init__(self, board, goal):
        self.board = board
        self.goal = goal
        self.size = 3

    def find_blank(self, state):
        for i in range(self.size):
            for j in range(self.size):
                if state[i][j] == 0:
                    return i, j

    def is_goal(self, state):
        return state == self.goal

    def get_moves(self, state):
        x, y = self.find_blank(state)
        moves = []
        directions = [(-1,0),(1,0),(0,-1),(0,1)]
        for dx, dy in directions:
            nx, ny = x+dx, y+dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                new_state = deepcopy(state)
                new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
                moves.append(new_state)
        return moves

    def dls(self, state, depth, path, visited):
        if self.is_goal(state):
            return path + [state]
        if depth == 0:
            return None
        visited.append(state)
        for move in self.get_moves(state):
            if move not in visited:
                new_path = self.dls(move, depth - 1, path + [state], visited)
                if new_path:
                    return new_path
        return None

    def iddfs(self, start):
        depth = 0
        while True:
            visited = []
            result = self.dls(start, depth, [], visited)
            if result:
                return result
            depth += 1


def input_state(prompt):
    print(prompt)
    state = []
    for _ in range(3):
        row = list(map(int, input().split()))
        state.append(row)
    return state


start = input_state("Enter the initial state row-wise (use 0 for blank):")
goal = input_state("Enter the goal state row-wise (use 0 for blank):")

puzzle = Puzzle(start, goal)
path = puzzle.iddfs(start)

print("\nTotal moves:", len(path)-1)
for step, state in enumerate(path):
    print(f"\nMove {step}:")
    for row in state:
        print(*row)
