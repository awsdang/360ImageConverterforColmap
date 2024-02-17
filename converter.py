import os
import numpy as np
from PIL import Image
import py360convert
import concurrent.futures
import argparse
import time


def sort_v_first(angles, exclude_h_angles):
    high_cutoff = max(exclude_h_angles) if exclude_h_angles else 360
    low_cutoff = min(exclude_h_angles) if exclude_h_angles else 0

    sorted_v = sorted(
        angles,
        key=lambda angle: (angle[0], angle[1] - 360 if angle[0] > high_cutoff else (angle[0] if angle[0] < low_cutoff else 360))
    )
    return sorted_v

def sort_h_first(angles, exclude_h_angles):
    high_cutoff = max(exclude_h_angles) if exclude_h_angles else 360
    low_cutoff = min(exclude_h_angles) if exclude_h_angles else 0
    sorted_h = sorted(
        angles,
        key=lambda angle: (angle[1], angle[0] - 360 if angle[0] > high_cutoff else (angle[0] if angle[0] < low_cutoff else 360))
    )
    return sorted_h 

def generate_viewing_angles(base_u, base_v, fov, overlap, sort_v, exclude_h_angles, exclude_v_angles, test_mode):
    h_fov, v_fov = fov
    h_step = h_fov * (1 - overlap / 100)
    v_step = v_fov * (1 - overlap / 100)
    horizontal_angles = np.arange(base_u, 360, h_step) % 360
    vertical_start = max(-90, base_v - v_fov / 2)
    vertical_end = 90
    vertical_angles = np.arange(vertical_start, vertical_end + 1, v_step)
    vertical_angles = np.clip(vertical_angles, -90, 90)
    angles = [(h, v) for v in vertical_angles if v not in exclude_v_angles for h in horizontal_angles if h not in exclude_h_angles]  
    angles += [(h, 90) for h in horizontal_angles if h not in exclude_h_angles if 90 not in exclude_v_angles]
    if(sort_v):
        angles = sort_v_first(angles, exclude_h_angles)
    else:
        angles = sort_h_first(angles, exclude_h_angles)
    if(test_mode):
        for index, (h_angle, v_angle) in enumerate(angles):
            print(f"{index+1}: h:{h_angle} v:{v_angle}")
    return angles

def process_single_angle(filename, output_dir, res, fov, i, u_deg, v_deg, e_img):
    p_img = py360convert.e2p(e_img, fov_deg=fov, u_deg=u_deg, v_deg=v_deg, out_hw=res)
    formatted_i = f'{i+1:02d}'
    output_filename = f'{os.path.splitext(filename)[0]}_perspective_{formatted_i}.png'
    Image.fromarray(p_img).save(os.path.join(output_dir, output_filename))  


def generate_images(filename, output_dir, res, fov, viewing_angles, e_img, threads, test_mode):
    if test_mode:      
         with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(process_single_angle, filename, output_dir, res, fov, i, u_deg, v_deg, e_img) 
                       for i, (u_deg, v_deg) in enumerate(viewing_angles)]
            concurrent.futures.wait(futures)
    else:
        for i, (u_deg, v_deg) in enumerate(viewing_angles):
            process_single_angle(filename, output_dir, res, fov, i, u_deg, v_deg, e_img)

    
def process_image(filename, input_dir, output_dir, res, base_angle, fov, overlap, sort_v, exclude_h_angles, exclude_v_angles, test_mode, threads=0):
    file_path = os.path.join(input_dir, filename)
    e_img = np.array(Image.open(file_path))
    base_u, base_v = base_angle
    viewing_angles = generate_viewing_angles(base_u, base_v, fov, overlap, sort_v, exclude_h_angles, exclude_v_angles, test_mode)
    generate_images(filename, output_dir, res, fov, viewing_angles, e_img, threads, test_mode)
    print(f'Processed {filename}')


def convert_and_save_perspective_images(input_dir, output_dir, res, base_angle, fov, threads, overlap, exclude_h_angles, exclude_v_angles, sort_v=False, test_mode=False, test_count=1):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    start_time = time.time()

    images = [filename for filename in os.listdir(input_dir) if filename.endswith('.jpg')]
    
    if test_mode:
        images = images[:test_count]  # Take only the first 3 images if --test is specified
        for filename in images:  # Iterate over each image
            process_image(filename, input_dir, output_dir, res, base_angle, fov, overlap, sort_v, exclude_h_angles, exclude_v_angles, test_mode, threads)

    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(process_image, filename, input_dir, output_dir, res, base_angle, fov, overlap, sort_v, exclude_h_angles, exclude_v_angles, test_mode) 
                       for filename in images]
            concurrent.futures.wait(futures)

    end_time = time.time()
    print(f"{end_time-start_time} seconds.")


def main():
    parser = argparse.ArgumentParser(description='Convert 360 images to perspective views.')
    parser.add_argument('-i', '--input_directory', required=True, help='Input directory containing 360 images.')
    parser.add_argument('-o', '--output_directory', required=True, help='Output directory for perspective images.')
    parser.add_argument('--start_angle', nargs=2, type=int, default=(0, 0), help='Base viewing angle for output images (u, v).')
    parser.add_argument('--res', nargs=2, type=int, default=(800, 800), help='Output height and width of the images.')
    parser.add_argument('--fov', nargs=2, type=float, default=(100, 100), help='Field of view in degrees (horizontal, vertical).')
    parser.add_argument('--threads', type=int, default=10, help='Maximum number of worker threads.')
    parser.add_argument('--overlap', type=float, default=5, help='the overlaps parameter between images min 0, max 100.')
    parser.add_argument('--exclude_h_angles', type=str, default='', help='Comma-separated list of horizontal angles to exclude (e.g., "40,60,90"')
    parser.add_argument('--exclude_v_angles', type=str, default='', help='Comma-separated list of vertical angles to exclude (e.g., "40,60,90"')
    parser.add_argument('--sort_v', action='store_true', help='If specified, sort images vertically.')
    parser.add_argument('--test', action='store_true', help='If specified, process only the first image.')
    parser.add_argument('--test_count', type=int, default=1, help='If specified, process the number of frames')
    args = parser.parse_args()
    exclude_h_angles = [float(angle.strip()) for angle in args.exclude_h_angles.split(',') if angle.strip()] if args.exclude_h_angles else []
    exclude_v_angles = [float(angle.strip()) for angle in args.exclude_v_angles.split(',') if angle.strip()] if args.exclude_v_angles else []
    convert_and_save_perspective_images(args.input_directory, args.output_directory, tuple(args.res), tuple(args.start_angle), tuple(args.fov), args.threads, args.overlap, exclude_h_angles, exclude_v_angles, args.sort_v, args.test, args.test_count)

if __name__ == '__main__':
    main()
