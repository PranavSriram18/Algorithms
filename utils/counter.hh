#pragma once

#include <map>

template<typename K, typename V, typename COMP = std::less<K>>
class Counter {
public:
    void increment(const K& key) {
        map_[key]++;
    }

    // decrement the key if it exists, otherwise do nothing
    void decrement(const K& key) {
        auto it = map_.find(key);
        if (it != map_.end() && --(it->second) == 0) map_.erase(it);
    }

    K firstKey() const {
        return map_.empty() ? K() : map_.begin()->first;
    }

    K lastKey() const {
        return map_.empty() ? K() : (--map_.end())->first;
    }

private:
    std::map<K, V, COMP> map_;
};  // class Counter
