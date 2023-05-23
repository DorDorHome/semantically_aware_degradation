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

def create_tone_curve_points(rough_low_cut_off , rough_high_cut_off = 255, sigma_input = 5, num_points =2, rough_max_output = 255, rough_min_output = 0 , sigma_output = 5 ):
    '''
    Create two sets of points, both in ascending order, to be used to create tone curve (in one channel)
    
    by creating random number between 0 and 255, to map to another 

    num_point: the number of points to be plotted. At least two should be entered.
    
    The remaining arguments can be divided into two parts:

    input image arguments:
        rough_low_cut_off: the value below which would be mapped to zero.
        rough_high_cut_off: the value above which would be mapped to max
        sigma_input: the uncertainty term applied to the input rough_cut_off and rough_blow_up_point
    output image arguments:
        rough_min_output: 
        rough_max_output: 
        sigma_output: the uncertainty term applied to the rough_max_output and rough_min_output

    '''

    # making sure the number of point is at least two:
    assert num_points >= 2, 'At least 2 number of points should be used to plot a tone curve.'



    assert rough_low_cut_off < rough_high_cut_off, "blow up point should be higher than cut off point"
    # generate the low cut off and the blow_up_point with sigma_input
    high_cut_off = None 
    # making sure the generated high_cut_off is larger than low_cut_off
    while high_cut_off == None or (low_cut_off > high_cut_off):
        low_cut_off = max(0, np.random.normal(loc= rough_low_cut_off, scale= sigma_input, size= None))
        high_cut_off = min(255, np.random.normal(loc = rough_high_cut_off, scale= sigma_input, size = None))
        

    assert rough_max_output > rough_min_output, "max ouput should be higher than min output. "
    max_output = None
    while max_output == None or (min_output > max_output):
        # generate the max and min output:
        min_output = max(0, np.random.normal(loc = rough_min_output, scale = sigma_output, size = None))
        max_output = min(255, np.random.normal(loc = rough_max_output, scale = sigma_output, size = None))

    if num_points == 2:

      input_points_list = [low_cut_off, high_cut_off]
      output_points_list = [min_output, max_output]
  
    else:
      input_points_list = np.sort(np.random.uniform(low= low_cut_off, high= high_cut_off, size= num_points -2))
      output_points_list = np.sort(np.random.uniform(low = min_output, high = max_output, size = num_points-2 ))
      # print('before appending end points:', input_points_list, output_points_list)

      # appending the end points to each list:
      input_points_list = np.append(np.append(low_cut_off, input_points_list), high_cut_off)
      output_points_list = np.append(np.append(min_output, output_points_list ), max_output)
      

    return input_points_list, output_points_list

def apply_tone_curve(image, input_points, output_points):
    # Create a lookup table using the input and output points for the tone curve
    lookup_table = np.zeros(256, dtype=np.uint8)
    # print('input points', input_points)
    # print('output points, ',output_points)
    lookup_table[0:int(input_points[0])] = int(output_points[0])
    for i in range(len(input_points) - 1):
        start_input = int(input_points[i])
        end_input = int(input_points[i + 1])
        start_output = int(output_points[i])
        end_output = int(output_points[i + 1])
        lookup_table[start_input:end_input +1] = np.linspace(start_output, end_output, end_input - start_input+1)

    lookup_table[int(input_points[len(input_points)-1]):] = int(output_points[len(input_points)-1])

        # Linear interpolation between input and output points

    # print('lookup table is', lookup_table)
    print('size of the lookup table:', lookup_table.shape)
    # Apply the tone curve to each channel of the image

    tone_curved_image = cv.LUT(image, lookup_table )

    return tone_curved_image

def apply_tone_curve_optimized(image, input_points, output_points):
    # Create the lookup table using input and output points
    lookup_table = np.interp(np.arange(256), input_points, output_points)
    lookup_table = np.round(lookup_table).astype(np.uint8)
    image= image.astype(np.uint8)
    # print('size of the lookup table:', lookup_table.shape)

    # print('lookup table dtype:', lookup_table.dtype)

    # Apply the tone curve to each channel of the image
    tone_curved_image = cv.LUT(image, lookup_table)

    return tone_curved_image

# def apply_tone_curve_optimized(image, input_points, output_points):
#     # Create the lookup table using input and output points
#     lookup_table = np.interp(np.arange(256), input_points, output_points)
#     lookup_table = np.round(lookup_table).astype(np.uint8)
#     print('size of the lookup table:', lookup_table.shape)

#     print('lookup table dtype:', lookup_table.dtype)
#     image= image.astype(np.uint8)
#     # Apply the tone curve to each channel of the image
#     tone_curved_image = np.zeros_like(image)
#     for i in range(image.shape[2]):
#         tone_curved_image[:, :, i] = cv.LUT(image[:, :, i], lookup_table)

#     return tone_curved_image

def preprocessing_randomized(image, rough_low_cut_off = 170, rough_high_cut_off = 240,
                              sigma_input = 6, num_points = 7,
                                rough_max_output = 250, rough_min_output = 5,
                                sigma_output = 20, noise_level_low_bound = 0.3,
                                noise_level_upper_bound = 2, blur_level = 25):
    input_points_list, output_points_list = create_tone_curve_points(rough_low_cut_off = rough_low_cut_off, 
                                                                     rough_high_cut_off = rough_high_cut_off ,
                                                                       sigma_input = sigma_input, num_points = num_points, 
                                                                       rough_max_output = rough_max_output, rough_min_output = rough_min_output, 
                                                                       sigma_output = sigma_output)
    
    # tone_curved_image = apply_tone_curve(image, input_points_list, output_points_list)
    tone_curved_image =  apply_tone_curve_optimized(image, input_points_list, output_points_list)

    noise_level = np.random.uniform(noise_level_low_bound, noise_level_upper_bound)
    gauss = noise_level*np.random.randn(*image.shape)
    gauss = np.uint8(gauss)
    # adding noise to the tone curve adjusted image:
    # tone_curved_image = cv.GaussianBlur(tone_curved_image, (blur_level, blur_level), 0)
    tone_curved_image += gauss

    # desaturate the tone curve adjusted image:
    grey_image = cv.cvtColor(tone_curved_image, cv.COLOR_BGR2GRAY)

      # adding blur after noise. 
    grey_image = cv.GaussianBlur(grey_image, (blur_level, blur_level), 0)

    return grey_image


