#include "dining_philosophers.hh"

#include "../utils/test_utils.hh"

/** 
 * Usage: 
 * > g++ dining_philosophers_test.cc -o dining_philosophers_test -std=c++20
 * > ./dining_philosophers_test
 */ 

void testBasic() {
    DiningPhilosophers diningPhilosophers(5, 2);
    diningPhilosophers.run();
    std::cout << "Success" << std::endl;
}

int main() {
    testBasic();
    return 0;
}
