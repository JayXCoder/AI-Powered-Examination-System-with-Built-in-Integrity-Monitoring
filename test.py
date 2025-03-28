import cv2

# Create a blank image (black screen)
image = cv2.imread("test.jpg")  # Try loading an image (optional)

# If no image is loaded, create a blank black image
if image is None:
    image = 255 * np.ones((300, 500, 3), dtype=np.uint8)  # White image

cv2.imshow("OpenCV Test Window", image)  # Display the window
cv2.waitKey(0)  # Wait for a key press
cv2.destroyAllWindows()  # Close the window
