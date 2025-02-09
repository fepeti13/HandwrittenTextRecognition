import csv
import os
import re


def parse_output_file(input_file, output_csv):
    """Reads extracted text from the OCR output and writes words grouped into rows."""

    words = []  # List to store (word, y_position)

    # Regex pattern to match words and their bounding boxes
    word_pattern = re.compile(r"Word: '(.+?)' \(Confidence: (.+?)\)")
    bbox_pattern = re.compile(
        r"Bounding Box: \[\((\d+), (\d+)\), \(.*?\), \((\d+), (\d+)\)\]"
    )  # Extract x1, y1, x3, y3

    with open(input_file, "r", encoding="utf-8") as file:
        lines = file.readlines()

    current_word = None
    current_x1, current_y1, current_x3, current_y3 = None, None, None, None

    for line in lines:
        word_match = word_pattern.search(line)
        bbox_match = bbox_pattern.search(line)

        if word_match:
            current_word = word_match.group(1)  # Extract word

        if bbox_match:
            current_x1, current_y1, current_x3, current_y3 = map(
                int, bbox_match.groups()
            )  # Extract coordinates

        if current_word and None not in (
            current_x1,
            current_y1,
            current_x3,
            current_y3,
        ):
            mean_x = (current_x1 + current_x3) / 2
            mean_y = (current_y1 + current_y3) / 2
            words.append((current_word, mean_x, mean_y))
            current_word, current_x1, current_y1, current_x3, current_y3 = (
                None,
                None,
                None,
                None,
                None,
            )  # Reset

    # Print the extracted words and bounding box values
    for word_data in words:
        print(word_data)

        # Sort words by Y-coordinate (top to bottom)
        words.sort(key=lambda x: x[2])

        # Group words into rows based on a Y-coordinate threshold
        rows = []
        current_row = []
        prev_y = None
        threshold = 20  # Adjust this if needed (defines row separation)

        for word, mean_x, mean_y in words:
            # Group words by their Y-coordinate and keep them sorted by X-coordinate within a row
            if prev_y is None or abs(mean_y - prev_y) < threshold:
                current_row.append(
                    (mean_x, word)
                )  # Store word along with its x-coordinate
            else:
                # Sort the current row by x-coordinate before appending it
                current_row.sort(key=lambda x: x[0])  # Sort by x-coordinate
                rows.append(
                    [word for _, word in current_row]
                )  # Add sorted words to rows
                current_row = [(mean_x, word)]  # Start a new row with the current word

            prev_y = mean_y

        # Sort the last row if necessary
        if current_row:
            current_row.sort(key=lambda x: x[0])  # Sort by x-coordinate
            rows.append([word for _, word in current_row])  # Add last row

        # Save the structured table as a CSV file
        with open(output_csv, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(rows)

        print(f"Processed OCR output saved to: {output_csv}")


"""
# Example usage
parse_output_file(
    "/home/fepeti13/Desktop/Research/output_6762.txt",
    "/home/fepeti13/Desktop/Research/structured_output_6762.csv",
)
"""

# Save output to a text file
folder = "/home/fepeti13/Desktop/Research/Cropped/"
output_folder = folder

pattern = re.compile(r"IMG_\d{4}\_b1.txt", re.IGNORECASE)
for filename in os.listdir(folder):
    if pattern.match(filename):
        print("Processing {filename}")

        file_path = os.path.join(folder, filename)

        new_filename = filename.replace(".txt", ".csv")
        output_file = os.path.join(output_folder, new_filename)
        # output_file = "/home/fepeti13/Desktop/Research/output_6762.txt"

        parse_output_file(file_path, output_file)
