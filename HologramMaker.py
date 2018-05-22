from PIL import Image
import numpy as np
from shapely.geometry import Point
from shapely.geometry import Polygon
 
def convertImage(file):    
    SCREEN_WIDTH = 1080
    SCREEN_HEIGHT = 1920 
    SCREEN_SQUARE = SCREEN_WIDTH
    SCREEN_MODE = 0 # Horizontal
    SCREEN_LEFTOVERX = 0
    SCREEN_LEFTOVERY = int((SCREEN_HEIGHT - SCREEN_SQUARE)/2)
    if (SCREEN_HEIGHT < SCREEN_WIDTH):
        SCREEN_SQUARE = SCREEN_HEIGHT
        SCREEN_MODE = 1 #Vertical
        SCREEN_LEFTOVERX = int((SCREEN_WIDTH - SCREEN_SQUARE)/2)
        SCREEN_LEFTOVERY = 0

    size = int(SCREEN_SQUARE*0.4)
    gutter = int(SCREEN_SQUARE*0.3)
    center = int(SCREEN_SQUARE*0.2)
    crop = int((size - center)/2)

    bg = Image.new("RGBA", (SCREEN_WIDTH, SCREEN_HEIGHT))
    im = Image.open(file).convert("RGBA")
    im1 = im.resize((size, size))
    pixels = np.array(im1)
    im_copy = np.array(im1)

    region1 = Polygon([(size-crop,-1), (size,-1), (size,crop),(size-crop, crop)])
    for index, pixel in np.ndenumerate(pixels):
        # Unpack the index.
        row, col, channel = index
        # We only need to look at spatial pixel data for one of the four channels.
        if channel != 0:
            continue
        point = Point(row, col)
        if (region1.contains(point)):# or region2.contains(point)):
            im_copy[(row, col, 0)] = 255
            im_copy[(row, col, 1)] = 255
            im_copy[(row, col, 2)] = 255
            im_copy[(row, col, 3)] = 0
    im1 = Image.fromarray(im_copy)
    startx = gutter + SCREEN_LEFTOVERX
    starty = 0 + SCREEN_LEFTOVERY
    bg.paste(im1, (startx, starty, startx+size, starty+size))
    im2 = im1.rotate(-90)
    startx = size + center + SCREEN_LEFTOVERX
    starty = gutter + SCREEN_LEFTOVERY
    bg.paste(im2, (startx, starty, startx+size, starty+size), im2)
    im3 = im1.transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.FLIP_LEFT_RIGHT)
    startx = gutter + SCREEN_LEFTOVERX
    starty = size + center + SCREEN_LEFTOVERY
    bg.paste(im3, (startx, starty, startx+size, starty+size), im3)
    im4 = im2.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.FLIP_TOP_BOTTOM)
    startx = 0 + SCREEN_LEFTOVERX
    starty = gutter + SCREEN_LEFTOVERY
    bg.paste(im4, (startx, starty, startx+size, starty+size), im4)
    bg.save("output.png", "PNG")


img = input("File name: ")
convertImage(img)