# Bad Apple In Terminal

Bad Apple, but it runs in your terminal. A terminal-based video player that displays the Bad Apple animation or any black and white (not monochrome) video you process as a series of characters.
This isn't a novel idea, plenty of peolple have made CLI bad apple, but this uses .BadApple files which could make it significantly easier to put it wherever you want

## Usage
### Prerequisites
#### Install Required Dependencies:
- Make sure you have Python 3 installed.
- if you plan on using the video reader you also need:
  - You'll need the Python Imaging Library (`PIL`), which is provided by the Pillow package:

            pip install Pillow
  - You'll need `tqdm`:

            pip install tqdm


#### Terminal:
- It is advised that you use a fast terminal like [Alacritty](https://github.com/alacritty/alacritty) (free to download) or any terminal with hardware acceleration. If you use a slower terminal, the video playback will likely be choppy or entirely broken. The terminal needs to also support ANSI escape codes, specifically `ESC[H`, `\033[H` or `\e[H`, and `ESCc`, `\033c` or `\ec`
- Zoom out (usually `'ctrl' + '-` is supported) or use a small font size to fit the video on screen. Word wrapping will cause issues with playback, so make sure the terminal window is large enough.
- **DO NOT TRY TO RUN THIS IN VS CODE**. VS Code has a hidden character print limit and will create visual artifacts when trying to run the video in the terminal. I have tried to get it to work and concluded that VS Code's integrated terminal isn't powerful enough

#### Video Processing:
- The video data is preprocessed and stored in a custom ``.BadApple`` binary format, which is then read for playback.
- The entire video is loaded into memory before playback. For larger videos, this may take up a few hundred MB, but the playback will be smoother.

### Running the Default Video (Bad Apple)
- To run the Bad Apple animation in your terminal, simply execute the `BadApple.py` script:

      python BadApple.py

## Running Other Videos

### To use other videos (not just Bad Apple), follow these steps:
*Note: .BadApple only supports pure black and white (2-color) videos. If you try to use a regular color video, you might get unexpected results due to how luminance-based conversion works. Videos with high contrast are more likely to work.*

#### Convert Your Video to PNG Frames:
First, you need to convert your video into individual `PNG` images. You can use `ffmpeg` to extract frames from your video:

      ffmpeg -i Z.mp4 -vf "fps=Y" video/frame%X4d.png
 - where `X` is large enough to amount of digits in the frame count (e.g for 3200 frame I need X to be 4, for 244334 frames I need X to be 6), `Y` is the FPS you want the final animation to run at (does not need to be the same as the original video), and `Z` is the name of the video
 - the video should be stored in the folder where the repository is placed (not in the video folder, in the same place as `video reader.py`)
 - This will generate frames from `Z.mp4` (replace Z with your actual file name) at a rate of Y frames per second and store them in the `video/` directory with filenames like `frame0001.png`, `frame0002.png`, etc.
 - this should be performed after you cd into the folder where you have saved the repository

        cd this/repository's/file/path/ 
- Make sure to install `ffmpeg` using your package manager if you don't already have it installed.

#### Adjust Frame Resolution:
You may need to adjust the frame resolution in the code to match the video’s resolution. Open the script (BadApple.py or the relevant script) and modify the constants at the top to fit your video’s dimensions.
- `FRAME_WIDTH`: Set the width of the frame (usually the horizontal dimension of the video).
- `FRAME_HEIGHT`: Set the height of the frame (usually the vertical dimension of the video).
- you can usually find this from the source of the video. 'Bad Apple!!' runs at `360p` max which is `480x360px`

#### Create a `.BadApple` File:
- Once your frames are ready, run the script to process the images into the `.BadApple` format. This step will read each PNG frame and store it in the `.BadApple` binary format.
  
      python process_video.py

#### Play the Processed Video:
After the `.BadApple` file is generated, you can use BadApple.py to view the video:
 - if your video is not using the same frame size, modifier, frame rate etc, go into the file and change the constants at the top

        python BadApple.py

## `.BadApple` Files
The `.BadApple` files are a custom binary format that stores the video frame data. The format is highly optimized for terminal rendering and includes pixel information (black or white) for each frame. These do not include the video frame rate, frame size or audio (this project currently does not support audio) so you will need to store these somewhere separate and edit the constants at the top of the file to run a `.BadApple` file. You may get unexpected results if you do not do this 
The `.BadApple` file is not playable in any standard video player, nor is it supported anywhere else. It is designed solely for use with the provided scripts.

### Internal Storage
- `.BadApple` files are stored in bits. The smallest addressable unit of information is technically bytes but we can workaround this with bitwise operators, but it means the file takes a while to read
- Each bit represents a pixel, `0` for black, `1` for white
- No compression is used because `RLE` (Run-Length Encoding) would require delimiters (which may happen to appear in the video and ruin the format) and it is already 24x as efficient as a standard uncompressed 24-bit RGB video file
- There is no storage of the frame size or the number of frames. It is split at runtime by taking the configuration from the constants at the top of the file
- Bits are written left to right, top to bottom. here is an example of a single frame for a clearer explanation of what this means:

      Frame Dimensions: 5x5
      Raw Bits: 11111 01110 11111 01110 11111
      Output:
      ██████████
      ██      ██
      ██████████
      ██      ██
      ██████████
- We differentiate frames based on the expected resolution of the frame. In the above example, we expect the resolution to be 25 (5x5). So after we have read 25 bits we know we have finished the frame and can print it, then move onto the next frame

## Additional Notes
**Performance Considerations:** The video is rendered as a sequence of characters in the terminal, so the rendering speed depends heavily on your terminal’s performance and your system’s capabilities. On a fast terminal like [Alacritty](https://github.com/alacritty/alacritty), the video should play smoothly, but on slower systems or terminals, the playback may be choppy. Setting the frame rate down can reduce this issue but the video will play slower unless you also make a custom video with its own frame rate

**Cross-Platform Compatibility:** The script has been tested on Linux (Kali) but should work on other major operating systems as well, such as Windows. However, performance may vary depending on the terminal emulator you are using and I cannot guarantee that it will work.




