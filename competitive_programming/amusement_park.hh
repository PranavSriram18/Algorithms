/**
 * Source: Singapore NOI 2024
 * 
 * 
 * 
 * Q = [(0, 5, true), (1, 4, true), (2, 10, true)]
 * Q = [(0, 5, true), (1, 4, false), (2, 10, true)]
 * 
 * head - position of start of queue.
 * 
 * 
 * join - O(1)
 * leave - O(1)
 * board:
 * (i) - whole group boards. advance head
 * 
 * 
 * Each group that can't split and whose size is too big is
 * an obstacle
 * We want a way to efficiently jump over these obstacles while scanning
 * 
 * "What is the next entry in my list whose size is at most some query value"
 * 
 */

class SegmentTree {
public:
    explicit SegmentTree(const vector<int>& vec) {
        // TODO
    }

    void update(int pos, int val) {
        // TODO
    }

    int getNextIdx(int startPos, int threshold) {
        // TODO
    }
};  // class SegmentTree

class ParkQueue {
public:
    constexpr int kMaxElems = 200000;

    ParkQueue() {
        vector<int> v(kMaxElems, INT_MAX);
        stree_ = SegmentTree(v);
        Group g(INT_MAX, false);
        groups_ = vector<Group>(kMaxElems, g);
    }

    struct Group {
        int numMembers;
        bool canSplit;

        Group(int n, bool s) {
            numMembers = n;
            canSplit = s;
        }

        int streeValue() {
            return canSplit ? 0 : groupSize;
        }
    };

    int join(int groupSize, bool canSplit) {
        Group group(groupSize, canSplit);
        groups_[numGroups_] = group;
        stree_.update(numGroups_++, group.streeValue());
    }

    void leave(int groupID) {
        stree_.update(groupID, INT_MAX);
    }

    // List of (groupID, numToBoard) pairs
    vector<pair<int, int>> board(int numSeats) {
        vector<pair<int, int>> result;
        int groupIdx = stree_.getNextIdx(0, numSeats);
        while (numSeats && groupIdx < numGroups_) {
            Group& group = groups_[groupIdx];
            // Case 1 - whole group boards
            if (group.numMembers <= numSeats) {
                numSeats -= group.numMembers;
                stree_.update(groupIdx, INT_MAX);
                result.emplace_back(groupIdx++, group.numMembers);
            } else {
                // Case 2 - board part of the group
                group.numMembers -= numSeats;
                stree_.update(groupIdx, group.numMembers);
                result.emplace_back(groupIdx, numSeats);
                numSeats = 0;
            }
            groupIdx = stree_.getNextIdx(groupIdx, numSeats);
        }
        return result;
    }

private:
    vector<Group> groups_;
    SegmentTree stree_;
    int numGroups_ = 0;

};  // class ParkQueue
