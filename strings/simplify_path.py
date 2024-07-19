
""" 
Given an absolute path for a Unix-style file system, which begins with a slash 
'/', transform this path into its simplified canonical path.

Full problem description: https://leetcode.com/problems/simplify-path/description/
Level: LC Medium

Basic idea:
State machine with a stack. 
".." pops the last dir-name, "." does nothing, nonempty dir-names get pushed.
"""
class Solution:
    def simplify_path(self, path: str) -> str:
        components = path.split('/')
        results = []
        for c in filter(lambda x: x and x != ".", components):
            if c == "..":
                if results:
                    results.pop() 
            else:
                results.append(c)
        return "/" + "/".join(results)

if __name__=="__main__":
    s = Solution()
    paths = [
        "/home/user/Documents/../Pictures",
        "/..",
        "/a/b/../c/../d"
    ]
    for path in paths:
        print(s.simplify_path(path))
