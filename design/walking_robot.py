from typing import List

""" 
Source: https://leetcode.com/problems/walking-robot-simulation/
Level: LC Medium
"""
dirs = [(0, 1), (-1, 0), (0, -1), (1, 0)] # NWSE

class Solution:
    def robotSim(self, commands: List[int], obstacles: List[List[int]]) -> int:
        self.location = (0, 0)
        self.dir_id = 0
        self.max_dist = 0
        self.obstacles = set([(x, y) for x, y in obstacles])
        self.commands = commands
        self.run()
        return self.max_dist

    def run(self) -> None:
        for command in self.commands:
            self.process(command)

    def process(self, command: int) -> None:
        if command == -2:  # turn left
            self.dir_id = (self.dir_id + 1) % 4
        elif command == -1:  # turn right
            self.dir_id = (self.dir_id - 1 if self.dir_id else 3)
        else:
            self.walk(command)

    def walk(self, steps: int) -> None:
        dx, dy = dirs[self.dir_id]
        x, y = self.location
        hit = 0
        for step in range(1, steps+1):
            loc = (x + step * dx, y + step * dy)
            if loc in self.obstacles:
                hit = 1
                break
        self.location = (loc[0] - hit * dx, loc[1] - hit * dy)
        return self.update_dist()

    def update_dist(self) -> None:
        self.max_dist = max(self.max_dist, self.dist_sq(self.location))

    def dist_sq(self, loc) -> int:
        return loc[0] ** 2 + loc[1] ** 2
