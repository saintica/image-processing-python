import cv2
import numpy as np

# Function to apply pixelation
def pixelate_area(img, center, radius, pixel_size=10):
    # Create mask with the same dimensions as the image
    mask = np.zeros_like(img)
    
    # Draw a filled circle on the mask
    cv2.circle(mask, center, radius, (1, 1, 1), -1)
    
    # Apply pixelation only within the circle
    output = img.copy()
    x0, y0 = max(center[0] - radius, 0), max(center[1] - radius, 0)
    x1, y1 = min(center[0] + radius, img.shape[1]), min(center[1] + radius, img.shape[0])
    
    for y in range(y0, y1, pixel_size):
        for x in range(x0, x1, pixel_size):
            if np.sqrt((x - center[0])**2 + (y - center[1])**2) < radius:
                x_end = min(x + pixel_size, img.shape[1])
                y_end = min(y + pixel_size, img.shape[0])
                region = img[y:y_end, x:x_end]
                color = region.mean(axis=(0, 1), dtype=int)
                output[y:y_end, x:x_end] = color
                
    return output

# Mouse callback function to update the position of the circle's center
def update_center(event, x, y, flags, param):
    global center
    if event == cv2.EVENT_MOUSEMOVE:
        center = (x, y)

# Initialize the center of the circle
center = (0, 0)

# Open the webcam
cap = cv2.VideoCapture(0)

# Create a window and set the mouse callback function
cv2.namedWindow("Pixellated Video")
cv2.setMouseCallback("Pixellated Video", update_center)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Radius of the circle
    radius = 50  # You can adjust this value
    
    # Apply pixelation
    pixellated_frame = pixelate_area(frame, center, radius)
    
    # Display the frame
    cv2.imshow("Pixellated Video", pixellated_frame)
    
    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and destroy all windows
cap.release()
cv2.destroyAllWindows()
