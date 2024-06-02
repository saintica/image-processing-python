import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Function to apply pixelation to the image
def pixelate_image(image, pixel_size):
    # Get the image dimensions
    height, width, _ = image.shape
    
    # Resize the image to a smaller size
    temp_image = cv2.resize(image, (width // pixel_size, height // pixel_size), interpolation=cv2.INTER_LINEAR)
    
    # Resize back to original size
    pixelated_image = cv2.resize(temp_image, (width, height), interpolation=cv2.INTER_NEAREST)
    
    return pixelated_image

# Function to update the image based on the slider value
def update(val):
    global pixel_size
    pixel_size = int(slider.val)

# Function to close the webcam and the window
def close(event):
    cap.release()
    plt.close()

# Initialize the webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Initial frame capture to get frame size
ret, frame = cap.read()
if not ret:
    print("Error: Could not read frame.")
    cap.release()
    exit()

# Convert the frame to RGB
frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

# Initialize pixel size
pixel_size = 10

# Initialize the plot
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.25)
ax_image = ax.imshow(frame)
ax.set_title("Webcam Image Pixelation")
ax.axis('off')

# Slider setup
axcolor = 'lightgoldenrodyellow'
ax_slider = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
slider = Slider(ax_slider, 'Pixel Size', 1, 30, valinit=pixel_size, valstep=1)
slider.on_changed(update)

# Connect the close event
fig.canvas.mpl_connect('close_event', close)

# Update the image continuously
def update_frame():
    while plt.fignum_exists(fig.number):
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pixelated_image = pixelate_image(frame, pixel_size)
        ax_image.set_data(pixelated_image)
        fig.canvas.draw_idle()
        plt.pause(0.01)

# Run the frame update in a loop
update_frame()

# Release the webcam
cap.release()
plt.close(fig)
