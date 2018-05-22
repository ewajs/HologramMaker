from PIL import Image
import numpy as np
from shapely.geometry import Point
from shapely.geometry import Polygon
from tkinter import filedialog, Entry, Button, Label, StringVar, Tk, DISABLED, NORMAL
from time import sleep

def openFile():
    string_file.set(filedialog.askopenfilename(initialdir="./"))

def convertImage(file, width, height):
    sleep(0.5)
    SCREEN_WIDTH = int(width)
    SCREEN_HEIGHT = int(height) 
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

window = Tk()
window.title("HologramMaker")
window.geometry('450x150')
string_file = StringVar()
file_txt = Entry(window, width=60, textvariable=string_file)
file_txt.pack()
open_btn = Button(window, text="Abrir...", command=openFile)
open_btn.pack() #grid(column=1,row=0)
width_lbl = Label(window, text="Ancho:")
width_lbl.pack() #grid(column=0, row=1)
width_val = StringVar(value="1920")
width_txt = Entry(window,width=5,textvariable=width_val)
width_txt.pack()#grid(column=1, row=1)
height_lbl = Label(window, text="Alto:")
height_lbl.pack() #grid(column=0, row=1)
height_val = StringVar(value="1080")
height_txt = Entry(window,width=5,textvariable=height_val)
height_txt.pack()#grid(column=1, row=1)
convert_btn = Button(window, text="Convertir", command=lambda: convertImage(string_file.get(),width_txt.get(), height_txt.get()))
convert_btn.pack()
window.mainloop()


#img = input("File name: ")
#convertImage(img)