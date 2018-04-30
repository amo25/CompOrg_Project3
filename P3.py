#Project 3
#Comp Org
# Alex Orlov

from writeAddressFunction import writeAddress
from readAddressFunction import readAddress


#named tuples are immutable. Use a class instead
class CacheClass:
    validBit = 0
    Tag = 0x0000
    dirtyBit = 0
    priority = 0  # use for LRU. The higher the priority, the more likely it will be picked.
    # for DM max will be 0, for 2W 1, for 4W 3, but for FA will be as big as the cache
    # this is the inefficiency in this scheme. Should be fine for simulation, but would
    # pose an issue in hardware for FA.


def buildCache(cache_size, block_size, cache_placement_type, write_policy):

    #For direct mapped, valid bit set to 1 when data is put in a line in the cache. Handles possible bad data at start

    #todo change width
    block_count = int(cache_size / block_size)

    #create a list of height "block_count" and width: TODO
    #width, height
    if (cache_placement_type == "DM"):
        width = 1
    elif (cache_placement_type == "2W"):
        width = 2
    elif (cache_placement_type == "4W"):
        width = 4
    elif (cache_placement_type == "FA"):
        width = block_count
    else:
        width = 1
        print("Invalid cache placement type")

    #adjust block_count as needed
    block_count = int(block_count / width)

    #build the Cache, initializing every element with junk data (validBit == 0)
    CacheMatrix = [[CacheClass() for x in range(width)]
                   for y in range(block_count)]

    return CacheMatrix


cache_size_list = [1024, 4096, 65536,
                   131072]  #1K, 4K, 64K, 128K TODO add 1024 back in
cache_placement_type_list = ["DM", "2W", "4W",
                             "FA"]  # TODO add back "DM", "2W", "4W",
block_size_list = [8, 16, 32, 128]
write_policy = "WB"

wFile = open("myTest3.result",
             "w+")  #overwrite original result. TODO change name
wFile.close()

for cache_size in cache_size_list:
    for block_size in block_size_list:
        for cache_placement_type in cache_placement_type_list:
            CacheMatrix = buildCache(cache_size, block_size,
                                     cache_placement_type, write_policy)

            #track num reads and num hits. Track hit rate via
            #hitRate = numHits/numReads.
            numReads = 0
            numHits = 0
            #todo parse all the files in the folder? Or just "test.trace"?
            #parse the file
            file = open("test3.trace", "r")  #todo change name

            #store results
            wFile = open(
                "myTest3.result",
                "a+")  #todo open these before loop? Close at end of loop?

            #TODO debug
            debugFile = open("debug.txt", "w+")

            #read the file line by line
            file1 = file.readlines()
            for x in file1:

                #debugFile.write(cache_placement_type)
                numReads = numReads + 1  #todo change name
                #print(x)
                #if the line starts with "r" (read), read function
                if (x[0] == "r"):
                    address = x[7:15]
                    addressHit = readAddress(address, cache_size, block_size,
                                             CacheMatrix, cache_placement_type)

                    #todo counter
                    if (addressHit):
                        numHits = numHits + 1
                        hitString = "hit"  #debug
                    else:
                        hitString = "miss"  #debug

                    #debug
                    convertedAddress = int(address, 16)
                    the_block_count = int(cache_size / block_size)
                    theTag = int(convertedAddress / cache_size)
                    theIndex = int(
                        convertedAddress / block_size) % the_block_count
                    debugString = "Read.	address: 0x" + address + "	Tag: " + str(
                        theTag) + "	" + hitString + "\n"
                    debugFile.write(debugString)

                elif (x[0] == "w"):
                    address = x[8:16]
                    (CacheMatrix, addressHit) = writeAddress(
                        address, cache_size, block_size, CacheMatrix,
                        cache_placement_type)
                    if (addressHit):
                        numHits = numHits + 1
                        hitString = "hit"  #debug
                    else:
                        hitString = "miss"  #debug

                    #debug
                    convertedAddress = int(address, 16)
                    the_block_count = int(cache_size / block_size)
                    theTag = int(convertedAddress / cache_size)
                    theIndex = int(
                        convertedAddress / block_size) % the_block_count
                    debugString = "Write.	address: 0x" + address + "	Tag: " + str(
                        theTag) + "	" + hitString + "\n"
                    debugFile.write(debugString)

            hitRate = numHits / numReads
            wFile.write("%d %d %s %s %.2f\n" %
                        (cache_size, block_size, cache_placement_type,
                         write_policy, hitRate))
