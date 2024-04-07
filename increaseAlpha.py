import numpy as np
import PIL.Image as Image

MULTIPLER = 2

def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))

image = Image.open("output.png")
image.show()
width, height = image.size
maxAlpha = 0
for x in range(width):
    for y in range(height):
        currentPixel = image.getpixel((x,y))
        currentAlpha = currentPixel[3]
        newAlpha = clamp(currentAlpha * 2, 0, 255)
        newPixel = (currentPixel[0], currentPixel[1], currentPixel[2], newAlpha)
        image.putpixel((x,y), newPixel)
image.show()
image.close()