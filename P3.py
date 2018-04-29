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
block_size = 8
cache_placement_type = "DM"
write_policy = "WB"

wFile = open("myTest3.result",
             "w+")  #overwrite original result. TODO change name
wFile.close()

for cache_size in cache_size_list:
    CacheMatrix = buildCache(cache_size, block_size, cache_placement_type,
                             write_policy)

    #track num reads and num hits. Track hit rate via
    #hitRate = numHits/numReads.
    numReads = 0
    numHits = 0
    #todo parse all the files in the folder? Or just "test.trace"?
    #parse the file
    file = open("test3.trace", "r")  #todo change name

    #store results
    wFile = open("myTest3.result",
                 "a+")  #todo open these before loop? Close at end of loop?

    #TODO debug
    debugFile = open("debug.txt", "w+")

    #read the file line by line
    file1 = file.readlines()
    for x in file1:

        numReads = numReads + 1  #todo change name
        #print(x)
        #if the line starts with "r" (read), read function
        if (x[0] == "r"):
            address = x[7:15]
            addressHit = readAddress(address, cache_size, block_size,
                                     CacheMatrix)

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
            theIndex = int(convertedAddress / block_size) % the_block_count
            debugString = "Read.	address: 0x" + address + "	Index: " + str(
                theIndex) + "	Tag: " + str(theTag) + "	" + hitString + "\n"
            debugFile.write(debugString)

        elif (x[0] == "w"):
            address = x[8:16]
            (CacheMatrix, addressHit) = writeAddress(address, cache_size,
                                                     block_size, CacheMatrix)
            if (addressHit):
                numHits = numHits + 1
                hitString = "hit"  #debug
            else:
                hitString = "miss"  #debug

            #debug
            convertedAddress = int(address, 16)
            the_block_count = int(cache_size / block_size)
            theTag = int(convertedAddress / cache_size)
            theIndex = int(convertedAddress / block_size) % the_block_count
            debugString = "Write.	address: 0x" + address + "	Index: " + str(
                theIndex) + "	Tag: " + str(theTag) + "	" + hitString + "\n"
            debugFile.write(debugString)

    hitRate = numHits / numReads
    wFile.write("%d %d %.2f\n" % (cache_size, block_size, hitRate))
