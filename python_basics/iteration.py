from collections import Counter 
from itertools import islice
class Solution:
    def top_k_frequent(self, iterable, k):
        freqs = Counter()
        chunk_sz = 1000
        while 1:
            chunk = list(islice(iterable, chunk_sz))
            if not chunk:
                break
            freqs.update(Counter(chunk))
        return freqs.most_common(k)
        
