#include "stream.hh"
#include "../utils/test_utils.hh"

/** 
 * Usage: 
 * > g++ stream_test.cc -o stream_test -std=c++20 -O3
 * > ./stream_test > out.txt
 * 
 */ 

std::vector<int> testBasic(int n, int k) {
    Stream s(k);
    for (int i = 0; i < n; ++i) {
        s.onUpdate(i);
    }
    return s.getSample();
}

void testDist(int n, int k, int iters) {
    std::vector<int> counts(n);
    for (int i = 0; i < iters; ++i) {
        std::vector<int> result = testBasic(n, k);
        for (auto val : result) {
            counts[val]++;
        }
    }
    for (int c : counts) {
        std::cout << c << " ";
    }
}

int main() {
    testDist(10, 3, 20000);
    return 0;
}