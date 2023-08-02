
#include "random_dists.hh"

#include <unordered_map>

/*
Code for experiments using the RandomPointSimulator.
We will often work with the inverse distance here, denoted f.
*/

// f -> (average points, density)
using ResultTable = std::unordered_map<double, std::pair<double, double>>;

// Number of runs of the simulation for a fixed distance
const int kNumTrials = 10;

// Iterations per simulation
const int kNumIters = 1000000;

// Print frequency for simulator object
const int kPrintFreq = 100000;

void runExperiment(double f, RandomPointSimulator& rps,  ResultTable& table) {
    double dist = 1.0 / f;
    std::cout << "Running experiment with f = " << f << " (dist = " << dist << ")" << std::endl;  
    std::vector<int> results(kNumTrials);
    for (int it = 0; it < kNumTrials; ++it) {
        std::cout << "Running trial " << it << std::endl;
        results[it] = rps.runSimulation(dist, kNumIters, kPrintFreq);
    }
    std::cout << "Result summary for f " << f << ":" << std::endl;
    double total = 0.0;
    for (int val : results) {
        total += val;
        std::cout << val << " ";
    }
    
    double upperBound = (2.0 * f + 1.0) * (2.0 * f + 1.0);
    double average = total / kNumTrials;
    double density = average / upperBound;
    std::cout << "\nAverage points placed was " << average << std::endl;
    std::cout << "Corresponding density: " << average / upperBound;
    table[f] = {average, density};
}

int main() {
    RandomPointSimulator rps;
    std::vector<double> invDistances {
        1.0, 2.0, 3.0, 4.0, 5.0, 10.0, 20.0, 50.0, 100.0
    };
    ResultTable table;
    for (double f : invDistances) {
        runExperiment(f, rps, table);
    }
    // Print the result table
    std::cout << "Result table: " << std::endl;
    for (const auto& [f, resultPair] : table) {
        auto [avg, density] = resultPair;
        std::cout << "f: " << f << " points: " << avg << " density: " << density << std::endl;
    }
    return 0;
}