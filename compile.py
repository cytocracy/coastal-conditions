import os
import cv2
from PIL import Image

os.chdir("D:\\Development\\Chem\\coastal-conditions\\image_out")
path = "D:\\Development\\Chem\\coastal-conditions\\image_out\\"

mean_height = 0
mean_width = 0
num_of_images = len(os.listdir('.'))

def generate_video():
    image_folder = "D:\\Development\\Chem\\coastal-conditions\\image_out"
    video_name = 'video.avi'
    os.chdir(image_folder)

    images = [img for img in os.listdir(image_folder)
              if img.endswith(".tiff")]

    print(images)
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape
    video = cv2.VideoWriter(video_name, 0, 30, (width, height))
    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()

generate_video()