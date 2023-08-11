#include <chrono>
#include <iostream>
#include <cmath>

#include "prime_sieve.hh"

int main() {
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

    return 0;
}