
/**
 *  Source: Singapore National Olympiad in Informatics 2024
 * Problem Description:
Zane is the principal of NOI school. NOI school has n classes, and each class has s students.
Student j in class i has height h[i][j].
Zane wants to select 1 student from each class to take a school photo. To make the photo look
nicer, Zane wants to select students such that the height difference between the tallest student
and shortest student selected is as small as possible.

Scratch:

C0: [4, 18, 29]
C1: [12, 17, 72]
C3: [15, 66, 93]
C4: [5, 13, 107]

Idea 1: Any pair of classes provides a lower bound on our solution.
This lower bound may not be achievable. 

Suppose I make some selections t0, t1, ..., t_{n-1}

Let's call the max and min M and m respectively
So I know that m <= t_i <= M

Step 1: sort each list
Time complexity: O(nslog(s))

For a given pair (m, M), is it possible to achieve m <= t_i <= M for each i?
Fix m, M. How long does it take to verify if (m, M) feasible?
-> O(nlog(s))

(1, 10^9) -> yes

a0, a1, ..., a_{ns-1}

m, M are a_i and a_j for some (i, j)

m = a0
M = a_{ns-1}

(m, M) -> isFeasible?

If I fix m, then in O(nlog(s)) time, I can get f(m) (=M - m)

Semi-naive algorithm:
there are ns choices for m
for each of them, run above procedure
O(n^2slog(s)) algorithm


Step 1: Sort each list -> O(nslog(s))
Step 2: Calculate a global sorted list -> O(nslog(ns)).
Call this list a0, ..., a_{ns-1}
Step 3: Initialize m = a0
Step 4: Initialize pointers. In each list, will be first elem h[i, 0]
Step 5: Loop as follows:
    Calculate current discrepancy
    Update m to next value in global list
    For each list, advance pointer to next thing >= m. Zero or 1 steps

Time complexity of Step 5: O(ns)

C0: [4, 18, 29]
C1: [12, 17, 72]
C2: [15, 66, 93]
C3: [5, 13, 107]

p = (0, 0, 0, 0), m = 4, l = 0, d = 11
p = (1, 0, 0, 0), m = 5, l = 3, d = 13
p = (1, 0, 0, 1), m = 12, l_m = 1, d = 6, l_M 
*/

class Solution {

};  // class Solution

