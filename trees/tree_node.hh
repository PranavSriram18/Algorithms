#pragma once

template<typename T>
class TreeNode {
public:
    explicit TreeNode(
        const T& val, const std::vector<TreeNode*>& children
    ) : val_(val), children_(children) {}

    const T& value() const {
        return val_;
    }

    const std::vector<TreeNode*>& children() const {
        return children_;
    }

    size_t numChildren() const {
        return children_.size();
    }

    void addChild(const TreeNode& child) {
        children_.push_back(child);
    }

private:
    T val_;
    std::vector<TreeNode*> children_;
};  // class TreeNode
