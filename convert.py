import cv2
import os
import argparse
from tqdm import tqdm

def video_to_images(path, target_fps, scale, vid_idx=0):
    cap = cv2.VideoCapture(path)
    
    output_directory = f"images"
    os.makedirs(output_directory, exist_ok=True)

    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print( f'found {length} frames' )
    
    for i in tqdm(range(length)):
        ret, frame = cap.read()
        
        if not ret:
            break
        
        # Only extract frames at the desired frame rate
        if i % int(cap.get(5) / target_fps) == 0:
            output_file = f"{output_directory}/frame_{vid_idx}_{i}.png"
            new_size = (int(frame.shape[1] * scale), int(frame.shape[0] * scale))
            frame = cv2.resize(frame, new_size, interpolation=cv2.INTER_AREA)
            cv2.imwrite(output_file, frame)
            
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert a video to a set of images.')
    parser.add_argument('-p', type=str, required=True, help='Path to a folder containing the video(s).')
    parser.add_argument('--fps', type=int, default=4, help='Target frames per second.')
    parser.add_argument('--scale', type=float, default=1, help='Scaling size of the images (default 0.25 -> 1/4 of the original size).')
    args = parser.parse_args()

    for root, dirs, files in os.walk(args.p):
        for i, file in enumerate(files):
            print(f'Processing {file} ...')
            video_to_images(os.path.join(root, file), args.fps, args.scale, vid_idx=i)