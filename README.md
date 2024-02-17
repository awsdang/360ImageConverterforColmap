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

**Basic Usage**
To use the 360 Image Converter for Colmap, start by running the script with your specified input and output directories. This basic command line example sets up the directories for processing:
```
python converter.py -i "path/to/input" -o "path/to/output"
```

**Testing Mode**
Before processing a large batch of images, you might want to run the script in test mode. This mode processes only the first image (or a specified number of images) and provides valuable information on the viewing angles generated. This is particularly useful for identifying specific angles you may want to exclude in the final batch process.
Enable test mode by adding the --test flag. Optionally, specify the number of frames to process in test mode with --test_count:
```
python converter.py -i "path/to/input" -o "path/to/output" --test --test_count 5
```

**Excluding Specific Angles**
Based on the output from the test mode, you might identify certain horizontal (H) or vertical (V) angles that you prefer not to include in your final output. Use the --exclude_h_angles and --exclude_v_angles parameters to exclude these angles. Specify the angles as comma-separated values:
```
python converter.py -i "path/to/input" -o "path/to/output" --exclude_h_angles '45,135' --exclude_v_angles '-45,-135'
```


**Full Command with All Options**
To fully utilize the script with all customizable options, your command might look like this:
```
python converter.py -i "path/to/input" -o "path/to/output" -res 800 800 --base_angle -10 10 --fov 95 --threads 16 --overlap 5 --exclude_h_angles '45,135' --exclude_v_angles '-45,-135' --sort_v
```
This command sets custom resolutions to 800x800, base angles to be H:-10,V:10 , fields of view to 95, thread counts for multithreading to 16, overlap percentages to 5%, excluded angles H: 45 and 135 V: -45 and -135, and an option to start sorting images vertically instead of horizontally.


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
