#pragma once

#include "point.hh"

#include <cmath>
#include <functional>
#include <random>

class RandomGenerator {
public:
    RandomGenerator() : gen_(std::random_device{}()), 
          uniform_dist_(0.0, 1.0) {}

    int randomInt(int lo, int hi) {
        static std::uniform_int_distribution<> dist(lo, hi);
        return dist(gen_);
    }

    double randomUniform(double a, double b) {
        return a + (b-a) * uniform_dist_(gen_);
    }

    Point randomPointInCenteredSquare() {
        return {randomUniform(-1, 1), randomUniform(-1, 1)};
    }

    Point randomPointInCircle(double radius) {
        // Generate random angle and random radius with square root scaling,
        // then convert from polar to Cartesian coords
        double theta = 2.0 * M_PI * uniform_dist_(gen_);
        double r = radius * sqrt(uniform_dist_(gen_));
        return {r * cos(theta), r * sin(theta)};
    }

    std::vector<int> randomPermutation(int n) {
        std::vector<int> permutation(n);
        iota(permutation.begin(), permutation.end(), 0);
        unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();
        std::shuffle(
            permutation.begin(), permutation.end(), 
            std::default_random_engine(seed)
        );
        return permutation;
    }

    std::vector<int> randomSingleCyclePermutation(int n) {
        std::vector<int> perm = randomPermutation(n);
        std::vector<int> permutation(n);
        for (int i = 0; i < n; ++i) {
            permutation[perm[i]] = perm[(i+1) % n];
        }
        return permutation;
    }

private:
    std::mt19937 gen_;
    std::uniform_real_distribution<> uniform_dist_;
};  // class RandomGenerator
