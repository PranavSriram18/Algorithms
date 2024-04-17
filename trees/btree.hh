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
     * Prints keys owned by this node.
    */
    void printNodeKeys() const {
        std::cout << "[";
        for (const auto& key : keys_) {
            std::cout << key << " ";
        }
        std::cout << "] ";
    }

    /**
     * Whether this node or any of its descendants owns the given key.
    */
    bool contains(const K& key) const {
        auto [owns, idx] = ownsKey(key);
        return (
            owns ? true : (isLeaf() ? false : children_[idx].contains(key))
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
    void splitChild(const K& midKey, const V& midValue) {
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

    // Note - it is currently assumed that midKey(), midValue() are
    // only called on full nodes. Any future code changes that violate this 
    // assumption must modify the implementation of these methods accordingly.

    const K& midKey() const {
        return keys_[B/2];
    }

    const V& midValue() const {
        return values_[B/2];
    }

    BTree<K, V, B>* btree_;  // owning BTree
    std::vector<BTreeNode> children_;  // children of this node
    std::vector<K> keys_;  // keys stored in this node. At most B-1
    std::vector<V> values_;  // values stored in this node
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

    /**
     * Prints all the keys in the B-Tree using a level order traversal.
    */
    void printKeys() {
        std::cout << "\n\nPrinting keys: \n\n";
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
            currNode.printNodeKeys();
            for (const auto& child : currNode.children_) {
                q.emplace_back(child, currLevel+1);
            }
        }
        std::cout << "\n\n";
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
    
    BTreeNode<K, V, B> root_;
};  // class BTree
