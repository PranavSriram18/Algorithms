class Solution {
/*
Scratch:
n queries of the form (pos, ch)
Base string s

Each query updates: s[pos] = ch
After each query, need to find length of longest 1-char substring

Q. What if we first consider just binary strings?

000110010 

[000] [11] [00] [1] [0]

(0, 3) ; (5, 2) ; (8, 1)

q = (4, 0)

[000] [1] [000] [1] [0]

(0, 3) ; (4, 3) ; (8, 1)

q = (3, 0)

[0000000] [1] [0]

(0, 7) ; (8, 1)




Case I: query with 0
1. Inside a zero block - no-op
2. Adjacent to neither left nor right block
3. Adjacent to left block only - extend left block
4. Adjacent to right block only - extend right block
5. Adjacent to left and right block - merge left and right blocks

s = 00111100
(0, 2) ; (6, 2)

q = (3, 0)

(0, 2) ; (3, 1) ; (6, 2)

Case II: query with 1
1. Inside a 1-block - no-op
2. Adjacent to neither left nor right block - split a zero block
3. Right edge of a zero block - shrink the zero block's size by 1 
4. Left edge of a zero block - shrink zero block's size by 1 and increment its pos
5. Zero block has size 1 - delete the zero block

s = 110011100
Blocks: (2, 2) ; (7, 2)
q = (3, 1)

110111100
Blocks: (2, 1) ; (7, 2)



*/
public:
    vector<int> longestRepeating(string s, string queryCharacters, vector<int>& queryIndices) {
        k_ = queryIndices.size();
        n_ = s.size();
        queryChars_ = queryCharacters;
        queryIdxs_ = queryIndices;
        vector<int> best(k_);
        for (char ch = 'a'; ch <= 'z'; ++ch) {
            vector<int> currResult = solve(ch);
            for (int i = 0; i < 26; ++i) {
                best[i] = max(best[i], currResult[i]);
            }
        }
        return best;
    }

private:
    vector<int> solve(char ch) {
        vector<int> vec = buildBinaryVec(ch);
        vector<pair<int, int>> queries = buildQueries(ch);
        Blocks blocks(vec);
        vector<int> result;
        result.reserve(k_);
        for (auto& [pos, val] : queries) {
            blocks.query(pos, val);
            result.push_back(blocks.largest());
        } 
        return result;
    }

    // Returns a binary vec whose ith entry is 0 iff s[i] == ch 
    vector<int> buildBinaryVec(char ch) {
        vector<int> vec(n_);
        for (int i = 0; i < k_; ++i) {
            vec[i] = (s_[i] != ch);
        }
    }

    vector<pair<int, int>> buildQueries(char ch) {
        vector<pair<int, int>> queries(k_);
        for (int i = 0; i < k_; ++i) {
            queries[i] = {queryIdxs_[i], (queryChars_[i] != ch)}
        }
        return queries;
    }

    int k_;
    int n_;
    string s_;
    string queryChars_;
    vector<int> queryIdxs_;
};
