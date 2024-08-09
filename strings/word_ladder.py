from collections import deque
import string
from typing import List

class Solution:
    START_TOKEN = "<START_TOKEN>"
    
    def generate_word_ladder(
            self, words: List[str], start_word: str, end_word: str) -> List[str]:
        self.words = set(words)
        self.build_graph(words)
        return self.run_bfs(start_word, end_word)

    def build_graph(self, words: List[str]):
        # O(N * L * 26), where L is length of each word
        self.graph = {word : self.generate_neighbors(word) for word in words}
    
    def generate_neighbors(self, word: str) -> List[str]:
        return [
            word[:i] + c + word[i+1:]
            for i in range(len(word))
            for c in string.ascii_lowercase
            if c != word[i] and (word[:i] + c + word[i+1:]) in self.words
        ]
    
    def run_bfs(self, start_word: str, end_word: str) -> List[str]:
        q = deque([start_word])
        prev_node_table = {start_word : Solution.START_TOKEN}
        while q:
            curr_word = q.popleft()
            for neighbor in self.graph[curr_word]:
                if neighbor == end_word:
                    return self.unwind(neighbor, prev_node_table)
                if neighbor not in prev_node_table:
                    q.append(neighbor)
                    prev_node_table[neighbor] = curr_word
        return []  # not found
    
    def unwind(self, end_word, prev_node_table) -> List[str]:
        result = []
        curr_word = end_word
        while curr_word != Solution.START_TOKEN:
            result.append(curr_word)
            curr_word = prev_node_table[curr_word]
        result.reverse()
        return result
