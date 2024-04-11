#include "segment_tree.hh"

#include <iostream>

int main() {
    std::vector<int> data {3, 1, 0, 7, 9};
    std::function<int(int, int)> addFn = [](int x, int y) -> int { return x + y; };
    SegmentTree<int> stree_(data, addFn);
    int partialSum = stree_.query(0, 3);  // expect 11
    std::cout << "sum(data[0...3]) = " << partialSum << std::endl;

    stree_.update(2, 5);
    partialSum = stree_.query(0, 3);  // expect 16
    std::cout << "sum(data[0...3]) = " << partialSum << std::endl;

    return 0;
}
