def sequential_search(data_list, target):
    for i in range(len(data_list)):
        if data_list[i] == target:
            return i
    return -1
