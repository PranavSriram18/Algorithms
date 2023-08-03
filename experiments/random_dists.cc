
#include "random_dists.hh"

#include <chrono>
#include <map>

/*
Code for experiments using the RandomPointSimulator.
We will often work with the inverse distance here, denoted f.
*/

// radius -> (average points, density)
using ResultTable = std::map<double, std::pair<double, double>>;

// Number of runs of the simulation for a fixed distance
const int kNumTrials = 10;

// Iterations per simulation
const int kBaseNumIters = 100000;

// Print frequency for simulator object
const int kPrintFreq = 100000;

void runExperiment(double r, ResultTable& table) {
    std::cout << "\nRunning experiment with radius = " << r << std::endl;  
    std::vector<int> results(kNumTrials);

    auto start = std::chrono::high_resolution_clock::now();
    for (int trial = 0; trial < kNumTrials; ++trial) {
        std::cout << "Running trial " << trial << std::endl;
        std::string filename = "out/radius_" + std::to_string(
            int(r)) + "_trial_" + std::to_string(trial) + ".txt";
        RandomPointSimulator rps(r, filename);
        // scale the number of iterations with the radius
        results[trial] = rps.runSimulation(kBaseNumIters * r, kPrintFreq);
    }
    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = end - start;

    std::cout << "Result summary for radius " << r << ":" << std::endl;
    double total = 0.0;
    for (int val : results) {
        total += val;
        std::cout << val << " ";
    }
    
    double upperBound = (2.0 * r + 1.0) * (2.0 * r + 1.0);
    double average = total / kNumTrials;
    double density = average / upperBound;
    std::cout << "\nAverage points placed was " << average << std::endl;
    std::cout << "Corresponding density: " << average / upperBound;
    table[r] = {average, density};

    // Print elapsed time
    std::cout << "\nElapsed time for experiment: " << elapsed.count() << " seconds." << std::endl;
}

int main() {
    std::vector<double> radii {
        20.0, 50.0, 100.0
    };
    ResultTable table;
    for (double r : radii) {
        runExperiment(r, table);
    }
    // Print the result table
    std::cout << "\nResult table: " << std::endl;
    for (const auto& [radius, resultPair] : table) {
        auto [avg, density] = resultPair;
        std::cout << "radius: " << radius << " points: " << avg << " density: " << density << std::endl;
    }
    return 0;
}
