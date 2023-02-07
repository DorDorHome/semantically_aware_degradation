import os

import cv2
import numpy as np
from PIL import Image
from pathlib import Path
import glob

# Read the two images

trainA = '/home/cihe/Shroud/dataset/train/trainA/'
trainB = '/home/cihe/Shroud/dataset/train/trainB/'
target_path = '/home/cihe/Shroud/dataset/train/train/'


# images = glob.glob(f'{destination_path}*.png')

# images = glob.glob(f'{folder_path}*.png')
#
# print(images)
# for image in images:
#     print(image)


def iterate(folder_path, folder_path2):
    files1 = Path(folder_path).glob('*')
    files2 = Path(folder_path2).glob('*')
    for fhs in zip(sorted(files1), sorted(files2)):
        yield fhs


for fh1, fh2 in iterate(trainA, trainB):
    print(f"file1 {fh1} file2 {fh2}")
    img1 = cv2.imread(str(fh1))
    img2 = cv2.imread(str(fh2))
    image = np.concatenate((img1, img2), axis=1)
    outfile = target_path + os.path.basename(str(fh1))
    status = cv2.imwrite(outfile, image)
