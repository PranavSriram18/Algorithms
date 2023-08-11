#pragma once

#include <vector>

/**
 * This class implements the Sieve of Eratosthenes.
 * Total time complexity for construction is O(n log log n).
*/
class PrimeSieve {
public:
    PrimeSieve(int n) : n_(n) {
        populateIsPrime();
        populateNumPrimes();
    }

    bool isPrime(int p) {
        if (p < 0 || p > n_) throw std::invalid_argument("Out of range");
        return isPrime_[p];
    }
    
    int numPrimesAtMost(int k) {
        return numPrimes_[k];
    }
    
private:
    // O(n log log n)
    void populateIsPrime() {
        isPrime_.resize(n_+1, true);
        isPrime_[0] = false;
        isPrime_[1] = false;
        for (int i = 2; i <= n_; ++i) {
            if (!isPrime_[i]) continue;
            // Mark all multiples of this prime as not prime
            for (int j = 2 * i; j <= n_; j += i) {
                isPrime_[j] = false;
            }
        }
    }
    
    // O(n)
    void populateNumPrimes() {
        numPrimes_.resize(n_+1);
        for (int i = 1; i <= n_; ++i) {
            numPrimes_[i] = isPrime_[i] + numPrimes_[i-1];
        }
    }
    
    int n_;
    
    // ith entry is number of primes in [0, i]
    std::vector<int> numPrimes_;
    
    std::vector<bool> isPrime_;
};  // class PrimeSieve
