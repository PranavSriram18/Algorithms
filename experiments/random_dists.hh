
#include "../utils/point.hh"
#include "../utils/random.hh"

#include <fstream>
#include <iostream>
#include <vector>

/**
 This code is inspired by a question posted to the Facebook group
 "Actually good math problems." Our modified problem is as follows.
 
 Tim is putting pins on a circle of radius d in R^2. First, he puts one at a uniformly random position. Then, Tim uniformly randomly chooses a point inside disk until he happens to choose one that is at least distance 1 from every other previously pinned point, and pins that point. He repeats this process until it is impossible to pin any more points in this way. What is the expected value of the number of pinned points? 
  
 This class allows approximately solving this problem using a Monte Carlo simulation.
*/
class RandomPointSimulator {
public:
    /**
     Initializes a RandomPointSimulator object.
     \param radius The radius of the circular disk.
    */
    RandomPointSimulator(
        double radius, std::string outputFile = ""
    ) : radius_(radius), outputFile_(outputFile) {
        // initialize the grid
        ceilRadius_ = static_cast<int>(std::ceil(radius_));
        int gridSize = 2 * ceilRadius_ + 1;
        pointGrid_ = std::vector<std::vector<std::vector<Point>>>(
            gridSize, std::vector<std::vector<Point>>(gridSize)
        );
    }

    /**
     Runs the simulation for the given number of iterations.
     Time complexity: O(kn), where n is number of iterations and k is answer. From experiments and mathematical bounds, k is O(f^2),
     where f = 1/dist. So total time complexity is O(nf^2).
    */
    int runSimulation(
        int iters,
        int printFreq
    ) {
        // Tracks the set of valid points placed
        for (int i = 0; i < iters; ++i) {
            Point point = rg_.randomPointInCircle(radius_);  // TODO
            if (isValid(point)) {
                addPoint(point);
            }

            if ((i % printFreq) == 0 || i == (iters - 1)) {
                std::cout << "Iteration " << i << ": Placed " << points_.size() << " points." << std::endl;
            }
        }
        writePointsToFile();
        return points_.size();
    }

private:
    // (i, j) entry is the list of points in the (i, j) grid cell
    using PointGrid = std::vector<std::vector<std::vector<Point>>>;

    using GridCell = std::pair<int, int>;

    // Places the given point
    void addPoint(const Point& point) {
        GridCell cell = gridCell(point);
        pointGrid_[cell.first][cell.second].push_back(point);
        points_.push_back(point);
    }

    // Gets the grid cell containing the given point
    GridCell gridCell(const Point& point) const {
        return {
            ceilRadius_ + static_cast<int>(std::floor(point.x())), 
            ceilRadius_ + static_cast<int>(std::floor(point.y()))
        };
    }

    // Gets the points in the given grid cell. Performs bounds checks.
    const std::vector<Point>& getPoints(const GridCell& cell) const {
        if (cell.first < 0 || cell.first > 2 * ceilRadius_) return emptyVec_;
        if (cell.second < 0 || cell.second > 2 * ceilRadius_) return emptyVec_;
        return pointGrid_[cell.first][cell.second];
    }

    // Checks whether a given point can be legally placed. Caller is responsible
    // for bounds checking.
    bool isValid(const Point& point) const {
        GridCell cell = gridCell(point);
        for (int hshift = -1; hshift <= 1; ++hshift) {
            for (int vshift = -1; vshift <= 1; ++vshift) {
                GridCell currCell {hshift + cell.first, vshift + cell.second};
                for (const Point& currPoint : getPoints(currCell)) {
                    if (point.squaredDist(currPoint) < 1) return false;
                }
            }
        }
        return true;
    }

    void writePointsToFile() {
        if (outputFile_.empty()) return;
        std::ofstream file(outputFile_);
        if (!file.is_open()) {
            std::cerr << "Failed to open the file: " << outputFile_ << std::endl;
            return;
        }
        for (const Point& point : points_) {
            file << point.x() << " " << point.y() << "\n";
        }
        file.close();
    }

    // Radius of the disk
    double radius_;
    int ceilRadius_;

    // The (i, j) grid entry stores points with coordinates (u, v)
    // where floor(u) = -r + i, floor(v) = -r + j.  
    PointGrid pointGrid_;

    // The set of points that has been placed
    std::vector<Point> points_;

    RandomGenerator rg_;

    std::vector<Point> emptyVec_;

    // Name of the 
    std::string outputFile_;

};  // class RandomPointGenerator
