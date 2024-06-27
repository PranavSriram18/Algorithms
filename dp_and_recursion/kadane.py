
"""
Implements Kadane's algorithm for maximum subarray sum.
"""
class Kadane:
    def max_subarray(self, numbers):
        best_sum = float('-inf')
        curr_sum = 0
        for val in numbers:
            curr_sum = max(curr_sum + val, 0)
            best_sum = max(best_sum, curr_sum)
        return best_sum
    
if __name__=="__main__":
    numbers = [-2, 11, -2, 3, -5, 7, -13, 2]
    kadane = Kadane()
    print(kadane.max_subarray(numbers))
    