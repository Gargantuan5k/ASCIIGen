from PIL import Image, ImageDraw, ImageFont
from tkinter import Tk
from tkinter.filedialog import askopenfilename

import math

Tk().withdraw()

chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "[::-1]
charArray = list(chars)
charLength = len(charArray)
interval = charLength / 256

scaleFactor = 0.2
oneCharWidth = 10
oneCharHeight = 18


def getChar(inputInt):
    return charArray[math.floor(inputInt * interval)]


def process_img(im, filename, font_face):
    text_file = open(f"{filename}_ascii-text.txt", "w")
    width, height = im.size
    im = im.resize((int(scaleFactor * width), int(scaleFactor * height * (oneCharWidth / oneCharHeight))), Image.NEAREST)
    width, height = im.size
    pix = im.load()

    outputImage = Image.new('RGB', (oneCharWidth * width, oneCharHeight * height), color=(0, 0, 0))
    d = ImageDraw.Draw(outputImage)

    for i in range(height):
        for j in range(width):
            r, g, b = pix[j, i]
            h = int(r / 3 + g / 3 + b / 3)
            pix[j, i] = (h, h, h)
            text_file.write(getChar(h))
            d.text((j * oneCharWidth, i * oneCharHeight), getChar(h), font=font_face, fill=(r, g, b))

        text_file.write('\n')
    return outputImage, True


def main():
    fmethod = input("Choose method to open file, [F]File Explorer/[P]Enter absolute path. PNG IMAGES ARE NOT SUPPORTED: ").lower()
    if fmethod == "f":
        fname = askopenfilename()
    else:
        fname = input("Enter absolute path to image file: ")
    n = fname.split(".")[0]

    im = Image.open(fname)
    fnt = ImageFont.truetype('C:\\Windows\\Fonts\\lucon.ttf', 15)
    saveName = ""
    saveName = input("Enter filename to save (including extension), leave blank for default: ")

    print(f"Processing image {fname}  ...")

    outputImage, done = process_img(im, n, fnt)

    if done:
        print("Finished processing")

    outputImage.save(f"{n}_ascii-converted.jpg" if saveName == "" else saveName)
    print(f"File saved in same directory as original file.")


if __name__ == "__main__":
    main()
