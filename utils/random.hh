#pragma once

#include "point.hh"

#include <cmath>
#include <functional>
#include <random>

class RandomGenerator {
public:
    RandomGenerator() : gen_(std::random_device{}()), 
          uniform_dist_(0.0, 1.0) {}

    Point randomPointInCircle(double radius) {
        // Generate random angle and random radius with square root scaling,
        // then convert from polar to Cartesian coords
        double theta = 2.0 * M_PI * uniform_dist_(gen_);
        double r = radius * sqrt(uniform_dist_(gen_));
        return {r * cos(theta), r * sin(theta)};
    }

private:
    std::mt19937 gen_;
    std::uniform_real_distribution<> uniform_dist_;
};  // class RandomGenerator
