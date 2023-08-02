
#include "../utils/point.hh"
#include "../utils/random.hh"

#include <iostream>
#include <vector>

/**
 * This code is inspired by a question posted to the Facebook group
 * "Actually good math problems." The original question was:
 * 
 * Tim is putting pins on the unit disk in R^2. First, he puts one at a
 * uniformly random position. Then, Tim uniformly randomly chooses a point
 * inside the unit disk until he happens to choose one that is at least distance
 * 1/10 from every other previously pinned point, and pins that point. He 
 * repeats this process until it is impossible to pin any more points in this
 * way. What is the expected value of the number of pinned points? 
 * 
 * This class allows approximately solving a slightly more general version of
 * this problem, taking an arbitrary distance threshold as an input parameter,
 * using a Monte Carlo simulation. 
*/
class RandomPointSimulator {
public:
    RandomPointSimulator() = default;

    /**
     Time complexity: O(kn), where n is number of iterations and k is answer. From experiments and from mathematical bounds, k is O(f^2),
     where f = 1/dist. So total time complexity is O(nf^2).
    */
    int runSimulation(
        double dist,
        int iters,
        int printFreq
    ) {
        // Tracks the set of valid points placed
        std::vector<Point> points;
        for (int i = 0; i < iters; ++i) {
            Point point = rg_.randomPointInUnitCircle();
            if (isValid(points, point, dist)) {
                points.push_back(point);
            }

            if ((i % printFreq) == 0 || i == (iters - 1)) {
                std::cout << "Iteration " << i << ": Placed " << points.size() << " points." << std::endl;
            }
        }
        return points.size();
    }

private:
    bool isValid(
        const std::vector<Point>& points, 
        const Point& point,
        double dist) const {
        double minSquaredDist = dist * dist;
        for (const auto& currPoint : points) {
            if (point.squaredDist(currPoint) < minSquaredDist) return false;
        }
        return true;
    }

    RandomGenerator rg_;

};  // class RandomPointGenerator
