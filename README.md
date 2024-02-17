# 360ImageConverterforColmap
This Python script converts 360-degree images into multiple perspective views based on specified viewing angles, field of view (FOV), and other parameters. It utilizes the `py360convert` library to perform the conversions and supports multithreading for processing multiple images concurrently.

## Features
- Converts 360-degree images to perspective views.
- Customizable base viewing angle, field of view, and image resolution.
- Supports exclusion of specific horizontal and vertical angles.
- Option to sort images vertically.
- Multithreading support for faster processing.

## Requirements
- Python 3.x
- numpy
- Pillow
- py360convert

## Installation
Install the required Python libraries by running:
```
pip install -r requirements.txt
```

# Usage
Run the script from the command line, specifying the necessary parameters. Here is an example command:

```
python converter.py --input_directory "path/to/input" --output_directory "path/to/output"
```

# Parameters
- -i, --input_directory: Input directory containing 360 images.
- -o, --output_directory: Output directory for perspective images.
- -res: Output height and width of the images. default is 1600x1600
- --base_angle: Base viewing angle for output images (u, v). default is H:0,V:0
- --fov: Field of view in degrees (horizontal, vertical). default is 70
- --threads: Maximum number of worker threads. default is 4
- --overlap: The overlaps parameter between images min 0%, max 100%. default is 10%
- --exclude_h_angles: Comma-separated list of horizontal angles to exclude. default is None
- --exclude_v_angles: Comma-separated list of vertical angles to exclude. default is None
- --sort_v: If specified, sort images vertically. default is False
- --test: If specified, process only the first image. default is False
- --test_count: If test is enabled, process the specified number of frames. default is 1
