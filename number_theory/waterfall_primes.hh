#pragma once

#include "primality.hh"

#include <queue>
#include <vector>

/**
 * This code is inspired by a tweet (link below) that points out that 73939133
 * is the largest prime with the following curious property: repeatedly removing
 * the last digit until only one remains produces a sequence of numbers that are
 * all themselves prime. That is, each number in the following list is prime:
 * 73939133
 * 7393913
 * 739391
 * 73939
 * 7393
 * 739
 * 73
 * 7
 * 
 * I'll call such a number a "waterfall prime". Note that each number in the
 * sequence above is a waterfall prime; we will be interested in the largest
 * number in this sequence, which we'll call a terminal waterfall prime. 
*/

class WaterfallPrimes {
public:
    static std::vector<int> generate() {
        std::queue<int> q;
        std::vector<int> singleDigitPrimes {2, 3, 5, 7};
        std::vector<int> lastDigits {1, 3, 7, 9};
        std::vector<int> result;

        for (int d : singleDigitPrimes) {
            q.push(d);
        }

        while (q.size()) {
            int num = q.front();
            q.pop();
            bool terminal = true;
            for (int d : lastDigits) {
                int newNum = num * 10 + d;
                if (primality::isPrime(newNum)) {
                    q.push(newNum);
                    terminal = false;
                }
            }
            if (terminal) {
                result.push_back(num);
            }
        }
        return result;
    }

};  // class WaterfallPrimes
