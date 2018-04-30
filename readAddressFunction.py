#read data

import random


def readAddress(the_address, the_cache_size, the_block_size, the_cache_matrix,
                the_cache_placement_type):

    #TODO this is repeated code from writeAddress. May be able to optimize in some way if slow
    #convert the_address to an int
    convertedAddress = int(the_address, 16)  #convert base 16 string to an int

    #first, calculate the stuff
    the_block_count = int(the_cache_size / the_block_size)  #needed internally
    num_elements = int(the_block_count)  #needed for FA. Janky I know

    #modify the_block_count based on cache_placement_type
    if (the_cache_placement_type == "2W"):
        width = 2
    elif (the_cache_placement_type == "4W"):
        width = 4
    elif (the_cache_placement_type == "FA"):
        width = num_elements
    else:
        width = 1
    #else the block count stays the same

    the_block_count = int(the_block_count / width)

    theTag = int(convertedAddress /
                 the_cache_size)  # tag = floor(memoryAddress/cacheSize)
    theIndex = int(
        convertedAddress / the_block_size) % the_block_count  # index = floor
    #I don't think we care about block offset (which byte inside block), because we don't care about the actual data. Could be wrong TODO

    width = int(width)
    theIndex = int(theIndex)
    #Now, loop through all possible places
    for i in range(width):
        if ((the_cache_matrix[theIndex][i].validBit == 1)
                and (the_cache_matrix[theIndex][i].Tag == theTag)):
            return True  #if we get something, it's a hit!

    #if we don't get a hit, we need to update cache so that it gets the data. In this case, just set valid bit to 1 and tag to the Tag
    #choose LRU to set
    #loop through the width of the index and find the biggest priority.
    # set the line at index to the location of this priority
    max = 0
    line_at_index = 0
    for i in range(width):
        temp = the_cache_matrix[theIndex][i].priority
        if (temp > max):
            max = temp
            line_at_index = i

    #once we've picked which block we're replacing, reset it's priority to 0.
    # increment the rest of the priorities
    for i in range(width):
        if (i == line_at_index):
            the_cache_matrix[theIndex][i].priority = 0
        else:
            the_cache_matrix[theIndex][
                i].priority = the_cache_matrix[theIndex][i].priority + 1

    the_cache_matrix[theIndex][
        line_at_index].validBit = 1  #todo changed line_at_index to 0 on a whim (non random read replacement)
    the_cache_matrix[theIndex][line_at_index].Tag = theTag

    return False