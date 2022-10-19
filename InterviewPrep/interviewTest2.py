# /**
# * SUBSTRINGS
# *
# * Directions
# *
# *     Given two strings, count and return the number of times
# *     that the second string is found within the first string.
# *
# * Examples
# *
# *     Given:
# *         string A = "This is an example, isn't it?.";
# *         string B = "is";
# *       String B can be found three (3) times in string A:
# *        "Th[is] [is] an example, [is]n't it?
# *     Answer: 3.
# *
# *     Given:
# *         string A = "Sit here, there, or anywhere, there are many open seats.";
# *         string B = "here, there";
# *       String B can be found two (2) times in string A:
# *         "Sit [here, there], or anyw[here, there] are many open seats."
# *     Answer: 2.
# *
# **/

def findInstancesOfSubstring(mainstring, substring):
    currentSplice = mainstring
    currentIndex = -1
    count = 0
    
    if len(substring) > len(mainstring) or len(substring) <= 0:
        return count

    # print('Starting while loop')
    while(True):
        # print('Iterating once')
        currentIndex = currentSplice.find(substring, currentIndex + 1)
        if(currentIndex == -1):
            break
        count += 1
        # print(currentIndex)
        # print(count)

    return count


if __name__ == '__main__':
    A = "This is an example, isn't it?."
    B = "is"
    C = "Sit here, there, or anywhere, there are many open seats."
    D = "here, there"
    print(findInstancesOfSubstring(A, B))
    print(findInstancesOfSubstring(C, D))