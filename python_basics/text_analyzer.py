from collections import Counter, defaultdict
import string

""" 
Create a class TextAnalyzer with a method analyze that takes a filename as input. The method should:

Read the file and process its content.
Return a dictionary where:

Keys are words (case-insensitive, alphanumeric only)
Values are dictionaries containing:
a. 'count': number of occurrences
b. 'lines': set of line numbers where the word appears
c. 'neighbors': dictionary of words that appear next to this word and their counts

Sort the main dictionary by word frequency (descending), then alphabetically.
"""
class TextAnalyzer():
    def analyze(self, filename: str):
        init_value = lambda: {"count": 0, "lines": set(), "neighbors": Counter()}
        # result: word -> {"count": <count> , "lines": <line_set>, "neighbors": {word -> count}}
        result = defaultdict(init_value)
        with open(filename, "r") as f:
            lines = f.readlines()

        prev_word = None
        for line_number, orig_line in enumerate(lines):
            line = [word.lower() for word in orig_line.split(" ") if word.isalnum()]
            for i, word in enumerate(line):
                word = word.rstrip(string.punctuation)
                result[word]["count"] += 1
                result[word]["lines"].add(line_number)
                if prev_word:
                    result[word]["neighbors"][prev_word] += 1
                    result[prev_word]["neighbors"][word] += 1
                prev_word = word
        return dict(sorted(result.items(), key=lambda kv: (-kv[1]["count"], kv[0])))
