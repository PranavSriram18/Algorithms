#pragma once

#include <iostream>
#include <vector>
#include <complex>
#include <cmath>

// Define pi
constexpr double PI = M_PI;

// Type for complex numbers
typedef std::complex<double> Complex;

// Function to compute the DFT
std::vector<Complex> directDft(const std::vector<Complex>& x) {
    int N = x.size();
    std::vector<Complex> X(N);
    for(int k = 0; k < N; k++) {
        X[k] = 0;
        for(int n = 0; n < N; n++) {
            double cosWeight = cos(2 * PI * k * n / N);
            double sinWeight = sin(2 * PI * k * n / N);
            double x_r = x[n].real();
            double x_i = x[n].imag();
            X[k] += Complex(
                x_r * cosWeight + x_i * sinWeight,
                x_r * cosWeight - x_i * sinWeight
            );
        }
    }
    return X;
}
