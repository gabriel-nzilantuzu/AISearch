import time
import sys
import random

class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def empty(self):
        return len(self.frontier) == 0
    
    def remove(self):
        if self.empty():
            raise Exception("Empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node
    
    def contain_state(self, state):
        return any(node.state == state for node in self.frontier)

class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("Empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node
    
class Maze():
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
            self.width = max(len(line) for line in file)

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
            raise Exception("File not found")
        self.solution = None

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
        candidates = [
            ("up", (row-1, col)),
            ("down", (row+1, col)),
            ("right", (row, col+1)),
            ("left", (row, col-1))
        ]
        random.shuffle(candidates)
        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))

        return result
    
    def solve(self):
        start = Node(state=self.start, parent=None, action=None)
        self.explored = set()
        self.num_explored = 0
        frontier = QueueFrontier()
        frontier.add(start)

        explored_nodes = set()

        while True:
            if frontier.empty():
                raise Exception("Maze has no solution")
            
            node = frontier.remove()
            self.explored.add(node.state)
            explored_nodes.add(node.state)
            
            self.print(explored_nodes)
            
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
            
            time.sleep(0.01)
            self.num_explored +=1
            
            for action, state in self.neighbor(node.state):
                if state not in self.explored and not frontier.contain_state(state):
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)

if len(sys.argv) !=  2:
    raise Exception("Usage: python maze.py maze.txt")

m = Maze(sys.argv[1])
print("\033c")
m.solve()
print()
print("node explored: ", m.num_explored)