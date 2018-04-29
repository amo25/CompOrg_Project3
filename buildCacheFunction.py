def buildCache(cache_size, block_size, cache_placement_type, write_policy):

    #For direct mapped, valid bit set to 1 when data is put in a line in the cache. Handles possible bad data at start

    #initialLine = CacheStruct(validBit=0, Tag=0x0000, dirtyBit=0)

    #create a list of height "block_count" and width: TODO
    #width, height
    width = 1
    #todo change width
    block_count = int(cache_size / block_size)
    #build the Cache, initializing every element with junk data (validBit == 0)
    CacheMatrix = [[CacheClass() for x in range(width)]
                   for y in range(block_count)]

    return CacheMatrix