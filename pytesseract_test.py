from PIL import Image
import pytesseract
#import os

def convert_to_grayscale(image_path):
    """Load an image and convert it to grayscale."""
    try:
        image = Image.open(image_path)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        grayscale_image = image.convert('L')  # Convert to grayscale
        return grayscale_image
    except (TypeError, IOError) as e:
        print(f"Error loading or converting image: {e}")
        return None



img_file = "kiskep.png"
#img = Image.open(path)
#img = img.convert('RGBA')

#img = convert_to_grayscale(img_file)
img = Image.open(img_file)
ocr_result = pytesseract.image_to_string(img)

print(ocr_result)

#with open("ocr_output.txt", "w") as file:
#    file.write(ocr_result)