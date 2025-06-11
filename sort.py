def bubble_sort(data, key=None, ascending=True):
    n = len(data)
    result = data.copy()

    for i in range(n):
        for j in range(0, n - i - 1):
            a = result[j][key] if key else result[j]
            b = result[j + 1][key] if key else result[j + 1]
            if (ascending and a > b) or (not ascending and a < b):
                result[j], result[j + 1] = result[j + 1], result[j]

    return result
