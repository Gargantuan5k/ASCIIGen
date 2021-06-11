from PIL import Image, ImageDraw, ImageFont
from tkinter import Tk
from tkinter.filedialog import askopenfilename

import math
import sys
import time
import itertools
import threading

Tk().withdraw()

global process_done

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
    try:
        text_file = open(f"{filename}_ascii-text.txt", "w")
        width, height = im.size
        im = im.resize((int(scaleFactor * width), int(scaleFactor * height * (oneCharWidth / oneCharHeight))), Image.NEAREST).convert("RGB")
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
        return outputImage
    except KeyboardInterrupt:
        sys.exit()


def main():
    print("""
WELCOME TO THE IMAGE TO ASCII CONVERTER :)
This is a tool that will convert any image file into an ASCII art textfile. It will also display the ASCII text as
a coloured picture!\n\n
    """)


    fmethod = input("Choose method to open file, [F]Open File Explorer/[P]Enter absolute path: ").lower()

    if fmethod == "f":
        fname = askopenfilename()
    else:
        fname = input("Enter absolute path to image file: ")
    n = fname.split(".")[0]

    im = Image.open(fname)
    fnt = ImageFont.truetype('C:\\Windows\\Fonts\\lucon.ttf', 15)

    

    try:
        process_done = False

        def process_animation():
            a = sys.executable
            m = '\\'
            m = m[0]
            while True:
                b = len(a)
                c = a[(b - 1)]
                if c == m:
                    break
                a = a[:(b - 1)]
            
            if sys.executable == a + "pythonw.exe":
                print("Processing image ...")
            else:            
                for c in itertools.cycle(['|', '/', '-', '\\']):
                    if process_done:
                        break
                    else:
                        sys.stdout.write('\rProcessing ' + c)
                        try:
                            sys.stdout.flush()
                        except KeyboardInterrupt:
                            sys.exit()
                        time.sleep(0.1)

                sys.stdout.flush()
                sys.stdout.write("\rFinished processing!\n")


        thread = threading.Thread(target=process_animation)
        thread.start()

        outputImage = process_img(im, n, fnt)
        process_done = True
        outputImage.save(f"{n}_ascii-converted.jpg")

        outputImage.show()

        time.sleep(1)

        print(f"Converted image saved in {n}_ascii-converted.jpg")
        print(f"ASCII text file saved in {n}_ascii-text.txt")

    except ValueError:
        print("Your file returned a ValueError. This means it is either not an image, is corrupted or is not supported by this tool :(")


if __name__ == "__main__":
    main()
