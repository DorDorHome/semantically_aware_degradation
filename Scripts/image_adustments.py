import cv2 as cv
import numpy as np

"""## 1. Curve Adjustment"""


def curve_adjustment(im, cutoff):
    rows = im.shape[0]  # get image shape
    cols = im.shape[1]

    # Linear high pass filter

    for x in range(0, rows):
        for y in range(0, cols):
            # blue channel

            if im[x][y][0] <= cutoff:  # if below cutoff
                im[x][y][0] = 0  # set color to black
            else:
                # change color to step according to curve (0 at cutoff increasing linearly to 255 at 255)
                im[x][y][0] = (im[x][y][0] - cutoff) * (255 / (255 - cutoff))
            # green channel
            if im[x][y][1] <= cutoff:
                im[x][y][1] = 0
            else:
                im[x][y][1] = (im[x][y][1] - cutoff) * (255 / (255 - cutoff))
            # red channel
            red_cutoff = 160
            if im[x][y][2] <= red_cutoff:
                im[x][y][2] = 0
            else:
                # Step of each 255-160=95, 255/95 = 2.6
                im[x][y][2] = (im[x][y][2] - red_cutoff) * (255 / (255 - red_cutoff))


"""#Replace Color

"""


def color_replacement(im, threshold):
    # if blue> (1-0.697) * 255 , regardless of blue/green, change to black (0)
    rows = im.shape[0]
    cols = im.shape[1]
    threshold = (1 - threshold) * 255
    for x in range(0, rows):
        for y in range(0, cols):
            if im[x][y][0] > threshold:
                im[x][y][0] = 0
                im[x][y][1] = 0
                im[x][y][2] = 0


def add_noise(im):
    row, col, ch = im.shape  # get image shape
    gauss = np.random.randn(row, col, ch)  # random noise in shape of image
    gauss = gauss.reshape(row, col, ch)
    noisy = im + im * gauss  # add noise to image
    noisy = np.uint8(noisy)  # convert back to 8bit image for CV2
    return noisy


def preprocessing(im):
    curve_adjustment(im, 194)
    # color_replacement(im, 0.697)
    im = add_noise(im)
    # desaturate
    im = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    # gaussian blur
#TODO: Randomize Blur
    im = cv.GaussianBlur(im, (25, 25), 0)
    return im
