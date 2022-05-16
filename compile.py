import os
import timeit
import fnmatch
import img2video

img_path = './image_out/'
video_path = './'
data_path = './'

def main():
    img_type = 'uint8_TIFF'
    video_type = 'mp4'

    img2video.convert2MP4(video_path, img_type)

if __name__ == '__main__':
    main()