from typing import List

class Solution:
    class Transaction:
        def __init__(self, s: str):
            lst = s.split(',')
            self.name = lst[0]
            self.time = int(lst[1])
            self.amount = int(lst[2])
            self.city = lst[3]
            self.str = s


    def invalid_transactions(self, transactions: List[str]) -> List[str]:
        self.transactions = [self.Transaction(t) for t in transactions]
        invalid_transactions = [t.str for t in self.transactions if self.is_invalid(t)]
        return invalid_transactions

    def is_invalid(self, t: 'Solution.Transaction'):
        if t.amount > 1000:
            return True 
        for u in self.transactions:
            if (abs(t.time - u.time) <= 60 and t.name == u.name and t.city != u.city):
                 return True
        return False
    
if __name__=='__main__':
    sol = Solution()
    print(sol.invalid_transactions(["Alice,20,800,MTV", "Alice,50,1200,MTV"]))