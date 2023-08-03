#pragma once

#include <functional>

// Represents a point in 2D
class Point {
public:
    Point() = default;

    Point(double x, double y) : x_(x), y_(y) {}

    double x() const { 
        return x_; 
    }

    double y() const { return y_; }

    double squaredDist(const Point& other) const {
        return (x_ - other.x_) * (x_ - other.x_) + (
            y_ - other.y_) * (y_ - other.y_);
    }

    bool operator==(const Point& other) {
        return x_ == other.x_ && y_ == other.y_;
    }

    // Note that this only defines a partial order
    bool operator<(const Point& other) {
        return x_ < other.x_ && y_ < other.y_;
    }

    friend struct std::hash<Point>;

private:
    double x_;
    double y_;
};

namespace std {
    template<> struct hash<Point> {
        std::size_t operator()(const Point& p) const {
            std::hash<int> int_hash;
            return int_hash(p.x_) ^ (int_hash(p.y_) << 1);
        }
    };
}
