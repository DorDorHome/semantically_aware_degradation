import numpy as np

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

