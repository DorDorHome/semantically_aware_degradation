import cv2 as cv # import the OpenCV package. cv2 denotes the OpenCV package
# we will use the package to read, and display images.
from pathlib import Path  #import Path lib. to manage files


#background removal

def bg_remove(mask_list, original_image):
  bg = cv.imread(str(Path(mask_list[0])))
  bg = cv.cvtColor(bg, cv.COLOR_BGR2GRAY) # mask image still has 3 channels despite being Black and white

  for i in range(1, len(mask_list)):
    add = cv.imread(str(Path(mask_list[i]))) #read image from masks
    add = cv.cvtColor(add, cv.COLOR_BGR2GRAY) #convert to 1 channel
    rows = bg.shape[0]
    cols = bg.shape[1]
    for x in range(0, rows):
        for y in range(0, cols):
          if add[x][y] == 255:
            bg[x][y] = 255 #add mask images to previous mask image

  for x in range(0, rows):
          for y in range(0, cols):
            if bg[x][y] == 0: #using cumulative mask image
              original_image[x][y] = 0  #change background pixels to black

  return original_image


