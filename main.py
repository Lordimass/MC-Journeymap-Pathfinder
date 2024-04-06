import anvil
import os
import numpy as np
import PIL.Image as PILage

import osFunctions.py

REGIONS_DIRECTORY = "test"

# Check whether REGIONS_DIRECTORY exists, if not create it and prompt user to upload files
osFunctions(REGIONS_DIRECTORY, fail_response = "No regions directory found, please upload your .mca files to the '{REGIONS_DIRECTORY}' directory, then restart the program.")

# Removes additional syntax from the file name of a region, returning a tuple of values
def get_region_coords_from_file_name(filename):
    regionCoordinates = filename.rstrip(".mca").lstrip("r.").split(".")

    for coordinate in [0,1]:
        regionCoordinates[coordinate] = int(regionCoordinates[coordinate])
    
    return tuple(regionCoordinates)

# Converting region relative coordinates to real chunk coodinates
def realise_chunk(region_coordinates, relative_coordinates):
    M = 10000
    region_coordinates = [region_coordinates[0] + M, region_coordinates[1] + M]
    zero_point = [region_coordinates[0] * 32, region_coordinates[1] * 32]
    coordinate = [zero_point[0] + relative_coordinates[0], zero_point[1] + relative_coordinates[1]]
    coordinate = [coordinate[0] - (M*32), coordinate[1] - (M*32)]
    return coordinate

# Creating suitably sized array of Tuples which can be later converted to an image
regionFileNames = []
xRange = [0,0]
zRange = [0,0]
for regionFileName in os.listdir("region"):
    regionFileNames.append(regionFileName)
    regionCoordinates = get_region_coords_from_file_name(regionFileName)

    if regionCoordinates[0] < xRange[0]: # Finding minX
        xRange[0] = regionCoordinates[0]
    if regionCoordinates[1] > xRange[1]: # Finding maxX
        xRange[1] = regionCoordinates[1]

    if regionCoordinates[0] < zRange[0]: # Finding minZ
        zRange[0] = regionCoordinates[0]
    if regionCoordinates[1] > zRange[1]: # Finding maxZ
        zRange[1] = regionCoordinates[1]

xRangeMagnitude = xRange[1] - xRange[0] # Calculating the magnitude of the range of possible values 
zRangeMagnitude = zRange[1] - zRange[0] # Determines the size of the image

chunkData = np.zeros((32*xRangeMagnitude,32*zRangeMagnitude, 3), dtype=np.uint8)

# Reading Data From Region
for regionFileName in regionFileNames:
    print(f"Scanning region {regionFileName}")
    regionFilePath = REGIONS_DIRECTORY + "/" + regionFileName
    region = anvil.Region.from_file(regionFilePath)
    regionCoordinates = get_region_coords_from_file_name(regionFileName)
    for relChunkX in range(0,32):
        for relChunkZ in range(0,32):
            try:
                chunk = region.get_chunk(relChunkX, relChunkZ)
            except:
                chunk = None

            realChunkCoord = realise_chunk(regionCoordinates, [relChunkX, relChunkZ])
            if chunk != None:    
                chunkData[
                    realChunkCoord[0] - xRange[0]*32,
                    realChunkCoord[1] - zRange[0]*32
                    ] = [255,0,0]

# Converting data to an image

img = PILage.fromarray(chunkData, mode="RGB")
img.show()
img.save("output.png")
