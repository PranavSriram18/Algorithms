#include "ant_permutation.hh"


AntPermutation::AntPermutation(int numAnts, const std::string& outFile) {
    n_ = numAnts;
    outFile_ = std::ofstream(outFile);
    rg_ = RandomGenerator();
    permutation_ = rg_.randomSingleCyclePermutation(n_);
    initPositions();
}

void AntPermutation::run(int numIters) {
    for (int it = 0; it < numIters; ++it) {
        step();
    }
    outFile_.close();
}

// Private methods

void AntPermutation::initPositions() {
    positions_.resize(n_);
    Point mean(0.0, 0.0);
    for (int i = 0; i < n_; ++i) {
        positions_[i] = rg_.randomPointInCenteredSquare();
        mean += positions_[i];
    }
    mean /= n_;
    for (int i = 0; i < n_; ++i) {
        positions_[i] -= mean;
    }
    for (int i = 0; i < n_; ++i) {
        freeEnergy_ += positions_[i].squaredNorm();
    }
}

void AntPermutation::step() {
    std::vector<Point> newPositions(n_);
    // First take a small step
    for (int i = 0; i < n_; ++i) {
        Point& currAnt = positions_[i];
        Point& leader = positions_[permutation_[i]];
        newPositions[i] = (currAnt + (leader - currAnt) * 0.01);
    }
    // Then balance free energy
    for (int i = 0; i < n_; ++i) {
        newPositions[i] *= kStepMultiplier;
    }

    for (int i = 0; i < n_; ++i) {
        positions_[i] = newPositions[i];
    }
    writePointsToFile();
}

void AntPermutation::writePointsToFile() {
    for (const auto& point : positions_) {
        outFile_ << point.x() << " " << point.y() << "\n"; 
    }
}
