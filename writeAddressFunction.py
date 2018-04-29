#write data

import random


def writeAddress(the_address, the_cache_size, the_block_size, the_cache_matrix,
                 the_cache_placement_type):

    #convert the_address to an int
    convertedAddress = int(the_address, 16)  #convert base 16 string to an int

    #first, calculate the stuff
    the_block_count = int(the_cache_size / the_block_size)  #needed internally
    num_elements = the_block_count  #needed for FA. Janky I know

    #modify the_block_count based on cache_placement_type
    if (the_cache_placement_type == "2W"):
        the_block_count = the_block_count / 2
    elif (the_cache_placement_type == "4W"):
        the_block_count = the_block_count / 4
    elif (the_cache_placement_type == "FA"):
        the_block_count = 1
    #else the block count stays the same

    theTag = int(convertedAddress /
                 the_cache_size)  # tag = floor(memoryAddress/cacheSize)
    theIndex = int(
        convertedAddress / the_block_size) % the_block_count  # index = floor
    #I don't think we care about block offset (which byte inside block), because we don't care about the actual data. Could be wrong TODO

    #next, update the tag and valid bit at a specified index.
    # TODO add in dirtyBit modification based on write policy.

    if (the_cache_placement_type == "2W"):
        line_at_index = random.randint(
            0, 1
        )  #change either the 0'th or 1'st line at the found index for 2Way (randomly)
    elif (the_cache_placement_type == "4W"):
        line_at_index = random.randint(0, 3)
    elif (the_cache_placement_type == "FA"):
        line_at_index = random.randint(
            0, num_elements - 1)  #todo check that this works
    else:
        line_at_index = 0

    line_at_index = int(line_at_index)
    theIndex = int(theIndex)
    if ((the_cache_matrix[theIndex][line_at_index].validBit == 1)
            and (the_cache_matrix[theIndex][line_at_index].Tag == theTag)):
        address_hit = True
    else:
        address_hit = False
        the_cache_matrix[theIndex][line_at_index].validBit = 1
        the_cache_matrix[theIndex][line_at_index].Tag = theTag

    return (
        the_cache_matrix, address_hit
    )  #finally, return the cache matrix. We can optimize this later, if pass by reference is available in python. TODO if too slow