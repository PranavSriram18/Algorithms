#include "discrete_fourier_transform.hh"

int main() {
    // Test signal
    std::vector<Complex> signal = {0, 1, 3, 4, 6, 8, 11, 12};

    // Compute DFT
    std::vector<Complex> result = directDft(signal);

    // Print result
    for(int i = 0; i < result.size(); i++) {
        std::cout << "X[" << i << "] = " << result[i] << std::endl;
    }

    return 0;
}
