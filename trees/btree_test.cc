#include "btree.hh"

#include "../utils/test_utils.hh"

/** 
 * Usage: 
 * > g++ btree_test.cc -o btree_test -std=c++20
 * > ./btree_test > out.txt
 * 
 * For faster BTree performance, consider the following optimizations:
 * g++ btree_test.cc -o btree_test -std=c++20 -O3
 */ 

using milli = std::chrono::duration<double, std::milli>;
using hr_clock = std::chrono::high_resolution_clock;

void testBasic() {
    BTree<int, int, 4> btree;
    btree.insert(1, 101);
    btree.insert(5, 105);
    btree.insert(8, 108);
    btree.insert(4, 104);
    btree.insert(7, 107);
    auto val4 = btree.value(4);
    std::cout << "Got val4: " << val4.value_or(0) << std::endl;
    assert(val4.value() == 104);
    std::cout << "Checking contains 8..." << std::endl;
    bool contains8 = btree.contains(8);
    std::cout << "contains8: " << contains8 << std::endl;
    std::cout << "Checking contains 6..." << std::endl;
    assert(!btree.contains(6));
    std::cout << "Success" << std::endl;
}

void testDoubleSplit() {
    BTree<int, int, 4> btree;
    std::vector<int> vec {
        100, 200, 300, 400, 150, 125, 140, 130, 120, 110
    };
    /**
    Tree looks like:
           [300]
    [100, 150, 200]  [400]

    Insert 125
           [150, 300]
    [100, 125] [200] [400]

    Insert 140
        [150, 300]
    [100, 125, 140] [200] [400]

    Insert 130
        [130, 150, 300]
    [100, 125] [140] [200] [400]

    Insert 120
        [130, 150, 300]
    [100, 120, 125] [140] [200] [400] 

    Insert 110 to trigger a double split
                    [150]
        [120, 130]              [300]
    [100, 110] [125] [140]  [200] [400]

    */
    for (int v : vec) {
        btree.insert(v, v+100);
        btree.printKeys();
    }
    for (int v : vec) {
        assert(btree.contains(v));
        auto val = btree.value(v);
        assert(val.has_value());
        assert(val.value() == v+100);
    }
    std::cout << "Success!" << std::endl;

}

void testPermutation() {
    BTree<int, int, 4> btree;
    int n = 100;
    RandomGenerator rg;
    std::vector<int> vec = rg.randomPermutation(n);

    for (int v : vec) {
        btree.insert(v, v+100);
        btree.printKeys();
    }
    for (int v : vec) {
        assert(btree.contains(v));
        auto val = btree.value(v);
        assert(val.has_value());
        assert(val.value() == v+100);
    }
    assert(!btree.contains(n+1));
    std::cout << "Success!" << std::endl;
}

void testLargeInsert(int n, int maxVal) {
    std::cout << "Running testLargeInsert with n=" << n << " and maxVal=" << maxVal << std::endl;
    // Generate n random (not necessarily distinct) nums in [0, maxVal)
    RandomGenerator rg;
    std::vector<int> vec = rg.randomVec(n, 0, maxVal-1);

    // Map
    auto mapStart = hr_clock::now();
    std::map<int, int> map;
    for (int k : vec) {
        map[k] = k;
    }
    auto mapEnd = hr_clock::now();
    milli mapDuration = mapEnd - mapStart;
    std::cout << "Map duration: " << mapDuration.count() << " ms" << std::endl;

    auto timeBTree = [&vec, &map]<int B>() {
        auto btreeStart = hr_clock::now();
        BTree<int, int, B> btree;
        for (int k : vec) {
            btree.insert(k, k);
        }
        auto btreeEnd = hr_clock::now();
        milli btreeDuration = btreeEnd - btreeStart;
        std::cout << "BTree duration (B = " << B << "): " << btreeDuration.count() << " ms" << std::endl;
        for (auto& [k, v] : map) {
            assert(btree.value(k).value_or(-1) == v);
        }
    };
    timeBTree.operator()<4>();
    timeBTree.operator()<16>();
    timeBTree.operator()<64>();
    timeBTree.operator()<256>();
    timeBTree.operator()<1024>();
    
    std::cout << "Success" << std::endl;
}

void testReadIntensive(int elems, int maxVal, int numQueries) {
    std::cout << "Running testReadIntensive " << std::endl;
    std::cout << "elems: " << elems << " maxVal: " << maxVal << " numQueries: " << numQueries << std::endl;
    RandomGenerator rg;
    std::vector<int> keys = rg.randomVec(elems, 0, maxVal);
    std::vector<int> queries = rg.randomVec(numQueries, 0, maxVal);

    // Map
    std::map<int, int> map;
    for (int key : keys) {
        map[key] = key;
    }
    auto mapStart = hr_clock::now();
    int64_t mapTotal = 0;
    for (int query : queries) {
        auto it = map.find(query);
        mapTotal += (it == map.end() ? 0 : it->second);
    }
    auto mapEnd = hr_clock::now();
    milli mapDuration = mapEnd - mapStart;
    std::cout << "Map read duration: " << mapDuration.count() << " ms" << std::endl;

    // BTree
    auto timeBTree = [&keys, &queries, &map, &mapTotal]<int B>() {
        BTree<int, int, B> btree;
        for (int key : keys) {
            btree.insert(key, key);
        }
        auto btreeStart = hr_clock::now();
        int64_t btreeTotal = 0;
        for (int query : queries) {
            btreeTotal += btree.value(query).value_or(0);
        }
        auto btreeEnd = hr_clock::now();
        milli btreeDuration = btreeEnd - btreeStart;
        std::cout << "BTree read duration: (B = " << B << "): " << btreeDuration.count() << " ms" << std::endl;
        for (int query : queries) {
            int mapVal = map.count(query) ? map.at(query) : -1; 
            assert(btree.value(query).value_or(-1) == mapVal);
        }
        assert(btreeTotal == mapTotal);
    };
    timeBTree.operator()<4>();
    timeBTree.operator()<16>();
    timeBTree.operator()<64>();
    timeBTree.operator()<256>();
    timeBTree.operator()<1024>();
} 

void testDeleteBasic(int n) {
    std::cout << "Running testDeleteBasic with n=" << n << std::endl;
    std::vector<int> vec(n);
    std::iota(vec.begin(), vec.end(), 0);
    BTree<int, int, 4> btree;
    for (int k : vec) {
        btree.insert(k, k);
        std::cout << "inserted " << k << std::endl;
        btree.printKeys();
    }
    std::cout << "Printing keys before deletion " << std::endl;
    btree.printKeys();
    
    
    for (int k : vec) {
        btree.deleteKey(k);
        btree.printKeys();
    }
    btree.printKeys();
    std::cout << "Done" << std::endl;
}

void testDeleteLarge(int n) {
    std::cout << "Running testDeleteLarge with n=" << n << std::endl; 
    RandomGenerator rg;
    std::vector<int> vec = rg.randomPermutation(n);
    BTree<int, int, 256> btree;
    std::map<int, int> map;
    for (int k : vec) {
        btree.insert(k, k);
        map[k] = k;
    }

    auto mapStart = hr_clock::now();
    for (int k : vec) {
        map.erase(k);
    }
    auto mapEnd = hr_clock::now();
    milli mapDuration = mapEnd - mapStart;
    std::cout << "Map duration " << mapDuration.count() << " ms" << std::endl;


    auto btreeStart = hr_clock::now();
    for (int k : vec) {
        btree.deleteKey(k);
    }
    auto btreeEnd = hr_clock::now();
    milli btreeDuration = btreeEnd - btreeStart;
    std::cout << "BTree delete duration (n=" << n << "): " << btreeDuration.count() << " ms" << std::endl;
    std::cout << "Num tombstones in BTree: " << btree.tombstones() << std::endl;
}

void testMixedWorkload(
    int numReads, int numWrites, int numDeletes, int maxVal
) {
    std::cout << "Running testMixedWorkload " << std::endl;
    std::cout << "numReads: " << numReads << std::endl;
    std::cout << "numWrites: " << numWrites << std::endl;
    std::cout << "numDeletes: " << numDeletes << std::endl;
    std::cout << "maxVal: " << maxVal << std::endl;

    int n = numReads + numWrites + numDeletes;
    enum QueryType {READ = 0, WRITE = 1, DELETE = 2};
    using Query = std::pair<QueryType, int>;
    // Generate a vector of random queries
    RandomGenerator rg;
    std::vector<Query> queries;
    queries.reserve(n);
    for (int i = 0; i < numReads; ++i) {
        queries.emplace_back(READ, rg.randomInt(0, maxVal));
    }
    for (int i = 0; i < numWrites; ++i) {
        queries.emplace_back(WRITE, rg.randomInt(0, maxVal));
    }
    for (int i = 0; i < numDeletes; ++i) {
        queries.emplace_back(DELETE, rg.randomInt(0, maxVal));
    }

    // Map
    std::map<int, int> map;
    int64_t mapTotal = 0;
    auto mapStart = hr_clock::now();
    for (int i = 0; i < n; ++i) {
        auto [queryType, key] = queries[i];
        if (queryType == READ) {
            auto it = map.find(key);
            if (it != map.end()) mapTotal += it->second;
        } else if (queryType == WRITE) {
            map[key] = key;
        } else {
            map.erase(key);
        }
    }
    auto mapEnd = hr_clock::now();
    milli mapDuration = mapEnd - mapStart;
    std::cout << "Map duration: " << mapDuration.count() << " ms" << std::endl;

    // BTree
    BTree<int, int, 256> btree;
    int64_t btreeTotal = 0;
    auto btreeStart = hr_clock::now();
    for (int i = 0; i < n; ++i) {
        auto [queryType, key] = queries[i];
        if (queryType == READ)
            btreeTotal += btree.value(key).value_or(0);
        else if (queryType == WRITE) {
            btree.insert(key, key);
        } else {
            btree.deleteKey(key);
        }
    }
    auto btreeEnd = hr_clock::now();
    milli btreeDuration = btreeEnd - btreeStart;
    std::cout << "BTree duration " << btreeDuration.count() << " ms" << std::endl;

}

int main() {
    // testBasic();
    // testPermutation();
    // testLargeInsert(1000000, 100000000);
    // testReadIntensive(10000, 1000000, 1000000);
    // testDeleteBasic(10);
    testDeleteLarge(1e6);
    // testMixedWorkload(1e7, 1e7, 1e7, 1e6);
    // Delete heavy
    // testMixedWorkload(1e7, 1e7, 1e8, 1e8);
    return 0;
}