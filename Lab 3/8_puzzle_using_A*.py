class Node:
    def __init__(self, data, level, fval):
        self.data = data
        self.level = level
        self.fval = fval

    def generate_child(self):
        x, y = self.find(self.data, '_')
        directions = [[x - 1, y], [x + 1, y], [x, y - 1], [x, y + 1]]
        children = []
        for i, j in directions:
            child = self.shuffle(self.data, x, y, i, j)
            if child is not None:
                child_node = Node(child, self.level + 1, 0)
                children.append(child_node)
        return children

    def shuffle(self, puz, x1, y1, x2, y2):
        if 0 <= x2 < len(self.data) and 0 <= y2 < len(self.data):
            temp_puz = self.copy(puz)
            temp_puz[x1][y1], temp_puz[x2][y2] = temp_puz[x2][y2], temp_puz[x1][y1]
            return temp_puz
        return None

    def copy(self, root):
        return [row[:] for row in root]

    def find(self, puz, x):
        for i in range(len(self.data)):
            for j in range(len(self.data)):
                if puz[i][j] == x:
                    return i, j


class Puzzle:
    def __init__(self, size=3):
        self.n = size
        self.open = []
        self.closed = []

    def accept(self):
        puz = []
        for i in range(self.n):
            row = input().split()
            puz.append(row)
        return puz

    def f(self, start, goal):
        return self.h(start.data, goal) + start.level

    def h(self, start, goal):
        mismatch = 0
        for i in range(self.n):
            for j in range(self.n):
                if start[i][j] != goal[i][j] and start[i][j] != '_':
                    mismatch += 1
        return mismatch

    def process(self):
        print("Enter the start state matrix (use _ for blank):")
        start = self.accept()
        print("Enter the goal state matrix (use _ for blank):")
        goal = self.accept()

        start_node = Node(start, 0, 0)
        start_node.fval = self.f(start_node, goal)
        self.open.append(start_node)

        print("\nSolving...\n")
        move = 0
        while True:
            cur = self.open[0]
            print(f"\nMove {move}:")
            for row in cur.data:
                print(' '.join(row))
            if self.h(cur.data, goal) == 0:
                print("\nGoal state reached!")
                break

            for child in cur.generate_child():
                child.fval = self.f(child, goal)
                self.open.append(child)

            self.closed.append(cur)
            del self.open[0]
            self.open.sort(key=lambda x: x.fval)
            move += 1


if __name__ == "__main__":
    Puzzle().process()
