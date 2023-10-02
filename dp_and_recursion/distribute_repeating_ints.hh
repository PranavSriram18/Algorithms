class Solution {

/**
Scratch

Have numbers a0, ..., a49
freqs: for each i in 0 to 49, have freqs[i] amount of number ai
Have quantity requests q0, ..., q_{m-1}

freqs: vector of "reserves" we have
Process quantity requests in order; update freqs as we fulfill

State: {remaining unfulfilled requests, freqs}

Problem: high branching factor - each step has up to 50 choices

Suppose we use two heuristics: 
1. Process requests from largest to smallest
2. Use largest available bucket in each step
Can this process get stuck?
--> yea
Say B0 = 70, B1 = 50
q0 = 50, q1 = 40, q3 = 30

Alternate:
Instead of processing queries in order, process buckets in order
B0 selects a query to fulfill; branch from there
Also, can we just restrict to top 10 buckets? --> yea

1. Sort quantities in decreasing order
2. Get top 10 buckets
3. Pop top bucket
    For each query:
        Assign this query to this bucket and recurse

State: vector<bucketSize>, numQueriesFulfilled
Store bucket sizes in a pqueue

TODO - complete
*/
public:
    using BucketState = priority_queue<int>;
    bool canDistribute(vector<int>& nums, vector<int>& quantity) {
        queries_ = quantity;
        m_ = queries.size();
        sort(queries_.begin(), queries_.end(), [](int q1, int q2) {
            return q1 > q2;
        });
        BucketState bucketState = buildBucketState();
        return distribute(bucketState, 0);
    }

private:
    void distribute(BucketState bucketState, int fulfilled) {
        for (int queryId = fulfilled; queryId < m_; ++queryId) {
            query = queries_[queryId];
            // TODO
            
        }

    }
    Buckets buckets_;
    vector<int> queries_;
    int m_;
};
