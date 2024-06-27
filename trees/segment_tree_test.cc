#include "segment_tree.hh"

#include <cassert>
#include <iostream>

/** 
 * Usage: 
 * > g++ segment_tree_test.cc -o segment_tree_test -std=c++20
 * > ./segment_tree_test
 */ 

void testBasic() {
    std::vector<int> data {3, 1, 0, 7, 9};
    std::function<int(int, int)> addFn = [](int x, int y) -> int { return x + y; };
    SegmentTree<int> stree_(data, addFn);
    int partialSum = stree_.query(0, 3);  // expect 11
    std::cout << "sum(data[0...3]) = " << partialSum << std::endl;
    assert(partialSum == 11);

    stree_.update(2, 5);
    // data is now {3, 1, 5, 7, 9}
    partialSum = stree_.query(0, 3);  // expect 16
    std::cout << "sum(data[0...3]) = " << partialSum << std::endl;
    assert(partialSum == 16);

    stree_.update(4, 14);
    stree_.update(0, 6);
    stree_.update(0, 7);
    // data is now {7, 1, 5, 7, 14}
    partialSum = stree_.query(0, 4);  // expect 34
    std::cout << "sum(data[0...4]) = " << partialSum << std::endl;
    assert(partialSum == 34);
    std::cout << "testBasic() passes " << std::endl;
}

int main() {
    testBasic();
    return 0;
}
