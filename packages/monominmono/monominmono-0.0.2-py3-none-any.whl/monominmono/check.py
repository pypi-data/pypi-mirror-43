def find_min_lin(array):
    return min(array)


def find_min_lin_stop(array, ind=0):
    if array[ind] < array[ind + 1]:
        minimum = array[ind]
        return minimum
    else:
        return find_min_lin_stop(array, ind + 1)


def find_min_binary_search(array, middle=None, step=None):
    if middle is None:
        middle = len(array) // 2
        step = len(array) // 4

    if array[middle - 1] > array[middle]:
        if array[middle] < array[middle + 1]:
            return array[middle]
        else:
            middle += step
            return find_min_binary_search(array, middle, step//2)
    elif array[middle] < array[middle+1]:
        middle -= step
        return find_min_binary_search(array, middle, step//2)


def find_min_binary_flat_spots(array, middle=None, step=None):
    i = 1
    if middle is None:
        middle = len(array) // 2
        step = len(array) // 4
    if array[middle - 1] >= array[middle]:
        while array[middle] == array[middle + i]:
            i += 1
        if array[middle] < array[middle + i]:
            return array[middle]
        else:
            middle += step + i - 1
            return find_min_binary_flat_spots(array, middle, step//2)
    elif array[middle] <= array[middle+1]:
        while array[middle] == array[middle - i]:
            i += 1
        middle -= step + i - 1
        return find_min_binary_flat_spots(array, middle, step//2)
