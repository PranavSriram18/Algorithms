#include <chrono>
#include <iostream>
#include <cmath>

#include "prime_sieve.hh"

/**
 * Usage:
 * g++ prime_sieve_test.cc -o prime_sieve_test -std=c++20 -O3
 * ./prime_sieve_test
*/

void test0() {
    auto start = std::chrono::high_resolution_clock::now();
    PrimeSieve sieve(1e8);
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(
        end - start).count();

    std::cout << "Constructed PrimeSieve in " << duration << " milliseconds" << std::endl;

    std::vector<int> nums {
        17, 30, 47, 551, 9081, 109733, 2359005, 40792201};
    for (int p : nums) {
        std::cout << p << " is " << (
            sieve.isPrime(p) ? "prime" : "composite") << std::endl;
    }
    for (int k = 0; k <= 8; ++k) {
        int val = pow(10, k);
        std::cout << "Num primes under " << val << ": " << sieve.numPrimesAtMost(
            val) << std::endl;
    }
}

void testLarge() {
    auto start = std::chrono::high_resolution_clock::now();
    PrimeSieve sieve(1e9);
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(
        end - start).count();
    std::cout << "Constructed PrimeSieve in " << duration << " milliseconds" << std::endl;
}

int main() {
    // test0();
    testLarge();
    return 0;
}