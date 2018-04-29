#read data
def readAddress(the_address, the_cache_size, the_block_size, the_cache_matrix):

    #TODO this is repeated code from writeAddress. May be able to optimize in some way if slow
    #convert the_address to an int
    convertedAddress = int(the_address, 16)  #convert base 16 string to an int

    #first, calculate the stuff
    the_block_count = int(the_cache_size / the_block_size)  #needed internally

    theTag = int(convertedAddress /
                 the_cache_size)  # tag = floor(memoryAddress/cacheSize)
    theIndex = int(
        convertedAddress / the_block_size) % the_block_count  # index = floor
    #I don't think we care about block offset (which byte inside block), because we don't care about the actual data. Could be wrong TODO

    #print("Read valid bit: ", the_cache_matrix[theIndex][0].validBit)

    if ((the_cache_matrix[theIndex][0].validBit == 1)
            and (the_cache_matrix[theIndex][0].Tag == theTag)):
        address_hit = True
    #if we have a miss, we need to update cache so that it gets the data. In this case, just set valid bit to 1 and tag to the Tag
    else:
        address_hit = False
        the_cache_matrix[theIndex][0].validBit = 1
        the_cache_matrix[theIndex][0].Tag = theTag

    return address_hit