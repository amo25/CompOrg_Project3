#write data
def writeAddress(the_address, the_cache_size, the_block_size,
                 the_cache_matrix):

    #convert the_address to an int
    convertedAddress = int(the_address, 16)  #convert base 16 string to an int

    #first, calculate the stuff
    the_block_count = int(the_cache_size / the_block_size)  #needed internally

    theTag = int(convertedAddress /
                 the_cache_size)  # tag = floor(memoryAddress/cacheSize)
    theIndex = int(
        convertedAddress / the_block_size) % the_block_count  # index = floor
    #I don't think we care about block offset (which byte inside block), because we don't care about the actual data. Could be wrong TODO

    #next, update the tag and valid bit at a specified index. TODO add in dirtyBit modification based on write policy.
    #TODO change [0] to a specified entry for 2W, 4W, FA
    if ((the_cache_matrix[theIndex][0].validBit == 1)
            and (the_cache_matrix[theIndex][0].Tag == theTag)):
        address_hit = True
    else:
        address_hit = False
        the_cache_matrix[theIndex][0].validBit = 1
        the_cache_matrix[theIndex][0].Tag = theTag

    return (
        the_cache_matrix, address_hit
    )  #finally, return the cache matrix. We can optimize this later, if pass by reference is available in python. TODO if too slow