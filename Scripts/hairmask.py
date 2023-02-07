import cv2 as cv
import numpy as np
import cv2


def _adjust_gamma(image, gamma=3.2):
    # build a lookup table mapping the pixel values [0, 255] to
    # their adjusted gamma values
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")
    # apply gamma correction using the lookup table
    return cv2.LUT(image, table)


# hair brightening
def hair_brighten(mask_list, original_image):
    # get mask
    for mask in mask_list:
        if 'hair' in str(mask):
            hair_mask = cv.imread(str(mask))
            hair_mask_bw = cv.cvtColor(hair_mask, cv.COLOR_BGR2GRAY)
            # cv2_imshow(hair_mask)
            rows = hair_mask.shape[0]
            cols = hair_mask.shape[1]
            for x in range(0, rows):
                for y in range(0, cols):
                    # get hair mask
                    if hair_mask_bw[x][y] > 0:
                        # fill mask with orignal color
                        hair_mask[x][y] = original_image[x][y]
            # get average brightness of hair
            lab = cv2.cvtColor(hair_mask, cv2.COLOR_BGR2LAB)
            avg_lightness = np.mean(lab[:, :, 0])
            # if over 50, brighten
            if avg_lightness <= 50:
                #the lower the average brigthness, the greater the gamma increase
                gamma = -.128 * (avg_lightness) + 6.4
                # brighten hair
                hair_mask = _adjust_gamma(hair_mask, gamma)
            # apply colors to image
            for x in range(0, rows):
                for y in range(0, cols):
                    if hair_mask_bw[x][y] > 0:
                        original_image[x][y] = hair_mask[x][y]

    return original_image
