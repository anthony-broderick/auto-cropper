# Auto Cropper

## Use

Takes multiple photos and crops them to the user provided aspect ratio, centered horizontally around the subject's eyes and uses the 2/3rd ratio for eye height in each photo.

The output pictures can be zipped into individual folders by selecting option '1' when running the program.

## How To Use

1. Drop folder(s) or raw images into the 'input_pictures' folder.
2. Enter 'make run' into the terminal.
3. Type a selection (number to the left of an option)

    MENU

    [0] Crop Input Pictures to Desired Aspect Ratio
    [1] Zip Output Pictures
    [2] Delete Input Pictures
    [3] Delete Output Pictures
    [4] Exit

4. Follow provided instructions in terminal.

## How It Works

The program uses the built in cv2 haarcascade data models to detect faces and eyes. The program calculates the average height of all of the eye boxes and the average center x position of all of the eye boxes. Using these two averages, the program centers the photo with the average center x position in the horizontal middle of the photo and the average eye height 1/3 of the photo's height from the top of the picture. It will iterate through each photo in the input_pictures folder, doing this process for each.

## Multi-Processing

The program takes the max amount of CPU cores from the user's device and does multi-processing amongst each photo in the input_pictures folder.
