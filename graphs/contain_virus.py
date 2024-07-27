from typing import List, Tuple

from union_find.union_find import UnionFind

"""
Scratch:
1. Identify connected components
2. Build wallls around largest connected component
3. Run spreading forward step
4. Repeat

Wall representation:
identify each wall with the cell directly to its left or above it
m x n grid, 2 entries per cell (horizontal wall and vertical wall)

1. wall b/w (i, j) and (i+1, j) is walls[i][j][0] (vertical)
2. wall b/w (i, j) and (i, j+1) is walls[i][j][1] (horizontal)

Three key pieces of state: 
walls, grid cells, UnionFind
self.uf tracks connected components of infected cells
# TODO: Complete connected components part
"""

class Solution:
    def contain_virus(self, is_infected: List[List[int]]) -> int:
        self.grid = is_infected
        self.m = len(self.grid)  # m rows
        self.n = len(self.grid[0])  # n cols
        self.uf = UnionFind(self.m * self.n)
        self.walls = [[(0, 0) for col in range(self.n)] for row in range(self.m)]
        self.num_walls = 0
        newly_infected = self.init_connections()
        self.run(newly_infected)
        return self.num_walls

    def run(self, newly_infected: int):
        while newly_infected:
            ccs = self.uf.connected_components()
            ccs.sort(key=lambda cc: -len(cc))
            self.build_walls([self.id_to_cell(x) for x in ccs[0]])
            newly_infected = self.propagate_virus()
    
    def init_connections(self):
        """Add edges between initially infected neighbors."""
        infected = 0
        for r in range(self.m):
            for c in range(self.n):
                if self.grid[r][c]:
                    infected += 1
                    for nr, nc in filter(
                        lambda n: self.grid[n[0]][n[1]], self.neighbors(r, c)):
                        self.uf.add_edge(self.cell_id(r, c), self.cell_id(nr, nc))
        return infected

    def build_walls(self, cc: List[Tuple[int, int]]):
        """
        For each cell in the connected component, build walls between it and its
        neighbors that are not in the cc.
        """
        for r, c in cc:
            for nr, nc in filter(lambda n: n not in cc, self.neighbors(r, c)):
                wr, wc, wz = self.wall_id(r, c, nr, nc)
                self.num_walls += self.walls[wr][wc][wz] != 1
                self.walls[wr][wc][wz] = 1

    def propagate_virus(self) -> int:
        """ 
        Run one step of virus propagation.
        Each infected cell infects its neighbors, unless there is a wall 
        between them.
        """
        buffer = []
        def spread(r, c):
            if self.grid[r][c]:
                for nr, nc in filter(
                    lambda n: not self.grid[n[0]][n[1]], self.neighbors(r, c)):
                    wr, wc, wz = self.get_wall_id(r, c, nr, nc)
                    if not self.walls[wr][wc][wz]:
                        buffer.append((r, c, nr, nc))
                       
        for row in range(self.m):
            for col in range(self.n):
                spread(row, col)
        for r, c, nr, nc in buffer:
            self.grid[nr][nc] = 1
            self.add_edge(r, c, nr, nc)
        return len(buffer)

    def neighbors(self, r: int, c: int) -> List[Tuple[int, int]]:
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        return list(filter(self.in_bounds, [(r+d[0], c+d[1]) for d in dirs]))

    def in_bounds(self, p: Tuple[int, int]) -> bool:
        return 0 <= p[0] <= self.m - 1 and 0 <= p[1] <= self.n - 1
    
    def wall_id(self, r: int, c: int, nr: int, nc: int) -> Tuple[int, int, int]:
        """Assumes (r, c) and (nr, nc) are valid neighbors."""
        return min(r, nr), c, 0 if r != nr else r, min(c, nc), 1
    
    def add_edge(self, r: int, c: int, nr: int, nc: int):
        self.uf.add_edge(self.cell_id(r, c), self.cell_id(nr, nc))

    def cell_id(self, r: int, c: int):
        return r * self.n + c
    
    def id_to_cell(self, id: int) -> Tuple[int, int]:
        return id / self.n, id % self.n
