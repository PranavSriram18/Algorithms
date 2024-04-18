#pragma once

#include <deque>
#include <iostream>
#include <optional>
#include <tuple>
#include <vector>

/**
 * The classes BTreeNode and BTree together implement a B-Tree.
 * 
 * Invariants:
 * Operations all maintain the following invariants.
 * 1. New keys are always inserted into leaf nodes 
 * 2. All non-leaf nodes satisfy numChildren() == numKeys()+1
 * 3. 0 <= numKeys() < B, EXCEPT during certain intermediate stages where
 *    numKeys() is temporarily B. A node containing B keys is called full.
 * 4. numKeys() == B will trigger a split. The splitting of a node is owned by
 *    the parent of the node. 
 * 5. For non-leaves, numKeys() == B can only occur due to a promotion of a
 *    child key. This in turn implies numChildren() == B+1 at this point.
 * 
 * Ownership model:
 * Parents own their children. Each node is owned by its parent. The root is the
 * exception; the root is owned by the owning BTree. All nodes contain a pointer
 * to the owning BTree.
*/

template<typename K, typename V, int B>
class BTree;  // Forward declaration of BTree

template<typename K, typename V, int B>
class BTreeNode {
public:
    friend class BTree<K, V, B>;

    BTreeNode() = default; 

    bool isLeaf() const {
        return children_.empty();
    }

    /**
     * Prints keys or values owned by this node.
     * \param printKeys prints keys if true otherwise values
     * \param includeTombstones includes keys/values in tombstones
     * TODO - support includeTombstones
    */
    void print(bool printKeys, bool includeTombstones) const {
        std::cout << "[";
        for (int i = 0; i < keys_.size(); ++i) {
            bool tombstone = !values_[i].has_value();
            if (!tombstone) {
                if (printKeys) {
                    std::cout << keys_[i] << " ";
                } else {
                    std::cout << values_[i].value() << " ";
                }
            } else {
                std::cout << "* ";
            }
        }
        std::cout << "] ";
    }

    /**
     * Whether this node or any of its descendants owns the given key.
    */
    bool contains(const K& key) const {
        auto [owns, idx] = ownsKey(key);
        return (
            owns ? values_[idx].has_value() : (isLeaf() ? false : children_[idx].contains(key))
        );
    }

    /**
     * Returns the value associated with the given key, or an empty optional if
     * the key is not present.
    */
    std::optional<V> value(const K& key) const {
        auto [owns, idx] = ownsKey(key);
        if (owns) return values_[idx];
        return (isLeaf() ? std::optional<V>() : children_[idx].value(key));
    }

    void insert(const K& key, const V& value) {
        auto [owns, idx] = ownsKey(key);
        if (owns) {
            // Case 1: node owns this key already; overwrite value
            values_[idx] = value;
        } else if (!isLeaf()) {
            // Case 2: non-leaf; delegate to appropriate child
            children_[idx].insert(key, value);
        } else {
            // Now we are in a leaf node. Insert the key at position vIdx
            // Case 3: all done; Case 4: split the node
            keys_.insert(keys_.begin() + idx, key);
            values_.insert(values_.begin() + idx, value);
            splitSelfIfNeeded();
        }
    }

    /**
     * We want deletion from a node to be managed by the parent of the node.
     * To achieve this, while searching for the key we keep track of:
     * parent - the parent of this node, i.e. the node that dispatched this call
     * prevIdx - the index of this node in parent's children_
     * There are 3 cases: own key, dispatch to a child, or not found (do nothing)
     * We also need to handle the case of deleting from the root separately
    */
    void deleteKey(const K& key, BTreeNode<K, V, B>* parent, int prevIdx) {
        auto [owns, currIdx] = ownsKey(key);
        if (owns) {
            return (parent ? parent->deleteFromChild(
                prevIdx, currIdx) : btree_->deleteFromRoot(currIdx));
        }
        if (!isLeaf()) return children_[currIdx].deleteKey(key, this, currIdx);
    }

protected:
    /**
     * Core subroutine used by several methods.
     * Usage: auto [owns, idx] = ownsKey(key);
     * owns indicates whether the given key is in this node's keys_.
     * idx is position in keys_ where this key *would* go. This is the current
     * position of key if owns is true, or the position where it should go if
     * inserted in keys_.
     * For non-leaves, note that idx is also the index of the child whose range
     * includes the key. To see this, suppose m children (0 < m <= b). 
     * Order of children and keys is
     * (C0, k0, C1, k1, ..., C_{i-1}, k_{i-1}, C_i, k_i, C_{i+1}..., C_{m-2}, k_{m-2}, C_{m-1})
     * If idx = i, then k_{i-1} < key < k_i, so C_i is the child whose range includes key.
    */
    std::pair<bool, int> ownsKey(const K& key) const {
        auto it = std::lower_bound(keys_.begin(), keys_.end(), key);
        int i = it - keys_.begin();
        bool owns = (it != keys_.end() && *it == key);
        return {owns, i};
    }

    // Constructor
    BTreeNode(BTree<K, V, B>* btree) : btree_(btree) {
        keys_.reserve(B-1);
        values_.reserve(B-1);
    }

    /**
     * Splits *this if *this is full. Node splitting operations are managed by
     * parents in our implementation, so this request is dispatched to the
     * parent of this node, or btree_ if this node is the root.
    */
    void splitSelfIfNeeded() {
        if (keys_.size() < B) return;
        BTreeNode* parent = btree_->parent(midKey());
        return parent ? parent->splitChild(
            midKey(), midValue()) : btree_->splitRoot();
    }

    /**
     * Splits the child node containing the given key, and promotes the key.
     * \pre The caller is a full child of *this and contains midKey. 
    */
    void splitChild(const K& midKey, const std::optional<V>& midValue) {
        // Promote the key, split child node, split self if needed
        auto [_, idx] = ownsKey(midKey);
        keys_.insert(keys_.begin() + idx, midKey);
        values_.insert(values_.begin() + idx, midValue);
        splitChildNode(idx);
        splitSelfIfNeeded();
    }

    /**
     * Splits the ith child node. 
     * Inserts a new child node at i+1 and partitions the original child's
     * keys, values, and childrens between the original and new child.
    */
    void splitChildNode(int i) {
        // Identify the left (original) child and instantiate the rightChild
        BTreeNode node(btree_);
        children_.insert(children_.begin() + i + 1, node);
        auto& leftChild = children_[i];
        auto& rightChild = children_[i+1];

        // Partition the keys and values
        int midIdx = B/2;
        rightChild.keys_ = {leftChild.keys_.begin() + midIdx + 1, leftChild.keys_.end()};
        rightChild.values_ = {leftChild.values_.begin() + midIdx + 1, leftChild.values_.end()};
        leftChild.keys_.resize(midIdx);
        leftChild.values_.resize(midIdx);

        // Partition children. If non-leaf is splitting, it has B+1 children
        // Left gets [0, midIdx], right gets [midIdx+1, B]
        if (!leftChild.isLeaf()) {
            rightChild.children_ = {
                leftChild.children_.begin() + midIdx + 1, 
                leftChild.children_.end()
            };
            leftChild.children_.resize(midIdx+1);
        }
    }

    void deleteFromChild(int childIdx, int keyIdx) {
        return children_[childIdx].isLeaf() ? deleteFromLeafChild(
            childIdx, keyIdx) : deleteFromInternalChild(childIdx, keyIdx);
    }

    /**
     * Deletes a key from a child that is a leaf.
     * \param childIdx the index of the child node in children_
     * \param keyIdx the index of the key in the child's keys_
     * The main challenge with deleting from a leaf is maintaining the invariant
     * that the node continues to have at least kMinKeys keys.
    */
    void deleteFromLeafChild(int childIdx, int keyIdx) {
        auto& child = children_[childIdx];
        if (child.keys_.size() > kMinKeys) {
            child.keys_.erase(child.keys_.begin() + keyIdx);
            child.values_.erase(child.values_.begin() + keyIdx);
            return;
        }
        if (attemptKeyBorrowing(childIdx, keyIdx)) return;
        if (keys_.size() > kMinKeys) return mergeChildWithSibling(childIdx, keyIdx);
        
        // Parent has insufficient keys for merging; use Tombstone
        auto& value = child.values_[keyIdx];
        btree_->tombstones_ += value.has_value();
        value = std::optional<V>();
    }

    bool attemptKeyBorrowing(int childIdx, int keyIdx) {
        // try borrowing a key from left sibling
        auto& child = children_[childIdx];
        if (childIdx) {
            auto& leftSibling = children_[childIdx-1];
            if (leftSibling.keys_.size() > kMinKeys) {
                child.keys_.erase(child.keys_.begin() + keyIdx);  // child key deletion
                child.values_.erase(child.values_.begin() + keyIdx);
                child.keys_.insert(child.keys_.begin(), keys_[childIdx-1]);  // parent->child
                child.values_.insert(child.values_.begin(), values_[childIdx-1]);
                keys_[childIdx-1] = leftSibling.keys_.back();  // leftSib->parent
                values_[childIdx-1] = leftSibling.values_.back();
                leftSibling.keys_.pop_back();  // leftSib deletion
                leftSibling.values_.pop_back();
                return true;
            }
        }

        // try borrowing a key from right sibling
        // note the differences in indexing compared to left sibling case
        if (childIdx+1 < children_.size()) {
            auto& rightSibling = children_[childIdx+1];
            if (rightSibling.keys_.size() > kMinKeys) {
                child.keys_.erase(child.keys_.begin() + keyIdx);  // child key deletion
                child.values_.erase(child.values_.begin() + keyIdx);
                child.keys_.insert(child.keys_.end(), keys_[childIdx]);  // parent->child
                child.values_.insert(child.values_.end(), values_[childIdx]);
                keys_[childIdx] = rightSibling.keys_[0];  // rightSib->parent
                values_[childIdx] = rightSibling.values_[0];
                rightSibling.keys_.erase(rightSibling.keys_.begin()); // rightSib deletion
                rightSibling.values_.erase(rightSibling.values_.begin());
                return true;
            }
        }
        return false;
    }

    void mergeChildWithSibling(int childIdx, int keyIdx) {
        auto& child = children_[childIdx];
        if (childIdx) {
            //std::cout << "Merging w left sibling " << std::endl;
            auto& leftSibling = children_[childIdx-1];
            // parent -> left
            leftSibling.keys_.push_back(keys_[childIdx-1]);
            leftSibling.values_.push_back(values_[childIdx-1]);

            // parent key removal
            keys_.erase(keys_.begin() + childIdx-1);
            values_.erase(values_.begin() + childIdx-1);

            // child key removal
            child.keys_.erase(child.keys_.begin() + keyIdx);
            child.values_.erase(child.values_.begin() + keyIdx);

            // transfer child contents -> left
            for (int i = 0; i < child.keys_.size(); ++i) {
                leftSibling.keys_.push_back(child.keys_[i]);
                leftSibling.values_.push_back(child.values_[i]);
            }

            // delete the child
            children_.erase(children_.begin() + childIdx);
            return;
        }

        // merge w right node
        // std::cout << "Merging w right sibling " << std::endl;
        auto& rightSibling = children_[childIdx+1];
        
        // child key removal
        child.keys_.erase(child.keys_.begin() + keyIdx);
        child.values_.erase(child.values_.begin() + keyIdx);

        // transfer child contents -> right
        std::vector<K> mergedKeys = child.keys_;
        std::vector<std::optional<V>> mergedValues = child.values_;
        mergedKeys.reserve(B-1);
        mergedValues.reserve(B-1);

        // parent -> right
        mergedKeys.push_back(keys_[childIdx]);
        mergedValues.push_back(values_[childIdx]);

        // parent key removal
        keys_.erase(keys_.begin() + childIdx);
        values_.erase(values_.begin() + childIdx);

        for (int i = 0; i < rightSibling.keys_.size(); ++i) {
            mergedKeys.push_back(rightSibling.keys_[i]);
            mergedValues.push_back(rightSibling.values_[i]);
        }
        rightSibling.keys_ = mergedKeys;
        rightSibling.values_ = mergedValues;

        // delete the child
        children_.erase(children_.begin() + childIdx);
    }

    void deleteFromInternalChild(int childIdx, int keyIdx) {
        // tombstone
        auto& value = children_[childIdx].values_[keyIdx];
        btree_->tombstones_ += value.has_value();
        value = std::optional<V>();
    }

    // Note - it is currently assumed that midKey(), midValue() are
    // only called on full nodes. Any future code changes that violate this 
    // assumption must modify the implementation of these methods accordingly.

    const K& midKey() const {
        return keys_[B/2];
    }

    const std::optional<V>& midValue() const {
        return values_[B/2];
    }

    static constexpr int kMinKeys = (B+1)/2 - 1;

    BTree<K, V, B>* btree_;  // owning BTree
    std::vector<BTreeNode> children_;  // children of this node
    std::vector<K> keys_;  // keys stored in this node. At most B-1
    std::vector<std::optional<V>> values_;  // values stored in this node
};  // class BTreeNode

/**
 * Manages the root of the B-Tree. This is the class clients use.
*/
template<typename K, typename V, int B>
class BTree {
public:
    friend class BTreeNode<K, V, B>;

    BTree() : root_(this) {}

    bool contains(const K& key) const {
        return root_.contains(key);
    }

    std::optional<V> value(const K& key) const {
        return root_.value(key);
    }

    void insert(const K& key, const V& value) {
        root_.insert(key, value);
    }

    void deleteKey(const K& key) {
        root_.deleteKey(key, nullptr, -1);
    }

    // Get the parent of the node containing the given key
    // This pointer is invalidated by any modification to the tree
    BTreeNode<K, V, B>* parent(const K& key) {
        BTreeNode<K, V, B> *p = nullptr, *c = &root_;
        while (true) {
            auto [owns, idx] = c->ownsKey(key);
            if (owns) return p;
            if (c->isLeaf()) return nullptr;
            p = c;
            c = &c->children_[idx];
        }
    }

    // Debugging & performance analysis utilities

    /**
     * Prints all the keys in the B-Tree using a level order traversal.
    */
    void printKeys(bool includeTombstones=false) {
        printLevelOrder(true, includeTombstones);
    }
    
    void printValues(bool includeTombstones=true) {
        printLevelOrder(false, includeTombstones);
    }

    int tombstones() const {
        return tombstones_;
    }

protected:
    void splitRoot() {
        // The root has requested to be split, so we first create a new root to 
        // replace the old root, and then forward the request to the new root
        BTreeNode<K, V, B> temp = root_;
        root_ = BTreeNode<K, V, B>(this);
        root_.children_.push_back(temp);
        auto& oldRoot = root_.children_[0];
        return root_.splitChild(oldRoot.midKey(), oldRoot.midValue());
    }

    void deleteFromRoot(int keyIdx) {
        // tombstone
        auto& value = root_.values_[keyIdx];
        tombstones_ += value.has_value();
        value = std::optional<V>();
    }

    void printLevelOrder(bool printKeys, bool includeTombstones) {
        std::string s = (printKeys ? "keys" : "values");
        std::cout << "\n\nPrinting " << s << " (level-order): \n\n";
        std::deque<std::pair<BTreeNode<K, V, B>, int>> q;
        int currLevel = 0;
        q.emplace_back(root_, currLevel);
        while(q.size()) {
            auto [currNode, newLevel] = q.front();
            q.pop_front();
            if (newLevel > currLevel) {
                std::cout << "\n";
                currLevel = newLevel;
            }
            currNode.print(printKeys, includeTombstones);
            for (const auto& child : currNode.children_) {
                q.emplace_back(child, currLevel+1);
            }
        }
        std::cout << "\n\n";
    }
    
    BTreeNode<K, V, B> root_;
    int tombstones_ = 0;
};  // class BTree
