from typing import List, Dict
from collections import Counter, defaultdict
import heapq
import string

class Solution:
    """
    Given a list of integers, return a dictionary where the keys are the unique
    integers in the list, and the values are the number of times each integer appears.
    """
    def get_counts(self, x: List[int]) -> Dict[int, int]:
        return dict(sorted(Counter(x).items(), key=lambda kv: -kv[1]))
    

    def process_words(self, s: str) -> Dict[str, List]:
        vowels = set('aeiouAEIOU')
        num_vowels = lambda s: sum(1 for ch in s if ch in vowels)
        word_dict = {word : [len(word), num_vowels(word), word] for word in s.split(" ")}
        return dict(sorted(word_dict.items(), key=lambda kv: (-len(kv[0]), kv[0].lower())))
    
    def dna_process(self, seqs: List[str]) -> Dict:
        flips = {"A": "T", "C": "G", "G": "C", "T": "A"}
        gc_content = lambda s: 100.0 * (sum(ch in "CG" for ch in s) / len(s))
        complement = lambda s: "".join([flips[ch] for ch in s])
        table = {s : [len(s), gc_content(s), complement] for s in seqs}
        return dict(sorted(table.items(), key=lambda kv: -kv[1][1]))
    
    def analyze_sales_data(self, sales_data) -> Dict:
        """ 
        Sales data is:
        region -> store -> {product -> number}
        """
        regional_stats = dict()
        global_top_product, global_top_product_v = None, 0
        global_top_store, global_top_store_v = None, 0

        def build_regional_stats(region, store_data) -> Dict:
            """ 
            Process a single region.
            Store data is {store -> {product -> number}}
            """
            nonlocal global_top_product, global_top_product_v
            nonlocal global_top_store, global_top_store_v
            total_sales = 0
            product_totals = Counter()
            store_totals = Counter()
            for store, product_data in store_data.items():
                for product, number in product_data.items():
                    total_sales += number
                    product_totals[product] += number
                    store_totals[store] += number
            top_product, top_product_v = product_totals.most_common(1)[0]
            sorted_stores = sorted(store_data.keys(), key=lambda s: -store_totals[s])
            top_store, top_store_v = sorted_stores[0], store_totals[sorted_stores[0]]
            result = dict()
            result['total_sales'] = total_sales
            result['top_product'] = top_product
            result['store_ranking'] = sorted_stores

            if top_store_v > global_top_store_v:
                global_top_store, global_top_store_v = region + "_" + top_store, top_store_v
            
            if top_product_v > global_top_product_v:
                global_top_product, global_top_product_v = top_product, top_product_v
            return result
        
        regional_stats = {region : build_regional_stats(
            region, store_data) for region, store_data in sales_data.items()}
        
        result = dict()
        result['regional_stats'] = regional_stats
        result['top_product'] = global_top_product
        result['top_store'] = global_top_store
        return result
    
    def filtered_top_k_frequency(numbers, k, filter_func):
        """
        The function should:
        Filter the list using the given filter function
        Find the k most frequent elements in the filtered list
        If there's a tie for the kth position, include all tied elements
        Return the result as a list of tuples (number, frequency), 
        sorted by frequency in descending order, with ties broken by the number in ascending order
        """
        numbers = filter(filter_func, numbers)
        elem_to_freq = Counter(numbers).items()

        # sort by freq descending, elem ascending
        result = heapq.nsmallest(k, elem_to_freq, key=lambda x: (-x[1], x[0]))

        # get everything tied with result[-1] that didn't make it to result
        last_elem, last_freq = result[-1]

        tied_entries = [(e, f) for e, f in elem_to_freq if f == last_freq and e > last_elem]
        tied_entries.sort()  # sort ascending by elem; all freqs equal
        return result + tied_entries
    
    def sliding_window_max(self, nums, w, k):
        """ 
        Given an array nums, determine the maximum sum of a window of length w
        that contains exactly k unique elements.
        """
        LARGE_NEG = -1000000000
        left, right = 0, w - 1
        c = Counter(nums[:right+1])
        running_sum = sum(nums[:right+1])
        best = LARGE_NEG if len(c) != k else running_sum

        while right+1 < len(nums):
            last_num, new_num = nums[left], nums[right+1]
            c[last_num] -= 1
            if not c[last_num]:
                c.pop(last_num)
            c[new_num] += 1
            running_sum += (new_num - last_num)
            if len(c) == k:
                best = max(best, running_sum)
            left, right = left+1, right+1
        return best if best != LARGE_NEG else -1
    

    def longest_no_repeats(self, s: str, k: int) -> int:
        """ 
        Given a string s, find the longest substring of s that contains no two
        adjacent repeated chars, and contains exactly k unique chars.
        """
        # we know no two adjacent equal chars in s can be part of the solution,
        # so split s by inserting dividers
        divided_s = [s[0]]
        for i in range(1, len(s)):
            if s[i] == s[i-1]:
                divided_s.append(" ")
            divided_s.append(s[i])
        # list of chars -> string -> list of strings
        strings = "".join(divided_s).split(" ")
        return max(self.longest_k_unique(ss, k) for ss in strings)
    
    def longest_k_unique(self, s: str, k: int) -> int:
        """
        Returns the length of the longest substring of s with exactly k 
        unique chars.
        """
        n = len(s)
        c = Counter()
        left, right, best = 0, 0, 0
        
        # outer loop invariant: we have "just landed" on right
        while right < len(s):
            c[s[right]] += 1

            while len(c) > k:
                c[s[left]] -= 1
                if not c[s[left]]:
                    c.pop(s[left])
                left += 1

            if len(c) == k:
                best = max(best, right - left + 1)
            right += 1
                
        return best
