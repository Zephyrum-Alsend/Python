'''/**
* INTERSECTION
*
* Directions
*
*     Given two arrays of positive integers, return the greatest
*     value from the intersection of the two arrays.
*
*     You may assume the intersection is not empty.
*
* Examples
*
*     Max of [ 1, 5, 3, 7, 9, 4, 5 ] n [ 13, 7, 10, 4, 2 ] is 7.
*     Max of [ 43, 13, 2 ] n [ 13, 44, 5, 2 ] is 13.
*
**/'''

from asyncio.windows_events import INFINITE


list1 = [ 1, 5, 3, 7, 9, 4, 5 ]
list2 = [ 13, 7, 10, 4, 2 ]

list3 = [ 43, 13, 2 ]
list4 = [ 13, 44, 5, 2 ]

def intersection(arr1, arr2):
    output = []

    for i in arr1:
        if i in arr2:
            output.append(i)
        # for j in arr2:
        #     if i == j: output.append(i)

    return output

def findMaxInList(arr):
    maxVal = -INFINITE

    for i in arr:
        if i > maxVal:
            maxVal = i

    return maxVal

if __name__ == '__main__':
    print(findMaxInList(intersection(list1, list2)))
    print(findMaxInList(intersection(list3, list4)))