#include "interval_counter.hh"

#include "../utils/test_utils.hh"

/** 
 * Usage: 
 * > g++ interval_counter_test.cc -o interval_counter_test -std=c++17
 * > ./interval_counter_test
 */ 

void testBasic() {
    IntervalCounter ic;
    ic.add(2, 3);
    ic.add(7, 10);
    std::cout << "Count: " << ic.count() << std::endl;
    ic.add(5, 8);
    std::cout << "Count: " << ic.count() << std::endl;
}

void test2() {
    IntervalCounter ic;
    // Cover the range [100, 199] in a convoluted way
    ic.add(100, 153);
    ic.add(130, 174);
    ic.add(188, 191);
    ic.add(121, 199);
    std::cout << "Count: " << ic.count() << std::endl;
    assert(ic.count() == 100);
}

int main() {
    testBasic();
    test2();
    return 0;
}