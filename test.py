import anvil
import numpy as np
import PIL.Image as PILage

regionCoord = [-1, -1]
region = anvil.Region.from_file(f"region/r.{regionCoord[0]}.{regionCoord[1]}.mca")

def realise_chunk(region_coordinates, relative_coordinates):
    M = 10000
    region_coordinates = [region_coordinates[0] + M, region_coordinates[1] + M]
    zero_point = [region_coordinates[0] * 32, region_coordinates[1] * 32]
    coordinate = [zero_point[0] + relative_coordinates[0], zero_point[1] + relative_coordinates[1]]
    coordinate = [coordinate[0] - (M*32), coordinate[1] - (M*32)]
    return coordinate


data = np.zeros((32, 32, 3), dtype=np.uint8)
for relChunkX in range(0,32):
    for relChunkZ in range(0,32):
        try:
            print(region.get_chunk(relChunkX, relChunkZ))
            valid = True
        except:
            print(f"No chunk found at {realise_chunk(regionCoord, [relChunkX, relChunkZ])}, (Relative {relChunkX}, {relChunkZ})")
            valid = False

        realCoords = realise_chunk(regionCoord, [relChunkX, relChunkZ])
        if valid:
            data[realCoords[0]][realCoords[1]] = (255,0,0)

img = PILage.fromarray(data, mode="RGB")
img.show()
img.save("output.png")


