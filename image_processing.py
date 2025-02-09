import cv2
import matplotlib.pyplot as plt

# Load the image
print("done0")
image_path = '/home/fepeti13/Desktop/Research/kep2.JPG'
image = cv2.imread(image_path)
#image = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)  # Adjust fx and fy as needed

# Convert to grayscale
print("done1")
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply thresholding (using adaptive thresholding for more control)
thresh_image = cv2.adaptiveThreshold(
    gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
)
print("done2")

_, thresh_image = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY)
print("done3")
# Display the original, grayscale, and thresholded images
cv2.imwrite('original_image.jpg', image)
cv2.imwrite('grayscale_image.jpg', gray_image)
cv2.imwrite('thresholded_image.jpg', thresh_image)
print("done4")

import cv2
import numpy as np
import matplotlib.pyplot as plt

# Assuming `thresh_image` is the thresholded image from the previous step

# Apply edge detection
# Adjust the threshold values for edge detection
edges = cv2.Canny(thresh_image, 30, 100, apertureSize=3)
cv2.imwrite('edges_image.jpg', edges)  # Save the edges image to inspect visually

#edges = cv2.Canny(thresh_image, 50, 150, apertureSize=3)

# Detect lines using Hough Line Transform
# Detect lines with lower thresholds
lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=50, minLineLength=20, maxLineGap=5)


# Create a copy of the thresholded image to draw lines on
line_image = cv2.cvtColor(thresh_image, cv2.COLOR_GRAY2BGR)

# Draw lines on the image
if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), 2)

# Display the edge-detected and line-detected images
cv2.imwrite('detected_grid_lines.jpg', line_image)

plt.show()

# Assuming `lines` contains the detected lines from the previous step

# Separate lines into horizontal and vertical categories
horizontal_lines = []
vertical_lines = []

# Debug: Print line lists to verify they contain expected entries
print("Horizontal Lines:", horizontal_lines)
print("Vertical Lines:", vertical_lines)

# Segment the image based on intersections
cell_images = []
for i in range(len(horizontal_lines) - 1):
    for j in range(len(vertical_lines) - 1):
        # Define top-left and bottom-right corners of each cell
        x_start = vertical_lines[j][0]
        y_start = horizontal_lines[i][1]
        x_end = vertical_lines[j + 1][0]
        y_end = horizontal_lines[i + 1][1]

        # Ensure valid coordinates before cropping
        if x_end > x_start and y_end > y_start:
            cell = thresh_image[y_start:y_end, x_start:x_end]
            
            # Check if the cell is empty before saving
            if cell.size > 0:
                cell_images.append(cell)
                cell_filename = f'cell_{i}_{j}.jpg'
                cv2.imwrite(cell_filename, cell)
            else:
                print(f"Skipped empty cell at position ({i}, {j})")
        else:
            print(f"Invalid cell dimensions at position ({i}, {j})")

print("Cells segmented and saved successfully if no errors above.")


import cv2
import numpy as np

# Binarizáljuk a képet
image_path = 'thresholded_image.jpg'  # Replace with actual path
from PIL import Image
binary_image = np.array(Image.open(image_path).convert('L'))
_, binary_image = cv2.threshold(binary_image, 128, 255, cv2.THRESH_BINARY_INV)

# Függőleges vonalak detektálása nagyobb kernellel
vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
vertical_lines = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, vertical_kernel)

# Kontúrok megtalálása
contours, _ = cv2.findContours(vertical_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Új kép a szűrt kontúrok számára
filtered_vertical_lines = np.zeros_like(vertical_lines)

# Szűrés terület alapján
min_area = 500  # Ezt az értéket növelheted vagy csökkentheted
for cnt in contours:
    area = cv2.contourArea(cnt)
    if area > min_area:  # Csak a nagyobb területű vonalakat rajzoljuk újra
        cv2.drawContours(filtered_vertical_lines, [cnt], 0, 255, thickness=cv2.FILLED)

# Vízszintes vonalak detektálása a korábbi módszerrel
horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
horizontal_lines = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, horizontal_kernel)

# Morfológiai zárás a kis zajos vonalak eltüntetéséhez
closing_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
filtered_vertical_lines = cv2.morphologyEx(filtered_vertical_lines, cv2.MORPH_CLOSE, closing_kernel)
horizontal_lines = cv2.morphologyEx(horizontal_lines, cv2.MORPH_CLOSE, closing_kernel)

# Kombináljuk a detektált vonalakat
grid_lines = cv2.addWeighted(horizontal_lines, 0.5, filtered_vertical_lines, 0.5, 0)
cv2.imwrite('filtered_grid_lines_area_based.jpg', grid_lines)  # Mentsük a képet ellenőrzésre


import cv2
import numpy as np

# Töltsük be a tisztított rács képet és az eredeti képet
grid_path = 'filtered_grid_lines_area_based.jpg'
original_path = 'kep1.JPG'
grid_image = cv2.imread(grid_path, cv2.IMREAD_GRAYSCALE)
original_image = cv2.imread(original_path)

# Vízszintes és függőleges vonalak detektálása a rácson
horizontal_lines = cv2.reduce(grid_image, 1, cv2.REDUCE_MAX)  # Soronként maximumot néz
vertical_lines = cv2.reduce(grid_image, 0, cv2.REDUCE_MAX)    # Oszloponként maximumot néz

# Vonalak pozícióinak megtalálása
horizontal_positions = np.where(horizontal_lines > 0)[0]
vertical_positions = np.where(vertical_lines > 0)[1]

# Tároló a kivágott cellák számára
cells = []

# Cellák kivágása a metszéspontok alapján
for i in range(len(horizontal_positions) - 1):
    for j in range(len(vertical_positions) - 1):
        # Határok meghatározása
        y_start = horizontal_positions[i]
        y_end = horizontal_positions[i + 1]
        x_start = vertical_positions[j]
        x_end = vertical_positions[j + 1]

        # Kivágás az eredeti képből
        cell = original_image[y_start:y_end, x_start:x_end]
        cells.append(cell)

        # Opció: Mentés a celláknak
        cell_filename = f'cell_{i}_{j}.jpg'
        cv2.imwrite(cell_filename, cell)

print("Cellák sikeresen kivágva és elmentve.")