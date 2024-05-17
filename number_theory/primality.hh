#pragma once

namespace primality {
/**
 * Basic primality test, with O(sqrt(n)) complexity.
 * Depending on your use case, using a Sieve of Eratosthenes (defined in 
 * prime_sieve.hh) may be more efficient.
 */ 
bool isPrime(int n) {
    if (n <= 1) return false;
    for (int i = 2; i * i <= n; ++i) {
        if (n % i == 0) return false;
    }
    return true;
}

}  // namespace primality