#pragma once

template<typename T>
class BSTreeNode {
public:
    explicit BSTreeNode(
        const T& val, 
        BSTreeNode* left = nullptr,
        BSTreeNode* right = nullptr
    ) : val_(val), left_(left), right_(right) {
        assert(left_->value() <= val_ && val_ <= right_->value());
    }

    const T& value() {
        return val_; 
    }

    BSTreeNode* left() {
        return left_;
    }

    BSTreeNode* right() {
        return right_;
    }

    // Find the smallest node in the subtree rooted at this node
    BSTreeNode* smallest() {
        TreeNode* node = this;
        while (node->left() != nullptr) {
            node = node->left();
        }
        return node;
    }

    // Find the first greater ancestor of this node in the BST rooted at root
    BSTreeNode* firstGreaterAncestor(BSTreeNode* root) {
        TreeNode* node = root;
        T target = val_;
        std::vector<TreeNode*> path;
        while (node != this) {
            path.emplace(node);
        }
    }

private:
    T val_;
    BSTreeNode* left_;
    BSTreeNode* right_;


};  // class BSTreeNode
