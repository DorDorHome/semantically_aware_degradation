import cv2 as cv  # import the OpenCV package. cv2 denotes the OpenCV package
# we will use the package to read, and display images.
import numpy as np  # import Python maths lib. Numpy& name its np
from pathlib import Path  #import Path lib. to manage files

def skin_tone_eye(eye_list, image):


  l_eye = cv.imread(str(Path(eye_list[0])))
  r_eye = cv.imread(str(Path(eye_list[1])))
  #grayscale r_eye and l_eye
  r_eye = cv.cvtColor(r_eye, cv.COLOR_BGR2GRAY)
  l_eye = cv.cvtColor(l_eye, cv.COLOR_BGR2GRAY)


  #Use r_mask to find (max (bottom right eye) + 10 px) to sample
  rows = r_eye.shape[0]
  cols = r_eye.shape[1]
  j_max = 0
  i_max = 0
  for i in range(0, cols):
      for j in range(0, rows):
              if r_eye[i][j] == 255:
                if i > j_max:
                  i_max = i
                  j_max = j

# average color in 3 pixel radius from color image in prev area
  count = 0
  color_sum = [0,0,0]
  for i in range(i_max - 3, i_max + 3):
    for j in range(j_max - 3, j_max +3):
      count += 1
      color_sum += image[i_max + 20][j_max][:]
  color_avg = color_sum/count

  #combine r_eye & l_eye mask
  rows = r_eye.shape[0]
  cols = r_eye.shape[1]
  for x in range(0, rows):
      for y in range(0, cols):
        if r_eye[x][y] == 255:
          l_eye[x][y] = 255


#find contours of ask to add thick outline to eyes
  # from https://stackoverflow.com/questions/58530261/how-to-create-an-outline-with-controllable-thickness-from-a-mask-segmentation
  cnts = cv.findContours(l_eye, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)  #find contours
  mask = np.zeros(l_eye.shape, dtype=np.uint8)  #mask empty image

  cnts = cnts[0] if len(cnts) == 2 else cnts[1]
  for c in cnts:
    # draw white contours around eye mask with thickness 10
      cv.drawContours(mask, [c], -1, (255, 255, 255), thickness=10)

  rows = l_eye.shape[0]
  cols = l_eye.shape[1]
  for x in range(0, rows):
      for y in range(0, cols):
        if mask[x][y] == 255:
          image[x][y] = 0 # add mask to original image but in black

  #apply skin-tone colored mask to original
  # rows = l_eye.shape[0]
  # cols = l_eye.shape[1]
  for x in range(0, rows):
      for y in range(0, cols):
        if l_eye[x][y] == 255:
          image[x][y] = color_avg

  return image