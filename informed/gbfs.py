import sys
import time, random

class Node:
    def __init__(self, state, parent, action, distance):
        self.state = state
        self.parent = parent
        self.action = action
        self.distance = distance

class Frontier:
    def __init__(self):
        self.frontier = []

    def add(self, node):
        return self.frontier.append(node)
    
    def empty(self):
        return len(self.frontier) == 0
    
    def remove(self):
        if self.empty():
            raise Exception("Frontier is empty")
        else:
            node = min(self.frontier, key=lambda n: n.distance)
            self.frontier.remove(node)
            return node
        
    def contain_state(self, state):
        return any(node.state == state for node in self.frontier)

class Maze:
    def __init__(self, filename):
        try:
            with open(filename) as f:
                content = f.read()
            if content.count("A") != 1:
                raise Exception("Maze should have exactly one starting point")
            
            if content.count("B") != 1:
                raise Exception("Maze should have exactly one goal")
            
            file = content.splitlines()
            self.height = len(file)
            self.width = max(len(row) for row in file)
            self.walls = []
            for i in range(self.height):
                row = []
                for j in range(self.width):
                    try:
                        if file[i][j] == "A":
                            self.start = (i, j)
                            row.append(False)
                        elif file[i][j] == "B":
                            self.goal = (i, j)
                            row.append(False)
                        elif file[i][j] == " ":
                            row.append(False)
                        else:
                            row.append(True)
                    except IndexError:
                        row.append(False)
                self.walls.append(row)
        except FileNotFoundError:
            raise FileNotFoundError("File not Found")
        
        self.solution = None

    def manhattan_distance(self, state):
        x1, y1 = state
        x2, y2 = self.goal
        horizontal_dist = abs(x2 - x1)
        vertical_dist = abs(y2 - y1)
        return horizontal_dist + vertical_dist

    def print(self, explored_nodes=None):
        print("\033[H", end="")
        solution = self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end="", flush=True)
                elif (i, j) == self.start:
                    print("A", end="", flush=True)
                elif (i, j) == self.goal:
                    print("B", end="", flush=True)
                elif explored_nodes and (i, j) in explored_nodes:
                    print("*", end="", flush=True)
                elif solution is not None and (i, j) in solution:
                    print("*", end="", flush=True)
                else:
                    print(" ", end="", flush=True)
            print()

        sys.stdout.flush()

    def neighbor(self, state):
        row, col = state
        candidate = [
            ("up", (row-1, col)),
            ("down", (row+1, col)),
            ("left", (row, col-1)),
            ('right', (row, col+1))
        ]
        random.shuffle(candidate)
        result = []
        for action, (r,c) in candidate:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result

    def solve(self):
        distance = self.manhattan_distance(self.start)
        start = Node(state=self.start, parent=None, action=None, distance=distance)
        frontier = Frontier()
        frontier.add(start)
        self.explored = set()
        self.num_explored = 0

        while True:
            if frontier.empty():
                raise Exception("No solution to the maze")
            
            node = frontier.remove()
            self.explored.add(node.state)
            self.print(self.explored)
            time.sleep(0.1)
            self.num_explored +=1
            if node.state == self.goal:
                action = []
                cells = []
                while node.parent is not None:
                    action.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                action.reverse()
                cells.reverse()
                self.solution = (action, cells)
                self.print()
                print("goal found!")
                print()
                print("path distance: ", len(cells))
                return
            
            for action, state in self.neighbor(node.state):
                distance = self.manhattan_distance(state)
                if state not in self.explored and not frontier.contain_state(state):
                    child = Node(state=state, parent=node, action=action, distance=distance)
                    frontier.add(child)

            

if len(sys.argv) != 2:
    raise Exception("Usage: python greed_algorithm.py maze1.txt")

m = Maze(sys.argv[1])
print("\033c")
m.solve()
print()
print("node explored: ", m.num_explored)