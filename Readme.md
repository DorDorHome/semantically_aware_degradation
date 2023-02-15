Script to convert faces to shroud-like images
![4 CelebA-HQ-img.jpg](4%20CelebA-HQ-img.jpg)![4 Shrouded.jpg](4%20Shrouded.jpg)![4 Shrouded hair brighten.jpg](4%20Shrouded%20hair%20brighten.jpg)

# Instructions
Download dataset from https://github.com/switchablenorms/CelebAMask-HQ
In main.py, replace with respective directories and run script

    PHOTO_DIRECTORY = '/home/cihe/Shroud/dataset/CelebAMask-HQ'
    MASK_DIRECTORY = '/home/cihe/Shroud/dataset/CelebAMask-HQ'
    OUTPUT_SHROUD_DIRECTORY = '/home/cihe/Shroud/dataset/CelebAMask-HQ/Preprocessed/'
    
    main(PHOTO_DIRECTORY, MASK_DIRECTORY, OUTPUT_SHROUD_DIRECTORY)


