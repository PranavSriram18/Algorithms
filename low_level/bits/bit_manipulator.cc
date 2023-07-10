
#include <cassert> 
#include <iostream>

#include "bit_manipulator.hh"

int main() {
    BitManipulator bitManipulator;
    assert(bitManipulator.rangeBitwiseAnd(5, 7) == 4);
    assert(bitManipulator.rangeBitwiseAnd(0, 0) == 0);
    assert(bitManipulator.rangeBitwiseAnd(1, 2147483647) == 0);
    std::cout << "Success " << std::endl;
    return 0;
}