#include "waterfall_primes.hh"

#include "../utils/test_utils.hh"

/** 
 * Usage: 
 * > g++ waterfall_primes.cc -o waterfall_primes -std=c++20 -O3
 * > ./waterfall_primes > out.txt
 * 
 * Measure with -O3 as well
 */ 

using milli = std::chrono::duration<double, std::milli>;
using hr_clock = std::chrono::high_resolution_clock;

void testWaterfall() {
    std::cout << "Running test" << std::endl;
    auto start = hr_clock::now();
    std::vector<int> waterfallPrimes = WaterfallPrimes::generate();
    auto end = hr_clock::now();
    milli duration = end - start;
    std::cout << "List of terminal waterfall primes: " << std::endl;
    for (int p : waterfallPrimes) {
        std::cout << p << ", ";
    }
    std::cout << "\nDuration: " << duration.count() << " ms" << std::endl;
}

int main() {
    testWaterfall();
    return 0;
}
