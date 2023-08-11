#include <iostream>

#include "jump_game_2.hh"

int main() {
    std::vector<int> nums {2,3,0,1,4};
    JumpGame2 solver;
    std::cout << "Jumps required: " << solver.solve(nums) << std::endl;
    return 0;
}