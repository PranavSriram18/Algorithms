
from collections import defaultdict
from sortedcontainers import SortedSet # type: ignore
from typing import List

"""
Problem Description: https://leetcode.com/problems/design-a-food-rating-system/
Level: LC Medium

Basic idea: use a table of cuisine -> SortedSet. Used a scalar key function
instead of tuple comparison because I was originally trying to hack around not
having a SortedSet in the standard library by using a Counter 
(with most_common), but that was too slow.

"""
class FoodRatings:

    def __init__(self, foods: List[str], cuisines: List[str], ratings: List[int]):
        self.N = (1 << 16)
        init_set = lambda: SortedSet([], self.global_score)
        self.table = defaultdict(init_set)
        self.f2i = {f:i for i, f in enumerate(sorted(foods))}  # food ->f index
        self.f2c = {f:c for f, c in zip(foods, cuisines)}  # food -> cuisine
        self.f2r = {f:r for f, r in zip(foods, ratings)}  # food -> rating

        for food, cuisine in zip(foods, cuisines):
            self.table[cuisine].add(food)
        
    def changeRating(self, food: str, newRating: int) -> None:
        ss = self.table[self.f2c[food]]
        ss.discard(food)
        self.f2r[food] = newRating
        ss.add(food)

    def highestRated(self, cuisine: str) -> str:
        return self.table[cuisine][-1]

    def global_score(self, food) -> int:
        return (self.f2r[food] << 16) + (self.N - 1 - self.f2i[food])