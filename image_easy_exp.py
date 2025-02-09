from PIL import Image
import pytesseract_test
import os

# Path to your Tesseract executable (adjust this based on your installation)
pytesseract_test.pytesseract_test.tesseract_cmd = r'/usr/local/bin/tesseract'  # Update to the correct path

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

def convert_image_to_text(grayscale_image):
    """Extract text from a grayscale image using pytesseract."""
    try:
        text = pytesseract_test.image_to_string(grayscale_image, config='--oem 1')
        return text
    except Exception as e:
        print(f"Error extracting text: {e}")
        return None

# Example usage
image_path = 'kiskep.png'

# Step 1: Convert the image to grayscale
grayscale_image = convert_to_grayscale(image_path)

grayscale_image.show()

if grayscale_image:
    # Step 2: Extract text from the grayscale image
    text = convert_image_to_text(grayscale_image)
    
    if text:
        print("Extracted Text:\n", text)
    else:
        print("Failed to extract text.")
else:
    print("Failed to load or convert the image.")
