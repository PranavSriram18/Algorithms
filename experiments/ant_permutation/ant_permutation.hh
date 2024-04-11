
#include "../../utils/point.hh"
#include "../../utils/random.hh"

#include <fstream>
#include <iostream>
#include <vector>

class AntPermutation {
public:
    explicit AntPermutation(int numAnts, const std::string& outFile);
    void run(int numIters);

private:
    constexpr static double kStepMultiplier = 1.0001;

    void initPositions();
    void step();
    void writePointsToFile();
    
    int n_;  // number of ants
    double freeEnergy_;

    RandomGenerator rg_;
    std::ofstream outFile_;

    // ith entry is ant that ith ant follows
    std::vector<int> permutation_;
    // position of ith ant
    std::vector<Point> positions_;
};  // class AntPermutation
