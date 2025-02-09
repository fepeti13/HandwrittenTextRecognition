import os
import re

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/fepeti13/Desktop/Research/durable-sunspot-449919-k7-02ac20478b89.json'

from google.cloud import vision

def detect_document(path):
    """Detects document features in an image and returns extracted text with bounding boxes."""
    
    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)

    extracted_text = ""

    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            extracted_text += f"\n Block (Confidence: {block.confidence:.2f})\n"

            for paragraph in block.paragraphs:
                extracted_text += f"     Paragraph (Confidence: {paragraph.confidence:.2f})\n"

                for word in paragraph.words:
                    word_text = "".join([symbol.text for symbol in word.symbols])

                    # Extract bounding box coordinates
                    bbox = [(vertex.x, vertex.y) for vertex in word.bounding_box.vertices]

                    extracted_text += f"        Word: '{word_text}' (Confidence: {word.confidence:.2f})\n"
                    extracted_text += f"             Bounding Box: {bbox}\n"

                    for symbol in word.symbols:
                        extracted_text += f"            Symbol: {symbol.text} (Confidence: {symbol.confidence:.2f})\n"

    if response.error.message:
        raise Exception(
            f"{response.error.message}\nFor more info: https://cloud.google.com/apis/design/errors"
        )

    return extracted_text.strip()

# Save output to a text file
folder = "/home/fepeti13/Desktop/Research/Cropped/"
output_folder = folder

pattern = re.compile(r"IMG_\d{4}\_b1.JPG", re.IGNORECASE)
for filename in os.listdir(folder):
        if pattern.match(filename):
            print("Processing {filename}")

            file_path = os.path.join(folder, filename)
            text = detect_document(file_path)

            new_filename = filename.replace(".JPG", ".txt")
            output_file = os.path.join(output_folder, new_filename)
            #output_file = "/home/fepeti13/Desktop/Research/output_6762.txt"
            with open(output_file, "w", encoding="utf-8") as file:
                file.write(text)
                print(f"Text with bounding boxes saved to {output_file}")


