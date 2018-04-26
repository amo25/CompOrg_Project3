#Project 3
#Comp Org
# Alex Orlov

from collections import namedtuple  #for structs

# Start by simulating a cache with size 1K (bytes), block size 8 bytes, Direct Mapped Cache Placement Type, Write back write policy
#todo change params to simulate all 128 cache configs
cache_size = 1024  # 1K
block_size = 8  # 8
cache_placement_type = "Direct"
write_policy = "back"

CacheStruct = namedtuple("CacheStruct", "validBit Tag dirtyBit")
#For direct mapped, valid bit set to 1 when data is put in a line in the cache. Handles possible bad data at start

initialLine = CacheStruct(validBit=0, Tag=0x0000, dirtyBit=0)

#create a list of height "block_count" and width: TODO
#width, height
width = 1
#todo change width
block_count = int(cache_size / block_size)
#build the Cache, initilizeing every element with junk data (validBit == 0)
CacheMatrix = [[initialLine for x in range(width)] for y in range(block_count)]

#CacheMatrix[index][entry in that line]
print(CacheMatrix[0][0].validBit)  #todo remove
print(CacheMatrix[4][0])