#include "max_segment_sum.hh"

#include <cassert>
#include <iostream>

/** 
 * Usage: 
 * > g++ max_segment_sum_test.cc -o max_segment_sum_test -std=c++17
 * > ./max_segment_sum_test
 */ 

void testBasic() {
    MaxSegmentSum solver;
    std::vector<int> nums {1,2,5,6,1};
    std::vector<int> queries {0,3,2,4,1};
    std::vector<long long> expected {14,7,2,2,0};
    std::vector<long long> output = solver.maximumSegmentSum(nums, queries);
    for (auto val : output) {
        std::cout << val << " ";
    }
    std::cout << "\n";
    
    assert(output == expected);
}

int main() {
    testBasic();
    return 0;
}