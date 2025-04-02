def counting_sort(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10

    for num in arr:
        index = abs(num) // exp
        count[index % 10] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    for i in range(n - 1, -1, -1):
        index = abs(arr[i]) // exp
        output[count[index % 10] - 1] = arr[i]
        count[index % 10] -= 1

    for i in range(n):
        arr[i] = output[i]

def radix_sort(arr):
    if not arr:
        return []

    positives = [num for num in arr if num >= 0]
    negatives = [-num for num in arr if num < 0]

    max_pos = max(positives, default=0)
    max_neg = max(negatives, default=0)

    exp = 1
    while max_pos // exp > 0:
        counting_sort(positives, exp)
        exp *= 10

    exp = 1
    while max_neg // exp > 0:
        counting_sort(negatives, exp)
        exp *= 10

    negatives = [-num for num in reversed(negatives)]

    return negatives + positives

# EJEMPLO
arr = [170, -45, 75, -90, 802, 24, 2, 66, -123]
sorted_arr = radix_sort(arr)
print(sorted_arr)  # [-123, -90, -45, 2, 24, 66, 75, 170, 802]
