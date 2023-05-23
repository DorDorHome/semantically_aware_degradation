import cv2 as cv # import the OpenCV package. cv2 denotes the OpenCV package
# we will use the package to read, and display images.
from pathlib import Path  #import Path lib. to manage files
import numpy as np

#background removal

def bg_remove(mask_list, original_image):
  print('path of the mask used to remove background: ', str(Path(mask_list[0])))
  bg = cv.imread(str(Path(mask_list[0])))
  bg = cv.cvtColor(bg, cv.COLOR_BGR2GRAY) # mask image still has 3 channels despite being Black and white

  # get number of rows and cols for the double loop:
  rows = bg.shape[0]
  cols = bg.shape[1]

  for i in range(1, len(mask_list)):
    add = cv.imread(str(Path(mask_list[i]))) #read image from masks
    add = cv.cvtColor(add, cv.COLOR_BGR2GRAY) #convert to 1 channel
    

    # build up the background removal mask by setting all pixels to all existing mask to be 255 
    for x in range(0, rows):
        for y in range(0, cols):
          if add[x][y] > 200:
            bg[x][y] = 255 #add mask images to previous mask image

  # setting the pixels of the original image to be zero when the corresponding pixel values 
  # of the background removal mask is zero. (i.e. not corresponding to any class)
  for x in range(0, rows):
          for y in range(0, cols):
            if bg[x][y] == 0: #using cumulative mask image
              original_image[x][y] = 0  #change background pixels to black

  return original_image


# background remmoval without double loops:

def bg_removal_optimized(mask_list, original_image):

  """
  a function to remove the background from an image.

  input:
  mask list: a list of paths, each representing the path of one of the annotated mask.
        None of these should be of the class 'background'.

  original_image: the input image whose background is to be removed:


  Output:
  an image with background removed.




  """

  # step 1: create a list of masks as a list of arrays:
  mask_array_list = []
  for i in range(0, len(mask_list)):
    add = cv.imread(str(Path(mask_list[i]))) #read image from masks
    # add = cv.cvtColor(add, cv.COLOR_BGR2GRAY)# probably no needed
    mask_array_list.append(add)
    print('type of add', type(add))
  # step 2: create a combined mask
  combined_mask = np.maximum.reduce(mask_array_list)


  # step 3: use the combined mask to remove the background from the original image:
  image = np.minimum(original_image, combined_mask)

  return image

