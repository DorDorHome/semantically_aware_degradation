import os
import cv2 as cv
from pathlib import Path

from Scripts.BG_removal import bg_remove
from Scripts.eyelid_replacement import skin_tone_eye
from Scripts.image_adustments import preprocessing
from Scripts.hairmask import hair_brighten


def main(photo_directory, mask_directory, output_directory):
    photo_directory = Path(photo_directory)
    # print('photo directory =', photo_directory)

    # print(list(photo_directory.glob('*')))
    mask_directory = Path(mask_directory)
    print('size of all matching files in photo_directory: ', len(list(photo_directory.glob('43.jpg'))))
    print('size of all matching files in mask_directory: ', len(list(mask_directory.rglob('00000_*.png'))))
    output_directory = output_directory
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)


    print('running main')
    for i in range(0, 30000):
        if i%100 ==0:
            print(f'processing {i}-th photo')
        file_name = str(i).zfill(5) + '_*'

        print('file_name ', file_name, ', of type: ', type(file_name))

        #list of files in mask
        # background_mask_directory = 

        mask_list = list(mask_directory.rglob(file_name))


        print('size of mask_list: ', len(mask_list))
        full_image_name = '**/' + str(i) + '.jpg'
        original_image = cv.imread(str(Path(list(photo_directory.glob(full_image_name))[0])))
        original_image = cv.resize(original_image, (512, 512), interpolation=cv.INTER_AREA)

        # remove background
        im = bg_remove(mask_list, original_image)

        # eyes
        eyes_file_name = '**/' + str(i).zfill(5) + '*eye.png'
        eyelist = list(mask_directory.glob(eyes_file_name))
        # print(eyelist)

        if len(eyelist) >= 2:
            im = skin_tone_eye(eyelist, im)

        # hair
        hair_file_name = '**/' + str(i).zfill(5) + '*hair.png'
        hairlist = list(mask_directory.glob(hair_file_name))
        im = hair_brighten(hairlist, im)

        #image adjustments
        im = preprocessing(im)
#
        outfile = output_directory + os.path.basename(str(i)) + '.jpg'
        print(outfile)
        status = cv.imwrite(outfile, im)

#TODO: make 5 iterations per image
# randomize hair brightening as effect not idea
# Randomize linen texture overlay i.e. which sections on the texture and different textures


if __name__ == '__main__':

    

    PHOTO_DIRECTORY = '/Users/shufaichan/Documents/datasets/CelebAMask-HQ/CelebA-HQ-img'

    MASK_DIRECTORY = '/Users/shufaichan/Documents/datasets/CelebAMask-HQ/CelebAMask-HQ-mask-anno'

    OUTPUT_SHROUD_DIRECTORY = '/Users/shufaichan/Documents/datasets/CelebAMask-HQ/artiticial_shroud_dataset'

    main(PHOTO_DIRECTORY, MASK_DIRECTORY, OUTPUT_SHROUD_DIRECTORY)
