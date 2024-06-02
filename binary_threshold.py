import cv2
import numpy as np
from tkinter import Tk, Label, Scale, HORIZONTAL
from PIL import Image, ImageTk

def apply_clamping_and_binarize(frame, lower_threshold, upper_threshold):
    # Convert the frame to grayscale
    gray_frame = np.dot(frame[...,:3], [0.2989, 0.5870, 0.1140])
    
    # Normalize the grayscale frame to range [0, 1]
    gray_frame = gray_frame / 255.0
    
    # Apply clamping
    clamped_frame = np.clip(gray_frame, lower_threshold / 100.0, upper_threshold / 100.0)
    
    # Binarize the image: pixels within the range are black (0), others are white (1)
    binary_frame = np.where((clamped_frame > lower_threshold / 100.0) & (clamped_frame < upper_threshold / 100.0), 0, 1)
    
    # Scale back to range [0, 255]
    binary_frame = (binary_frame * 255).astype(np.uint8)
    
    # Convert the single-channel binary image back to a 3-channel image for display
    frame = np.stack((binary_frame,)*3, axis=-1)
    
    return frame

def update_frame():
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        return
    
    # Get the current threshold values from the sliders
    lower_threshold = lower_threshold_slider.get()
    upper_threshold = upper_threshold_slider.get()
    
    # Ensure that lower_threshold is not greater than upper_threshold
    if lower_threshold > upper_threshold:
        lower_threshold = upper_threshold_slider.get()
    
    # Apply clamping and binarization
    frame = apply_clamping_and_binarize(frame, lower_threshold, upper_threshold)
    
    # Convert the frame to an image format suitable for Tkinter
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(image=img)
    video_label.imgtk = imgtk
    video_label.configure(image=imgtk)
    
    # Schedule the next update
    video_label.after(10, update_frame)

# Initialize the main window
root = Tk()
root.title("Webcam Video with Clamping and Binarization")

# Initialize the video capture
cap = cv2.VideoCapture(0)

# Create and place the video label
video_label = Label(root)
video_label.pack()

# Create lower threshold slider
lower_threshold_slider = Scale(root, from_=0, to=100, orient=HORIZONTAL, label="Lower Threshold")
lower_threshold_slider.set(0)
lower_threshold_slider.pack()

# Create upper threshold slider
upper_threshold_slider = Scale(root, from_=0, to=100, orient=HORIZONTAL, label="Upper Threshold")
upper_threshold_slider.set(100)
upper_threshold_slider.pack()

# Start updating the frame
update_frame()

# Start the Tkinter main loop
root.mainloop()

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
