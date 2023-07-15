def solution(A):
    # 1. Initialize a set to store all the elements in A.
    s = set()
    for i in range(len(A)):
        s.add(A[i])
    # 2. Iterate over all the integers from 1 to 1000000.
    # If an integer is not in the set, then return it.
    for i in range(1, 1000001):
        if i not in s:
            return i
    # 3. If all the integers from 1 to 1000000 are in the set, then return 1.
    return 1

A = [-1, -3]
print(solution(A))
