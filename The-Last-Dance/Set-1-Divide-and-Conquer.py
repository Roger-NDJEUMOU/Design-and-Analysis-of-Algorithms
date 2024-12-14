""" SET 1 - DIVIDE AND CONQUER """

import math

def sum_of_numbers(A: list, lower: int, upper: int) -> int:
    """ Compute the sum of n numbers using divide-and-conquer strategy. """
    if lower == upper:
        return A[lower]

    mid = math.floor((lower + upper)/2) # mid = (lower + upper) // 2
    return sum_of_numbers(A, lower, mid) + sum_of_numbers(A, mid+1, upper)


def merge(A: list, l: int, m: int, u:int):
    """ Combine the sorted portions, A[l..m-1] and A[m..u] into a single array A[l..u] """
    
    # Creating the sorted portion
    B = A[l:m+1]
    C = A[m+1:u+1]

    # Merging the arrays, while maintening the result sorted.
    i = 0
    j = 0
    k = l
    while i < len(B) and j < len(C) :
        if B[i] < C[j]:
            A[k] = B[i]
            i += 1
        else:
            A[k] = C[j]
            j += 1
        k += 1

    while i < len(B):
        A[k] = B[i]
        i += 1
        k += 1
    
    while j < len(C):
        A[k] = C[j]
        j += 1
        k += 1


def mergesort(A: list, lower: int, upper: int):
    """ Sort the given array A[0..n-1] by dividing it into two halves
        A[0..⌊n/2⌋-1] and A[⌊n/2⌋..n-1], sorting each of them recursively, and then
        merging the two smaller sorted arrays into a single sorted one. """
    
    if lower < upper:
        mid = math.floor((lower + upper) / 2 ) 
        mergesort(A, lower, mid)
        mergesort(A, mid+1, upper)
        merge(A, lower, mid, upper)


def swap(A:list, i:int, j:int):
    """ swap(A[i], A[j]) """
    aux = A[i]
    A[i] = A[j]
    A[j] = aux


def partition(A: list, l:int, r:int) -> int:
    """ Select the first element of A[l..r] as pivot, then split the array A such that
        all elements less than or equal to the pivot appear to its left and all 
        elements greater than the pivot appear on its right. Finally, return the 
        pivot as the partition/split position. """
    
    pivot = A[l]

    i = l+1
    j = r
    while i < j:
        while A[i] < pivot:
            i += 1
        while A[j] > pivot:
            j -= 1
        swap(A, i, j)

    swap(A, i, j) # undo last swap when i ≥ j
    swap(A, l, j)

    return j


def quicksort(A:list, l:int, r:int):
    """ Sorts a subarray by quicksort """
    if l < r:
        split = partition(A, l, r)
        quicksort(A, l, split-1)
        quicksort(A, split+1, r)


if __name__ == "__main__" :
    A = [8, 3, 2, 9, 7, 1, 5, 4]

    quicksort(A, 0, len(A)-1)

    # mergesort(A, 0, len(A)-1)

    print(f"Sorted: {A}")

    # print(sum_of_numbers(A, 0, len(A)-1))

