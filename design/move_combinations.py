import itertools
import math
from typing import List

# TODO - needs to be debugged 

class Solution:
    def countCombinations(self, pieces: List[str], positions: List[List[int]]) -> int:
        self.pieces = pieces
        self.positions = [[r-1, c-1] for r, c in positions]
        self.n = len(pieces)
        return self.run()
    
    def run(self): 
        # piece -> List of dests
        all_dests = [self.get_dests(piece, pos) for piece, pos in zip(
            self.pieces, self.positions
        )]

        # pieces x path idx x time x coord
        all_paths = [
            [self.get_path(pos, dest) for dest in all_dests[i]] for i, piece, pos in zip(
                range(self.n), self.pieces, self.positions)
        ]

        return len(self.filter_paths(all_paths, self.n))

    def filter_paths(self, all_paths: List[List[List[int]]], k):
        """
        Returns a list of joint paths for the first k pieces.
        A joint path is a list of the form 
        [[loc_0_0, loc_0_1, loc2, ..., loc_0_k], [loc_10, loc_11, loc_12, ..., loc_1k],
        ...] where each entry is the list of locations at that timestep.
        Indexing of result is hence: path_idx x timestamp x piece x coord
        Indexing of all_paths is: pieces x path_idx x time x coord
        """
        if k == 1:
            path0 = all_paths[0]  # path_idx x time x coord 
            print(f"path0: {path0}")
            res = []
            for path in path0: 
                curr_row = []
                for loc in path:
                    curr_row.append([loc])
                res.append(curr_row)
            return res
        
        # path_idx x time x piece x coord
        prev_paths = self.filter_paths(all_paths, k-1)
        new_paths = [self.merge(prev_path, curr_path) for 
                     prev_path, curr_path in itertools.product(prev_paths, all_paths[k-1])]
        new_paths = [p[0] for p in new_paths if p[1]]
        return new_paths
    
    def merge(self, prev_path: List[List[List[int]]], curr_path: List[List[int]]):
        """ 
        prev_path is indexed by timestamp then piece
        curr_path is indexed by timestamp
        """
        print(f"prev path: {prev_path}")
        print(f"curr path: {curr_path}")
        result = []
        valid = True
        for location_list, new_location in zip(prev_path, curr_path):
            if new_location not in location_list:
                new_location_list = location_list + [new_location]
                result.append(new_location_list)
            else:
                print(f"Conflict: {new_location} already in location list")
                valid = False
                break
        return result, valid
    
    def get_path(self, pos, dest) -> List[List[int]]:
        row0, col0 = pos
        row1, col1 = dest
        dr = -1 if row0 > row1 else (1 if row0 < row1 else 0)
        dc = -1 if col0 > col1 else (1 if col0 < col1 else 0)
        steps = max(abs(row0 - row1), abs(col0 - col1))
        path = [[row0 + i * dr, col0 + i * dc] for i in range(0,steps+1)]
        path += path[-1] * (7 - len(path))
        return path

    def get_dests(self, piece: str, pos: List[int]) -> List[List[int]]:
        row, col = pos
        return [[rr, cc] for rr, cc in itertools.product(
            range(8), range(8)
        ) if self.movable(piece, row, col, rr, cc)]
        
    def movable(self, piece, row0, col0, row1, col1) -> bool:
        if piece == "rook":
            return row0 == row1 or col0 == col1
        elif piece == "bishop":
            return (row0 + col0 == row1 + col1) or (row0 - col0 == row1 - col1)
        else:
            return self.movable("rook", row0, col0, row1, col1) or self.movable(
                "bishop", row0, col0, row1, col1)
    