#pragma once

template<typename K, typename V>
class BTreeNode {
public:
    BTreeNode(int b) : b_(b), isLeaf_(true) {
        keys_.reserve(b_-1);
        values_.reserve(b_-1);
    }

    // Number of elements in this node
    int numElements() const {
        return kvPairs_.size();
    }

    void insert(const K& key, const V& value) {
        // Case 0: node is empty
        if (numElements() == 0) {
            keys_.push_back(key);
            values_.push_back(value);
        }

        bool isFull = keys_.size() == b_-1;
        auto it = std::lower_bound(keys_.begin(), keys_.end(), key);
        
        // ith key k_i is first that is >= key
        int i = it - keys_.begin();

        // Case 1: node contains this key already; overwrite value
        if (it != keys_.end() && *it == key) {
            values_[i] = value;
            return;
        }

        // At this point have k_{i-1} < key < k_i
        
        if (isLeaf_) {
            if(!isFull) {
                // Case 2: node is leaf, not full
                // Insert the key at position i
                keys_.insert(keys_.begin() + i, key);
                values_.insert(values_.begin() + i, value);
                return;
            } else {
                // Case 3: node is leaf and full
                // TODO - finish this
                keys_.insert(keys_.begin()+i, key);
                values_.insert(values_.begin()+i, value);
                int midIdx = b_ / 2;

                BTreeNode leftChild(b_);
                BTreeNode rightChild(b_);
                leftChild.keys_ = {keys_.begin(), keys_.begin() + midIdx};
                leftChild.values_ = {values_.begin(), values_.begin() + midIdx};
                K midKey = keys_[midIdx];
                V midVal = values_[midIdx];
                rightChild.keys_ = {keys_.begin() + midIdx + 1, keys_.end()};
                rightChild.values_ = {values_.begin() + midIdx + 1, values_.end()};

                return;
            }
        }

        // Case 4: non-leaf; delegate to appropriate child
        // Suppose m children (m <= b). Order of children and keys is
        // (C0, k0, C1, k1, ..., C_{i-1}, k_{i-1}, C_i, k_i, C_{i+1}..., C_{m-2}, k_{m-2}, C_{m-1})
        // k_{i-1} < key < k_i so C_i is the child to insert in
        auto child = children_[i];
        child->insert(key, value);
        // TODO - handle child splitting
    }

private:
    int b_;  // branching factor
    vector<std::shared_ptr<BTreeNode>> children_;
    vector<K> keys_;  // keys stored in this node. At most b_-1
    vector<V> values_;  // values stored in this node
    bool isLeaf_;

};  // class BTreeNode
