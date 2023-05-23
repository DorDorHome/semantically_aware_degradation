import cv2 as cv  # import the OpenCV package. cv2 denotes the OpenCV package
# we will use the package to read, and display images.
import numpy as np  # import Python maths lib. Numpy& name its np
from pathlib import Path  #import Path lib. to manage files
import os

def skin_tone_eye(eye_list, image):


  # read the left and right eye images from the the paths in eye_list:
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



def skin_tone_eye_optimized_randomized(eye_list, face_list, image, i = None, randomize = True, thickness_lower_bound = 0, thickness_upper_bound = 10, 
                                       blur_kernel_size_lower_bound =5, blur_kernel_size_upper_bound = 15, output_directory = None):

  # step 1: load the left and right eye images from the paths:
  l_eye = cv.imread(str(Path(eye_list[0])))
  r_eye = cv.imread(str(Path(eye_list[1])))


   # step 2: combine the two masks into one
  combined_eye = np.maximum(l_eye, r_eye)

  # step 3: find optimimum values for eyes by average face values:
  if len(face_list) >=1:
    face = cv.imread(str(Path(face_list[0]))) 
    face_non_zero = (face!=0)
    average_face_value = (face_non_zero*image).sum()/face_non_zero.sum()
  else:
    average_face_value = 255
  
  #print('average face value =', average_face_value)
  
  eyelips_replacement = (combined_eye!=0)*average_face_value*1.2

  #cv.imwrite(output_directory+ '/'+ os.path.basename(str(i))+'_eyelips_replacement.jpg', eyelips_replacement)



  # step 4: remove eye by darkening it:
  image = np.minimum(255- combined_eye, image)
  #cv.imwrite(output_directory+ '/'+ os.path.basename(str(i))+'step4.jpg', image)


   # step 4: create a blurred combined_eye_mask:

  if randomize:
    blur_kernel_size = np.random.randint(blur_kernel_size_lower_bound, blur_kernel_size_upper_bound)
  else:
   blur_kernel_size = (blur_kernel_size_lower_bound + blur_kernel_size_upper_bound)/2

  eyelips_replacement_blur = cv.blur(eyelips_replacement, (blur_kernel_size, blur_kernel_size ))

  # step 4.2 use the blurred_combined_eye_mask to create a white shadow on eyelips:



  # step 5: replace it with the skin tone values:
  image = np.maximum(image, eyelips_replacement_blur)
  #cv.imwrite(output_directory+ '/'+ os.path.basename(str(i))+'step5.jpg', image)





   # step 6: create the contour mask as thick outline to eyes
  # from https://stackoverflow.com/questions/58530261/how-to-create-an-outline-with-controllable-thickness-from-a-mask-segmentation
  combined_eye_grey = cv.cvtColor(combined_eye, cv.COLOR_BGR2GRAY)
  cnts = cv.findContours(combined_eye_grey, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)  #find contours
  contour_mask = 255*np.ones(combined_eye.shape, dtype=np.uint8)  #mask empty image
  
  # whether to randomized the thickness of the contour:
  if randomize == True:
    thickness = np.random.randint(thickness_lower_bound, thickness_upper_bound)
  else:
    thickness = (thickness_lower_bound+ thickness_upper_bound)/2
  cnts = cnts[0] if len(cnts) == 2 else cnts[1]
  for c in cnts:
    # draw white contours around eye mask with thickness 
      cv.drawContours(contour_mask, [c], -1, (0, 0, 0), thickness=thickness)
  
  image = np.minimum(image, contour_mask)
  #cv.imwrite(output_directory+ '/'+ os.path.basename(str(i))+'final_step.jpg', image)


  return image







