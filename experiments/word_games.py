
class WordFinder:
    def __init__(self, filepath: str):
        """
        Read all words from the provided file into a single list of words.
        """
        self.words = []
        with open(filepath, 'r') as file:
            for line in file:
                for word in line.split():
                    self.words.append(word)
        
    def single_inversion(self, word) -> bool:
        """
        Returns True if all chars in word are distinct, and the word contains
        exactly one inversion wrt lexicographic character ordering.
        """
        k = len(word)
        if len(list(set(word))) != k:
            return False
        # this is O(k^2) but k is small
        inversions = 0
        for i in range(k):
            for j in range(i+1, k):
                inversions += (ord(word[i]) > ord(word[j]))
        return inversions == 1

    def longest_satisfying_constraint(self):
        single_inv = list(filter(lambda w: self.single_inversion(w), self.words))
        best = max(single_inv, key=len)
        all_best = [w for w in single_inv if len(w) == len(best)]
        runners_up = [w for w in single_inv if len(w) == len(best) - 1]
        return all_best, runners_up
    
if __name__ == "__main__":
    word_finder = WordFinder("words.txt")
    best, runers_up = word_finder.longest_satisfying_constraint()
    print(f"Best: {best}")
    print(f"Runners up: {runers_up}")
