#write data

import random


def writeAddress(the_address, the_cache_size, the_block_size, the_cache_matrix,
                 the_cache_placement_type, the_bcache2mem, the_write_policy):

    #convert the_address to an int
    convertedAddress = int(the_address, 16)  #convert base 16 string to an int

    #first, calculate the stuff
    the_block_count = int(the_cache_size / the_block_size)  #needed internally
    num_elements = the_block_count  #needed for FA. Janky I know

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

    blocks_per_way = the_block_count / width
    bytes_per_way = the_cache_size / width

    theTag = int(convertedAddress /
                 bytes_per_way)  # tag = floor(memoryAddress/#bytes per way)
    theIndex = int(
        convertedAddress / the_block_size
    ) % blocks_per_way  # index = floor(address/#bytes per block) % #blocks per way
    theIndex = int(theIndex)
    #I don't think we care about block offset (which byte inside block), because we don't care about the actual data. Could be wrong TODO

    #LOOP THROUGH AND CHECK IF WE GET A HIT! IF NOT, USE LRU!
    for i in range(width):
        if ((the_cache_matrix[theIndex][i].validBit == 1)
                and (the_cache_matrix[theIndex][i].Tag == theTag)):

            address_hit = True
            the_cache_matrix[theIndex][i].validBit = 1
            the_cache_matrix[theIndex][i].Tag = theTag
            # TODO add in dirtyBit modification based on write policy.
            the_cache_matrix[theIndex][
                i].dirtyBit = 1  # any time you write, set dirty bit to 1
            return (the_cache_matrix, address_hit, the_bcache2mem)

    #IF WE MISS, USE LRU
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

    line_at_index = int(line_at_index)  #TODO MODIFY THIS

    #on write miss, send block to memory if we're doing WB method
    if (the_write_policy == "WB"
            and the_cache_matrix[theIndex][line_at_index].dirtyBit == 1):
        the_bcache2mem = the_bcache2mem + the_block_size

    #any time you write, set dirty bit to 1
    the_cache_matrix[theIndex][line_at_index].dirtyBit = 1
    address_hit = False
    the_cache_matrix[theIndex][line_at_index].validBit = 1
    the_cache_matrix[theIndex][line_at_index].Tag = theTag

    return (
        the_cache_matrix, address_hit, the_bcache2mem
    )  #finally, return the cache matrix. We can optimize this later, if pass by reference is available in python. TODO if too slow