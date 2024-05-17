#pragma once 

#include "../utils/random.hh"

#include <vector>

class Stream {
public:
    Stream(int k) : k_(k) {}

    void onUpdate(int val) {
        if (count_ < k_) {
            samples_.push_back(val);
            count_++;
            return;
        }

        // keep val with prob (k/(count_+1))
        int randVal = rg.randomInt(0, count_);
        bool keep = (randVal < k_);

        if (keep) {
            samples_[randVal] = val;
        }
        count_++;
    }

    std::vector<int> getSample() {
        return samples_;
    }

private:
    int k_;

    std::vector<int> samples_;

    int count_ = 0;

    RandomGenerator rg;
}; 

