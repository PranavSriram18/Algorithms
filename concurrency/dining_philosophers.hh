#pragma once

#include "semaphore.hh"
#include "../utils/random.hh"

#include <iostream>
#include <thread>
#include <vector>

/**
 * Implements a solution to the classing Dining Philosopher problem.
 * We use a Semaphore to maintain the invariant that at most n-1 philosophers
 * attempt to eat at a given time, which in turn guarantees that at least one
 * philosopher is capable of eating, avoiding deadlock.
*/
class DiningPhilosophers {
public:
    DiningPhilosophers(
        int n, int numMeals = 3
    ) : n_(n), numMeals_(numMeals), permits_(n-1), forkMutexes_(n) {}

    void run() {
        std::vector<std::thread> threads(n_);
        for (int i = 0; i < n_; ++i) {
            threads[i] = std::thread([this, i]() { this->philosophize(i); } );
        }
        for (auto& t : threads) {
            t.join();
        }
    }

private:
    void philosophize(int i) {
        for (int j = 0; j < numMeals_; ++j) {
            think(i);
            eat(i);
        }
    }

    void think(int i) {
        print("Philosopher " + std::to_string(i) + " starts thinking");
        std::this_thread::sleep_for(std::chrono::milliseconds(getThinkTimeMillis()));
        print("Philosopher " + std::to_string(i) + " done thinking");
    }

    void eat(int i) {
        permits_.wait();
        std::unique_lock<std::mutex> leftLock(forkMutexes_[i]);
        std::unique_lock<std::mutex> rightLock(forkMutexes_[(i+1) % n_]);
        print("Philosopher " + std::to_string(i) + " starts eating");
        std::this_thread::sleep_for(std::chrono::milliseconds(getEatTimeMillis()));
        print("Philosopher " + std::to_string(i) + " done eating");
        permits_.signal();
    }

    int getEatTimeMillis() {
        return rg_.randomInt(kMinEatTimeMillis, kMaxEatTimeMillis);
    }

    int getThinkTimeMillis() {
        return rg_.randomInt(kMinThinkTimeMillis, kMaxThinkTimeMillis);
    }

    void print(const std::string& message) {
        std::lock_guard<std::mutex> lg(coutMutex_);
        std::cout << message << std::endl;
    }

    static constexpr int kMinThinkTimeMillis = 300;
    static constexpr int kMaxThinkTimeMillis = 500;
    static constexpr int kMinEatTimeMillis = 100;
    static constexpr int kMaxEatTimeMillis = 300;

    // Number of philosophers
    int n_;

    // Number of meals each philosopher eats
    int numMeals_;

    // Mutexes for the n_ forks
    std::vector<std::mutex> forkMutexes_;

    // Semaphore that ensures at most n_-1 philosophers attempt to eat at a time
    Semaphore permits_;

    // Mutex to guard printing to cout
    std::mutex coutMutex_;

    RandomGenerator rg_;

};  // class DiningPhilosophers
