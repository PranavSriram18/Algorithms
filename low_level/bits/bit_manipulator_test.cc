
#include <cassert> 
#include <iostream>

#include "bit_manipulator.hh"

void testRangeBitwiseAnd() {
    BitManipulator bitManipulator;
    assert(bitManipulator.rangeBitwiseAnd(5, 7) == 4);
    assert(bitManipulator.rangeBitwiseAnd(0, 0) == 0);
    assert(bitManipulator.rangeBitwiseAnd(1, 2147483647) == 0);
    std::cout << "RangeBitwiseAnd successful " << std::endl;
}

void testGreatXOR() {
    BitManipulator bitManipulator;
    long x = 100;
    assert(bitManipulator.theGreatXor(x) == 27);
    std::cout << "GreatXOR successful " << std::endl;
}

int main() {
    testRangeBitwiseAnd();
    testGreatXOR();
    return 0;
}