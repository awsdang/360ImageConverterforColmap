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
python converter.py --input_directory "path/to/input" --output_directory "path/to/output" --start_angle 0 0 --res 800 800 --fov 100 100 --threads 10 --overlap 5
```

# Parameters
-i, --input_directory: Input directory containing 360 images.
-o, --output_directory: Output directory for perspective images.
--start_angle: Base viewing angle for output images (u, v).
--res: Output height and width of the images.
--fov: Field of view in degrees (horizontal, vertical).
--threads: Maximum number of worker threads.
--overlap: The overlaps parameter between images min 0, max 100.
--exclude_h_angles: Comma-separated list of horizontal angles to exclude.
--exclude_v_angles: Comma-separated list of vertical angles to exclude.
--sort_v: If specified, sort images vertically.
--test: If specified, process only the first image.
--test_count: If specified, process the specified number of frames.
