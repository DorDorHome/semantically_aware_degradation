import cv2
import cv2 as cv
import glob
import os
import numpy as np

"""## 1. Curve Adjustment"""


def main():
    print('running main()')
    destination_path = '/home/cihe/Shroud/dataset/test/'
    # target_path = './results/'
    #
    images = glob.glob(f'{destination_path}*.png')
    target_path = './test/'


    print(images)
    for image in images:
        img = cv.imread(image)
        p = img.copy()

        #file path and name to write
        outfile = target_path + os.path.basename(str(image))
        status = cv.imwrite(outfile, p)
        #check if write successful
        # print(status)


if __name__ == '__main__':
    main()