""" 
Problem description: https://leetcode.com/problems/decode-string/description/

Basic idea: use a stack. 
1. "]" triggers evaluation of portion enclosed between this and most recent "[".
2. Once we seek to the most recent "[", we need to get the number that 
multiplies this block.
3. To get this number, we just walk backwards while the popped char is a digit.
"""
class Solution:
    def decode_string(self, s: str) -> str:
        result = ""
        stack = []

        for ch in s:
            if ch != "]":
                stack.append(ch)
            else:
                # trigger evaluation of enclosed []
                last_popped, buffer = None, ""
                while 1:
                    last_popped = stack.pop()
                    if last_popped != "[":
                        buffer += last_popped
                    else:
                        break
                inner = buffer[::-1]
                # get the number of repeats
                last_popped, buffer = None, ""
                while 1:
                    if not stack:
                        break
                    last_popped = stack.pop()
                    if last_popped.isdigit():
                        buffer += last_popped
                    else:  # gone too far
                        stack.append(last_popped)
                        break
                num = int(buffer[::-1])
                expanded = inner * num
                stack.extend(expanded)
        return ''.join(stack)
                