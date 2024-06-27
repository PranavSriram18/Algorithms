"""
Scratch:
* can always align with the left end of a white segment

* given left endpoint of carpet, num white tiles covered is 
f (l + C) - f(l)
where f(i) is number of things covered up till but excl i

To calculate f(i): 
just need f values at each left endpoint of the segments
let g(i) be nearest left segment endpoint to i
f(i) = f(g(i)) + min(i - g(i), T(g(i)))

Store precomputed f values in pfx
Store tile segment lengths in tiles

tile_starts: sorted list of starting points of tiles
tile_lengths: map from tile_start -> length
pfx: tile_start -> prefix sum (0...tile_start-1)
"""
class Solution:
    def maximumWhiteTiles(self, tiles: List[List[int]], carpet_len: int) -> int:
        sort(tiles, key=lambda x: x[0])
        tile_start = [l[0] for l in tiles]
        tile_lengths = [l[1] - l[0] + 1 for l in tiles]
        pfx = [0] + itertools.accumulate(tile_lengths)

        best = 0
        for start_pos, curr_pfx in zip(tile_start, pfx):
            endpoint = start_pos + carpet_len
            value = self.pfx_sum(endpoint+1) - curr_pfx
            best = max(value, best)
        return best

    def pfx_sum(self, pos):
        pass # TODO