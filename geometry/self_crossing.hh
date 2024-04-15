#pragma once

/**
 * Problem Link: 
 * https://leetcode.com/problems/self-crossing/description/
 * 
 * Description:
 * You are given an array of integers distance.
 * You start at the point (0, 0) on an X-Y plane, and you move distance[0]
 * meters to the north, then distance[1] meters to the west, distance[2] meters
 * to the south, distance[3] meters to the east, and so on. In other words, 
 * after each move, your direction changes counter-clockwise.
 * Return true if your path crosses itself or false if it does not.
 * 
 * Scratch:
 * Can keep track of sets of vertical segments and horizontal segments
 * Suppose we have placed k non-self-intersecting segments so far and we
 * are now considering a new segment S, WLOG it is horizontal
 * We need to check two things:
 * 1. Does S intersect any existing horizontal segment?
 * 2. Does S intersect any existing vertical segment?
 * 
 * Let S be at height h over the interval [x1, x2]
 * 
*/
class SelfCrossing {
// TODO
};  // class SelfCrossing
