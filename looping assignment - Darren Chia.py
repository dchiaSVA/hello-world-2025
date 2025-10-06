# import required modules
from tkinter import *
from PIL import Image, ImageDraw, ImageTk

if not hasattr(Image, "Resampling"):  # Pillow<9.0
    Image.Resampling = Image
from random import randint

import seaborn as sns  # install seaborn for color palettes (https://seaborn.pydata.org/installing.html)
from math import sin, cos, pi

palette = list(reversed(sns.color_palette("magma_r", 16).as_hex()))
# palette = list(sns.color_palette("Spectral", 16).as_hex())
#palette = list(sns.color_palette("ocean", 16).as_hex())
# palette = list(sns.color_palette("Purples", 16).as_hex())
# palette = list(sns.color_palette("Purples_r", 16).as_hex())
# palette = list(sns.color_palette("hls", 16).as_hex())
#palette = list(sns.color_palette("mako", 16).as_hex())
# palette = list(sns.color_palette("viridis", 16).as_hex())
# palette = list(sns.color_palette("cubehelix", 16).as_hex())
# palette = list(sns.color_palette("coolwarm", 16).as_hex())
#palette = list(sns.color_palette("twilight", 16).as_hex())
# palette = list(sns.color_palette("Greys", 16).as_hex())

# convert hex to rgb
get_rgb = lambda x: list(int(x[i : i + 2], 16) for i in (0, 2, 4))
new_palette = [elem.replace("#", "") for elem in palette]
rgb_palette = list(map(get_rgb, new_palette))


scaleFactor = 4
appWidth = 1000
appHeight = 600
width = int(1000/ 16)
height = int(600 / 9)

app = Tk()
app.geometry("1000x600")

canvas = Canvas(app, bg=palette[2])
canvas.pack(fill=BOTH, expand=1)

myImage = Image.new(
    "RGB",
    (appWidth * scaleFactor, appHeight * scaleFactor),
    color="black",
)
# next create a drawing context
drawingContext = ImageDraw.Draw(
    myImage, "RGBA"
)  # specify that you will use the alpha channel


# create function so we can draw circles in a loop
def drawCircle(x, y, radius, color, outline_color):
    # draw with an outline color and thickness
    drawingContext.ellipse(
        (x, y, x + radius, y + radius),
        fill=color,
        outline=outline_color,
        width=1, #randint(1, 20),
    )

def drawMultipleCircles(x, y, radius, number):
    # an example of drawing things in a circle, but you can modify x,y in any way you want
    angle = pi * 2 / number
    for i in range(number):
        if (i % 2) == 0:
             alpha = 150
        else:
             alpha = 75
        outline_alpha = 255
        new_x = sin(angle * i) * radius / 2 + x  # x + (i * 20)
        new_y = cos(angle * i) * radius / 2 + y  # y + (i * 20)
        drawCircle(
            new_x,
            new_y,
            radius,
            (*rgb_palette[i], alpha),
            (*rgb_palette[i], outline_alpha),
        )

def drawTriangle(x, y, size, color, outline_color):
    points = [(x, y),
        (x + size, y),
        (x + size / 2, y + size)]
    drawingContext.polygon(points, fill=color, outline=outline_color)

def drawMultipleTriangles(x, y, radius, number):
    angle = pi * 2 / number
    new_size = radius * 0.9
    for i in range(number):
        if (i % 2) == 0:
             alpha = 255
        else:
             alpha = 130
        outline_alpha = 255
        new_x = sin(angle * i) * radius / 2 + x
        new_y = cos(angle * i) * radius / 2 + y
        drawTriangle(
            new_x,
            new_y,
            new_size,
            (*rgb_palette[i], alpha),
            (*rgb_palette[i], outline_alpha),
        )


def drawRectangle(x, y, width, height, color):
    drawingContext.rectangle((x, y, x + width, y + height), fill=color, outline= None )

for i in range(int(appWidth / width)):
    for j in range(int(appHeight / height)):
        print("row: ", i, "col: ", j)
       
        if (i + j) %2 == 0:
           drawMultipleCircles(
            i * (width * scaleFactor),
            j * (height * scaleFactor),
            width * scaleFactor,
            16,
            )
        else:
              drawMultipleTriangles(
                i * (width * scaleFactor),
                j * (height * scaleFactor),
                width * scaleFactor,
                16,
            )
# resize it back to 100 so we can smooth it out, https://pillow.readthedocs.io/en/stable/handbook/concepts.html#PIL.Image.LANCZOS
myImage = myImage.resize((appWidth, appHeight), Image.Resampling.LANCZOS)
# convert the image to a Tkinter PhotoImage
myImage.save("myImage.png", bitmap_format="png")
myImage = ImageTk.PhotoImage(myImage)
# draw it to the app canvas
canvas.create_image(0, 0, image=myImage, anchor="nw")

app.mainloop()
