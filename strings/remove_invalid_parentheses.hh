/*
Problem Statement:
Given a string s that contains parentheses and letters, remove the minimum number of invalid parentheses to make the input string valid.

Return a list of unique strings that are valid with the minimum number of removals. You may return the answer in any order.
Problem description: https://leetcode.com/problems/remove-invalid-parentheses/
Level: Leetcode Hard

Scratch:
For now, ignore non-paren chars

()() --> valid

())( --> not valid

((())) --> valid

(()))( --> not valid

+1 for every opening
-1 for every closing

Validity criteria:
(i) At each point, running count is >= 0
(ii) At end, running count is 0

Q. How to find min deletions?

If score at some point is -k, with k > 0, need at least k deletions of
closing braces

For a string s, let:
n = len(s)
f(s, k) = running score after reading k chars
g(s) = max(0, - min_{k} f(s, k)) 

g(s) is lower bound on result
g(s) is min number of closing braces that need deletion

Now suppose we have deleted g(s) closing braces
disc(s) = f(s, n) + g(s) is new discrepancy

s = )))((()
g(s) = 3
disc(s) = 2

CCCOOCCOO
g(s) = 3
disc(s) = 2

CCCOOCCOO
-1 -2 -3 -2 -1 -2 -3 -2 -1

XXXOOCCOO
0 0 0 1 2 1 0 1 2

Changing C --> X at position j: add 1 to score[j], ..., score[n-1]
Changing O --> X at position j: sub 1 from score[j], ..., score[n-1]

End goal:
all scores nonnegative
end score is 0

Recursion idea:
Walk through string
First convert C's to X's
Then convert O's to X's

State to keep track of:
--> Current string
--> Score vector
--> Deletions left in current phase

Start with initial string
Run phase 1, to produce a vector of strings
For each of these, run phase 2


Search based idea:
Given string s, identify set of possible successors
If g(s) > 0:
    then only going to consider deletion of appropriate C's
    Let i be first index where s[i] < 0
    Only consider deleting C's at or before i
Otherwise, only going to consider deletion of O's
    Let j be position of last 0 in scores\
    Only consider O's after position j

)a))(())

1R 1a 2R 2L 2R
RaRRLLRR

RRR -> {XRR, RXR, RRX} 
RRR -> {XRR}

)())) --> {())}

((()())))(...)

*/
class Solution {

public:
    static constexpr char kOpenCh = '(';
    static constexpr char kCloseCh = ')';

    vector<string> removeInvalidParentheses(string s) {
        vector<string> vec = solve(s);
        unordered_set<string> uset{vec.begin(), vec.end()};
        vector<string> dedup {uset.begin(), uset.end()};
        return dedup;
    }

private:

    vector<string> solve(string& s) {
        vector<string> result;
        queue<string> q;
        q.push(s);

        while(q.size()) {
            string currStr = q.front();
            q.pop();
            process(currStr, q, result);
        }
        return result;
    }

    void process(
        string& currStr, queue<string>& q, vector<string>& result
    ) {
        int currSz = currStr.size();
        if (currSz == 0) {
            result.push_back(currStr);
            return;
        }
        vector<int> currScores = computeScores(currStr);
        auto [closedDel, openDel] = minDelete(currScores);
        if (closedDel) {
            int j = firstNegScoreIdx(currScores);
            for (int i = 0; i <= j; ++i) {
                if (currStr[i] != kCloseCh) continue;
                // only produce 1 successor state per block 
                if (i && currStr[i-1] == kCloseCh) continue;
                // build copy without ith char
                string succ = currStr;
                succ.erase(i, 1);
                q.push(succ);
            }
            return;
        }

        if (openDel) {
            int j = lastZeroScoreIdx(currScores);
            for (int i = j+1; i < currSz; ++i) {
                if (currStr[i] != kOpenCh) continue;
                if (i && currStr[i-1] == kOpenCh) continue;
                // build copy without ith char
                string succ = currStr;
                succ.erase(i, 1);
                q.push(succ);
            }
            return;
        }

        // currStr is valid if control reaches here
        result.push_back(currStr);
    }

    // This function assumes a negative score exists
    int firstNegScoreIdx(vector<int>& currScores) {
        int n = currScores.size();
        for (int i = 0; i < n; ++i) {
            if (currScores[i] < 0) return i;
        }
        return -1;  // control should not reach here
    }

    int lastZeroScoreIdx(vector<int>& currScores) {
        int n = currScores.size();
        for (int i = n-1; i >= 0; --i) {
            if (currScores[i] == 0) return i;
        }
        return -1;  // control should not reach here
    }

    // (num closed, num open) to delete
    pair<int, int> minDelete(vector<int>& currScores) {
        int gs = g(currScores);
        int disc = currScores.back() + gs;
        return {gs, disc};
    }

    vector<int> computeScores(string& currStr) {
        int sz = currStr.size();
        vector<int> scores(sz);
        auto charScore = [](char ch) {
            return ((ch == kOpenCh) ? 1 : ((ch == kCloseCh) ? -1 : 0));
        };
        scores[0] = charScore(currStr[0]);
        for (int i = 1; i < sz; ++i) {
            scores[i] = scores[i-1] + charScore(currStr[i]);
        }
        return scores;
    }

    int g(const vector<int>& currScores) {
        return max(0, -*min_element(currScores.begin(), currScores.end()));
    }

    int n_;  // length of s
};
