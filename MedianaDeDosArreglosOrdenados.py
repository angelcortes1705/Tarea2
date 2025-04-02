def findMedianSortedArrays(A, B):
    if len(A) > len(B):
        A, B = B, A

    m, n = len(A), len(B)
    low, high = 0, m

    while low <= high:
        i = (low + high) // 2
        j = (m + n + 1) // 2 - i

        maxLeftA = float('-inf') if i == 0 else A[i - 1]
        minRightA = float('inf') if i == m else A[i]
        maxLeftB = float('-inf') if j == 0 else B[j - 1]
        minRightB = float('inf') if j == n else B[j]

        if maxLeftA <= minRightB and maxLeftB <= minRightA:
            if (m + n) % 2 == 1:
                return max(maxLeftA, maxLeftB)
            return (max(maxLeftA, maxLeftB) + min(minRightA, minRightB)) / 2
        elif maxLeftA > minRightB:
            high = i - 1
        else:
            low = i + 1

# EJEMPLO
arr1 = [1, 3, 8]
arr2 = [7, 9, 10, 11]
print(findMedianSortedArrays(arr1, arr2))  # 8
