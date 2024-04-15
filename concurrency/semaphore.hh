#pragma once 

#include <mutex>
#include <condition_variable>

class Semaphore {
public:
    explicit Semaphore(int value = 0) : value_(value) {}

    void wait() {
        std::unique_lock<std::mutex> lock(mutex_);
        cv_.wait(lock, [this](){ return value_ > 0; });
        value_--;
    }

    void signal() {
        std::unique_lock<std::mutex> lock(mutex_);
        if (++value_ == 1) cv_.notify_all();
    }

private:
    int value_;
    std::mutex mutex_;
    std::condition_variable cv_;

};  // class Semaphore
