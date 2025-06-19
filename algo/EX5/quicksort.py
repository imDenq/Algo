import random

def deterministic_quicksort(arr):
    if len(arr) <= 1:
        return arr[:]
    pivot = arr[-1]
    less = [x for x in arr[:-1] if x <= pivot]
    greater = [x for x in arr[:-1] if x > pivot]
    return deterministic_quicksort(less) + [pivot] + deterministic_quicksort(greater)

def randomized_quicksort(arr):
    if len(arr) <= 1:
        return arr[:]
    pivot = random.choice(arr)
    less = [x for x in arr if x < pivot]
    equal = [x for x in arr if x == pivot]
    greater = [x for x in arr if x > pivot]
    return randomized_quicksort(less) + equal + randomized_quicksort(greater)
