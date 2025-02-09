from PIL import Image
import os
import re

input_folder = "/home/fepeti13/Desktop/Research/Cropped/"
output_folder = input_folder

CROP_COORDS = (200, 100, 1900, 1300)

def rotate_img(img):
    if img.height < img.width:
        #img = img.transpose(Image.ROTATE_90) 
        img.show()
        print("Rotation was successfull")
        img.save('/home/fepeti13/Desktop/Research/Cropped/IMG_5765_Rot.JPG')
        return img


def process_images(folder):
    pattern = re.compile(r"IMG_\d{4}\.JPG", re.IGNORECASE)

    for filename in os.listdir(folder):
        if pattern.match(filename):
            file_path = os.path.join(folder, filename)
            print(f"Processigng {filename}")

            img = Image.open(file_path)
            cropped_img = img.crop(CROP_COORDS)

            new_filename = filename.replace(".JPG", "_b1.JPG")
            output_path = os.path.join(output_folder, new_filename)

            cropped_img.save(output_path)
            print(f"Saved: {new_filename}")



process_images(input_folder)

#image_path = "/home/fepeti13/Desktop/Research/Cropped/IMG_5765.JPG"
#img = Image.open(image_path)
#print('Image opened sucsesfully')

#region = (300, 100, 1900, 1300)
#cropped_b1 = img.crop(region)

#cropped_b1.save(f"/home/fepeti13/Desktop/Research/Cropped/IMG_5765_b1.jpg")

#print("Images cropped and saved successfully.")
