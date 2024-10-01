import random

"""
This code is based on a problem posed by Daniel Litt (@littmath) on X.
Below is an adapted version of the problem.

Flip 100 coins, labeled 0 through 99. Alice checks the coins in order 
(0, 1, 2, 3, …) while Bob checks the even-labeled coins, then the odd-labeled 
ones (so 0, 2, 4, ..., 98, 1, 3, 5, ..., 99). Who is more likely to see two 
heads (not necessarily consecutive) *first*?

Our implementation generalizes the game to n coins, with t heads required to 
win, and with coins landing on heads with probability p.
"""
class CoinGame:
    def __init__(
            self, 
            num_coins: int = 100, 
            target: int = 2, 
            head_prob: float = 0.5
        ):
        self.n = num_coins
        self.t = target
        self.p = head_prob

    def flip(self):
        # Returns a 1 (Heads) with probability self.p
        return int(random.random() <= self.p)

    def play(self) -> int:
        """
        Play a single game.
        Returns 1 if Alice wins, 0 if tied, -1 if Bob wins.
        """
        a_score, b_score = 0, 0
        a_idxs = list(range(self.n))
        b_idxs = list(range(0, self.n, 2)) + list(range(1, self.n, 2))
        coins = [self.flip() for _ in range(self.n)]  # 0 is tails, 1 is heads
        for a_id, b_id in zip(a_idxs, b_idxs):
            a_score += coins[a_id]
            b_score += coins[b_id]
            if max(a_score, b_score) == self.t:
                return 1 if b_score < self.t else (-1 if a_score < self.t else 0)
        return 0
    
    def run_monte_carlo(self, n_iters: int):
        res = [0, 0, 0]
        for i in range(n_iters):
            res[1 - self.play()] += 1
        print(f"Alice: {res[0]} \n Ties: {res[1]} \n Bob: {res[2]}")

    
if __name__=="__main__":
    game = CoinGame(100, 2, 0.5)
    game.run_monte_carlo(100000)
    game = CoinGame(100, 26, 0.5)
    game.run_monte_carlo(100000)
            





    