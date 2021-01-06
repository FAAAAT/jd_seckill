import numpy as np
import qrcode
import platform

from PIL import Image
from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol


# gray scale level values from:
# http://paulbourke.net/dataformats/asciiart/

# 70 levels of gray
gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

# 10 levels of gray
# gscale2 = '@%#*+=-:. '
white_block = '\033[0;37;47m  '
black_block = '\033[0;37;40m  '
new_line = '\033[0m\n'
# gscale2 = '█ '
gscale2 = [black_block,white_block]


def getAverageL(image,x1,x2,y1,y2):
    """
    Given PIL Image, return average value of grayscale value
    """
    # get image as numpy array
    im = np.array(image)

    cropedIm = im[x1:x2,y1:y2]

    # get shape
    w, h = cropedIm.shape

    # get average
    return np.average(cropedIm.reshape(w * h))


def covertImageToAscii(fileName, cols, scale, moreLevels):
    """
    Given Image and dims (rows, cols) returns an m*n list of Images
    """
    # declare globals
    global gscale1, gscale2

    # open image and convert to grayscale
    image = Image.open(fileName,"r").convert('L')

    code = decode(image,[ZBarSymbol.QRCODE])
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=1,
        border=4,
    )
    qr.add_data(code[0].data)
    qr.make(True)
    image = qr.make_image(fill_color="black", back_color="white")
    image.save("C:\\Users\\v-yuli4\\Desktop\\wbQR.bmp")

    # store dimensions
    W, H = image.size[0], image.size[1]
    print("input image dims: %d x %d" % (W, H))

    # compute width of tile
    w = W / cols

    # compute tile height based on aspect ratio and scale
    h = w / scale

    # compute number of rows
    rows = int(H / h)

    print("cols: %d, rows: %d" % (cols, rows))
    print("tile dims: %d x %d" % (w, h))

    # check if image size is too small
    if cols > W or rows > H:
        print("Image too small for specified cols!")
        exit(0)

        # ascii image is a list of character strings
    aimg = ""
    # generate list of dimensions
    for j in range(rows):
        y1 = int(j * h)
        y2 = int((j + 1) * h)

        # correct last tile
        if j == rows - 1:
            y2 = H

            # append an empty string
        # aimg.append("")

        for i in range(cols):

            # crop image to tile
            x1 = int(i * w)
            x2 = int((i + 1) * w)

            # correct last tile
            if i == cols - 1:
                x2 = W

                # crop image to extract tile
            # img = image.crop((x1, y1, x2, y2))

            # get average luminance
            avg = int(getAverageL(image,x1,x2,y1,y2))

            # look up ascii char
            if moreLevels:
                # gsval = gscale1[int((avg * 69) / 255)]
                gsval = gscale1[int((avg * 69) / 1)]
            else:
                # gsval = gscale2[int((avg * 1) / 255)]
                gsval = gscale2[int((avg * 1) / 1)]

                # append ascii char to string
            aimg += gsval
        aimg += new_line
            # return txt image
    return aimg
