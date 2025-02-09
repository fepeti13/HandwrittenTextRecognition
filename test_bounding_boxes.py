import matplotlib.pyplot as plt
import cv2

image = cv2.imread("/home/fepeti13/Desktop/Research/Cropped/IMG_5762_b1.JPG")
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

points = [(357, 255), (618, 242), (623, 346), (362, 359)]

plt.imshow(image)

for x, y in points:
    plt.scatter(x, y, color="red", s=50)

plt.show()