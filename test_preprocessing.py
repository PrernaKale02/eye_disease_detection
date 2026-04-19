from preprocessing import preprocess_image
import cv2

img = preprocess_image("sample_fundus.jpg")

print("Shape:", img.shape)
print("Min:", img.min())
print("Max:", img.max())

image = cv2.imread("sample_fundus.jpg")
print(image.shape)