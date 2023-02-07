import os
import cv2 as cv
from pathlib import Path


from BG_removal import bg_remove
from eyelid_replacement import skin_tone_eye
from image_preprocessing import preprocessing


def main():
    original_image_path = Path('/home/cihe/Shroud/dataset/CelebAMask-HQ')
    mask_image_path = Path('/home/cihe/Shroud/dataset/CelebAMask-HQ')
    destination_path = '/home/cihe/Shroud/dataset/CelebAMask-HQ/Preprocessed/'

    print('running main()')
    for i in range(0, 30000):
        file_name = '**/' + str(i).zfill(5) + '_*'
        mask_list = list(mask_image_path.glob(file_name))

        full_image_name = '**/' + str(i) + '.jpg'
        original_image = cv.imread(str(Path(list(original_image_path.glob(full_image_name))[0])))
        original_image = cv.resize(original_image, (512, 512), interpolation=cv.INTER_AREA)

        #Mask
        im = bg_remove(mask_list, original_image)
        #eyes
        eyes_file_name = '**/' + str(i).zfill(5) + '*eye.png'
        eyelist = list(mask_image_path.glob(eyes_file_name))
        # print(eyelist)

        if len(eyelist) >=2:
            im = skin_tone_eye(eyelist, im)

        #hair
        hair_file_name = '**/' + str(i).zfill(5) + '*hair.png'

        im = preprocessing(im)

        outfile = destination_path + os.path.basename(str(i)) + '.jpg'
        print(outfile)
        status = cv.imwrite(outfile, im)

# def main():
#     print('running main()')
#     destination_path = '/home/cihe/Shroud/dataset/test/'
#     # target_path = './results/'
#     #
#     images = glob.glob(f'{destination_path}*.png')
#     target_path = './test/'
#
#
#     print(images)

# for image in images:
#     img = cv.imread(image)
#     p = img.copy()
#     p = preprocessing(p)
#
#     # file path and name to write
#     outfile = target_path + os.path.basename(str(image))
#     status = cv.imwrite(outfile, p)
#     # check if write successful
#     # print(status)

if __name__ == '__main__':
    main()



