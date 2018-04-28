#Project 3
#Comp Org
# Alex Orlov

from collections import namedtuple  #for structs

# Start by simulating a cache with size 1K (bytes), block size 8 bytes, Direct Mapped Cache Placement Type, Write back write policy
#todo change params to simulate all 128 cache configs
cache_size = 1024  # 1K
block_size = 8  # 8
cache_placement_type = "Direct"
write_policy = "WB"


#named tuples are immutable. Use a class instead
class CacheClass:
    validBit = 0
    Tag = 0x0000
    dirtyBit = 0


#CacheStruct = namedtuple("CacheStruct", "validBit Tag dirtyBit")
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

#CacheMatrix[index][entry in that line]
"""print(CacheMatrix[0][0].validBit)  #todo remove
print(CacheMatrix[4][0])"""


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


#read data
def readAddressHit(the_address, the_cache_size, the_block_size,
                   the_cache_matrix):

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


"""print("Original	", "ValidBit: ", CacheMatrix[0][0].validBit, " Tag: ", CacheMatrix[0][0].Tag)"""
"""addressHit = readAddressHit("04000000", cache_size, block_size, CacheMatrix)	#expect miss
if (addressHit):
	print("Original Address Hit")
else:
	print("Original Address Miss")"""

#CacheMatrix = writeAddress("04000000", cache_size, block_size, CacheMatrix)
#print("Updated	", "ValidBit: ", CacheMatrix[0][0].validBit, " Tag: ", CacheMatrix[0][0].Tag)

#track num reads and num hits. Track hit rate via
#hitRate = numHits/numReads.
numReads = 0
numHits = 0
#todo parse all the files in the folder? Or just "test.trace"?
#parse the file
file = open("test1.trace", "r")

#store results
wFile = open("myTest1.result", "w+")

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
        addressHit = readAddressHit(address, cache_size, block_size,
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
wFile.write("Hit Rate: %.2f\n" % hitRate)
