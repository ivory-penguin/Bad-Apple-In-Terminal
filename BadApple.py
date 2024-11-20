"""
Bad Apple Terminal Player

Plays Bad Apple (or whatever custom video you put in) in the terminal
The included .BadApple file is BadApple.BadApple which runs with the config:
 - File name of BadApple.BadApple
 - Frame size of 480x360
 - Resolution mod of 2
 - Frame rate of 24
"""

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Constants ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# this is what file we read the data from
# It should always be a .BadApple file obtained from the video reader
FILE_NAME: str = 'BadApple.BadApple'

# This should match the BASE quality of the video
# If you used a resolution mod you are recomended to edit the resolution mod instead
FRAME_WIDTH: int = 480
FRAME_HEIGHT: int = 360

# This adjusts the frame size based on the resolution mod put into the video reader
# If you put x mod into the video reader, you should use x mod when running the video
RESOLUTION_MOD: int = 2

# How many frames we play per second
FRAME_RATE: int = 24

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Imports and Other Pre-Processing ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from time import sleep, time

# The only reason I change the values of constants is to simplify the process of changing the constants above
# The constants do not change beyond this point
# Forgive me programming gods, for I have broken naming conventions
FRAME_WIDTH //= RESOLUTION_MOD
FRAME_HEIGHT //= RESOLUTION_MOD
FRAME_RESOLUTION = FRAME_HEIGHT * FRAME_WIDTH


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Functions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# This function takes a byte as an input, and returns a list of 8 boolean bits
# For example, if you put in the number 255 you would get out [1, 1, 1, 1, 1, 1, 1, 1] for example
def ConvertByteToBits(byte: bytes) -> list[bool]:
    bit_list: list[bool] = []

    # we itterate from 7 to 0 because we're essentially indexing the byte
    for i in range(7, -1, -1):

        # This checks the value of the ith bit and casts it to a boolean
        bit: bool = bool((byte >> i) & 1)

        bit_list.append(bit)

    return bit_list


# This function reads the given (given by constant) .BadApple file
# It returns a boolean 3D list of [frame][row][column] where each element represents a black or white pixel
def GetBadApple() -> list[list[list[bool]]]:

    with open(FILE_NAME, 'rb') as file:
        BadAppleBytes: list[bytes] = file.read()

        # 1D list of bits
        BadAppleBits: list[bool] = []

        # 3D list of [frame][row][column]
        BadApple: list[list[list[bool]]] = []




        # This is the loop that converts the bytes into bits
        num_bytes: int = len(BadAppleBytes)
        for i, byte in enumerate(BadAppleBytes):
            # we only display this every 1234 frames because rendering calls slows down the conversion process so we want to print less
            if i % 1234 == 0:
                # \033[H moves the cursor back to the start of the file
                print(f"\033[Hconverting the .BadApple to bits ({i}/{num_bytes})     ")

            bits: list[bool] = ConvertByteToBits(byte)
            BadAppleBits.extend(bits)


        # Quick sanity check to make sure the file isn't corrupted, incorrectly created or had a runtime error
        expected_bit_count: int = (len(BadAppleBytes) * 8)
        if expected_bit_count != len(BadAppleBits):
            input(f"Warning: Bit count mismatch! Expected {expected_bit_count}, got {len(BadAppleBits)}")

        # This is the loop that converts the list of bits into a more easily readable format
        for frame_start in range(0, len(BadAppleBits), FRAME_RESOLUTION):
            # \033[H to move cursor to start, divide everything by frame resolution because we count in bits here, not frames
            print(f"\033[Hconverting the .BadApple to frames ({frame_start/FRAME_RESOLUTION}/{len(BadAppleBits)/FRAME_RESOLUTION})     ")

            # Identify the next frame
            frame_bits: list[bool] = BadAppleBits[frame_start:frame_start + FRAME_RESOLUTION]

            # Format the frame into rows
            frame: list[list[bool]] = []
            for row_start in range(0, FRAME_RESOLUTION, FRAME_WIDTH):
                row: list[bool] = frame_bits[row_start:row_start + FRAME_WIDTH]
                frame.append(row)


            # Add the frame to the file
            BadApple.append(frame)

        # Making sure the file was read properly
        if not BadApple:
            raise FileNotFoundError("The program couldn't get any frames from your.BadApple file. Make sure the file is valid and accessible")

        return BadApple


# Takes some bits, converts them to bytes, puts them in the file
def WriteBitsToBinaryFile(bits, file_path):
    byte: int = 0
    bit_count: int = 0
    with open(file_path, 'ab') as file:
        for bit in bits:
            # This adds the bit to the right end of the bit and left shifts it (functionally adds it to the left side)
            byte = (byte << 1) | bit
            bit_count += 1

            # once we have a full byte, add it to the file and reset the byte
            if bit_count == 8:
                # We have a full byte
                file.write(byte.to_bytes(1, byteorder='big'))
                byte = 0
                bit_count = 0

        # If there are remaining bits, add them (very minor visual artifacts might exist on the final frame in this situation)
        if bit_count > 0:
            # we fill out the rest with 0s which will usually be invisible
            byte = byte << (8 - bit_count)
            file.write(byte.to_bytes(1, byteorder='big'))


# Super simple output function that displays the input frame
# Please don't complicate it with a list constructor, it's readable this way
def PrintFrame(frame):
    constructed_frame: list[char] = []

    # We construct the frame as one string to avoid multiple print calls
    for row in frame:
        constructed_frame.append(''.join("██" if bit else "  " for bit in row))
        constructed_frame.append('\n')

    # Flushing the output makes it render slightly faster in testing
    print(''.join(constructed_frame), flush=True)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Main ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    # clear the terminal
    print("\033c")

    # Get the frames onto memory
    BadApple: list[list[list[int]]] = GetBadApple()


    # Time debt is a system to make sure the video catches up if it ever takes too long to render any frame
    # We keep track of how far behind we are (behind refering to having rendered less frames than we would have expected to by now), and attempt to catch up whenever we would usually be waiting after rendering a frame
    time_debt: float = 0.0

    FRAME_TIME = 1 / FRAME_RATE
    for frame in BadApple:
        start: float = time()
        PrintFrame(frame)

        # This calculates how long the frame has taken to render
        # We add time_debt, so if we're behind time, we speed up the next frame(s) to catch up
        elapsed_time: float = time() - start + time_debt

        # Calculate if we're behind time and adjust time debt if so
        time_debt = 0 if elapsed_time > FRAME_TIME else elapsed_time - FRAME_TIME

        # sleeping until the end of the frame ensures that we're running at constant frame rate
        sleep(max((FRAME_TIME) - elapsed_time, 0))
