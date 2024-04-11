#include "ant_permutation.hh"

#include <chrono>
#include <map>

// g++ -std=c++17 run_simulation.cc ant_permutation.cc -o run_simulation

const int kNumAnts = 100;
const int kNumIters = 20000;

int main() {
    AntPermutation ap(kNumAnts, "out.txt");
    ap.run(kNumIters);
    return 0;
}
