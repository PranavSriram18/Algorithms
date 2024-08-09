
"""
TODO - needs to be debugged
Scratch:
A cell ends up O iff there is a path from it to an edge
visit(cell):
    visit each neighbor
states:
    X -> 1
    O, not yet processed -> 0
    O, in progress -> 2
    O, processed and found border -> -1
    O, processed and didn't find border -> 3
"""

class Solution:
    def solve(self, board: List[List[str]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        self.board = board
        self.m, self.n = len(board), len(board[0])
        self.state = [[int(ch == "X") for ch in row] for row in board]
        for i, j in itertools.product(range(self.m), range(self.n)):
            self.visit(i, j, True)
        for i, j in itertools.product(range(self.m), range(self.n)):
            board[i][j] = "O" if self.state[i][j] == -1 else "X"
    
    def visit(self, i, j, force):
        valid_states = [0, 3] if force else [0]
        # cell is "O" and either unprocessed, or not yet found (if force)
        if self.state[i][j] in valid_states:  
            nbrs = self.neighbors(i, j)
            if len(nbrs) < 4:  # base case - border cell
                self.state[i][j] = -1
            else:
                self.state[i][j] = 2  # in progress
                nb_states = [self.visit(nr, nc, False) for nr, nc in nbrs]
                self.state[i][j] = -1 if -1 in nb_states else 3
        return self.state[i][j]

    def neighbors(self, r, c):
        dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        return list(filter(lambda p: self.in_bounds(p), [(r + dr, c + dc) for dr, dc in dirs]))

    def in_bounds(self, cell):
        r, c = cell
        return 0 <= r < self.m and 0 <= c < self.n