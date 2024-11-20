"""
Frame-By-Frame .BadApple Converter

This is the file used to convert your own frame-by-frame vide files into .BadApple files
An understanding of how .BadApple files is not strictly needed, but is recomended for using this file
This can take a very long time to run if you're using a high quality video. Converting the full 'Bad Apple!' source at 60fps would took my laptop about an hour
I think that's due to repeated file access though so it's quite hard to improve. Writing to files with multithreading would usually lead to race conditions
Refer to the README for more information on how to use this file
"""

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Constants ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# What name you want to store your file under. Should end in .BadApple
FILE_NAME: str = 'test.BadApple'

# Most terminals or implemenations of .BadApple files are not going to be able to handle the same quality as a full video
# As such, you can modify how frequently you sample the pixels
# a sample rate of 2 runs across half the number of pixels horizontally and vertically, or 1/4 the number of pixels total
# you can use this value to decrease the size of the video, larger modifiers lead to lower quality, smaller files
RESOLUTION_MOD: int = 1

# This is the resolution of the video 
FRAME_WIDTH: int = 480
FRAME_HEIGHT: int = 360

# The number of PNGs extracted from your frame-by-frame (check the folder where you stored the ffmpeg output if you don't know the exact value)
EXPECTED_FRAME_COUNT: int = 5255

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Imports and Other Pre-Processing ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from tqdm import tqdm
from PIL import Image
import BadApple
from time import sleep

# Clear the terminal so we don't get overlapping text later
print("\033c")

# This defines how many numerical characters to check for in the file names frameXXXX.png
PNG_COUNTER_LENGTH: int = len(str(EXPECTED_FRAME_COUNT))


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Main ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# This is [row][column][x coordinate, y coordinate]
pixel_positions: list[list[list[int, int]]] = []

# This loop calculates all of the pixels we're going to check and caches them
for y in range(0, FRAME_HEIGHT, RESOLUTION_MOD):
    row: list[int] = []

    for x in range(0, FRAME_WIDTH, RESOLUTION_MOD):
        row.append([y, x])
    pixel_positions.append(row)




# The main video conversion loop:

# Using tqdm here adds a fancy progress bar
for i in tqdm(range(1, EXPECTED_FRAME_COUNT + 1)):
    print(f"\033[Hconverting frame {i}/{EXPECTED_FRAME_COUNT}")
    try:
        with Image.open(f"video/frame{i:0{PNG_COUNTER_LENGTH}d}.png") as frame:

            # stores the RGB values as [row][column][R,G,B]
            frame_data: list[list[int,int,int]] = []

            for row in pixel_positions:
                for position in row:
                    frame_data.append(frame.getpixel((position[1], position[0])))


            # We convert each pixel to black or white based on a luminance value to account for how we see brightness
            for index, pixel in enumerate(frame_data):
                # this is the standard luminance formula
                luminance = (0.2126 * pixel[0]) + (0.7152 * pixel[1]) + (0.0722 * pixel[2])

                # white pixel if it is >50%, else black
                frame_data[index] = luminance > 128

            # This function works in append mode so we can write multiple times
            # Writing one time would risk running out of memory because we would need to store the entire file on RAM
            BadApple.WriteBitsToBinaryFile(frame_data, FILE_NAME)

    except FileNotFoundError:
        print(f"video/frame{i:0{PNG_COUNTER_LENGTH}d}.png or {FILE_NAME} could not be opened. This is usually due to incorrect usage of ffmpeg or incorrect configuration")
        quit()
    
    except:
        print(f"an unknown error occured on frame {i}")
        quit()
