import cv2
import numpy as np
from tkinter import Tk, Label, Scale, HORIZONTAL, Frame
from PIL import Image, ImageTk

def apply_clamping_and_binarize(frame, lower_threshold, upper_threshold):
    # Convert the frame to grayscale
    gray_frame = np.dot(frame[...,:3], [0.2989, 0.5870, 0.1140])
    
    # Normalize the grayscale frame to range [0, 1]
    gray_frame = gray_frame / 255.0
    
    # Apply clamping
    clamped_frame = np.clip(gray_frame, lower_threshold / 100.0, upper_threshold / 100.0)
    
    # Binarize the image: pixels within the range are black (0), others are white (1)
    binary_frame = np.where((clamped_frame > lower_threshold / 100.0) & (clamped_frame < upper_threshold / 100.0), 255, 0).astype(np.uint8)
    
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
    thresholded_frame = apply_clamping_and_binarize(frame, lower_threshold, upper_threshold)
    
    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Convert the grayscale frame to an image format suitable for Tkinter
    gray_img = Image.fromarray(gray_frame)
    gray_imgtk = ImageTk.PhotoImage(image=gray_img)
    gray_label.imgtk = gray_imgtk
    gray_label.configure(image=gray_imgtk)
    
    # Convert the thresholded frame to an image format suitable for Tkinter
    thresholded_img = Image.fromarray(thresholded_frame)
    thresholded_imgtk = ImageTk.PhotoImage(image=thresholded_img)
    thresholded_label.imgtk = thresholded_imgtk
    thresholded_label.configure(image=thresholded_imgtk)
    
    # Schedule the next update
    root.after(10, update_frame)

# Initialize the main window
root = Tk()
root.title("Webcam Video with Clamping and Binarization")

# Initialize the video capture
cap = cv2.VideoCapture(0)

# Create a frame to hold the left and right sections
frame = Frame(root)
frame.pack()

# Create and place the grayscale image label on the left side
gray_label = Label(frame)
gray_label.pack(side="left", padx=10, pady=10)

# Create and place the thresholded image label on the right side
thresholded_label = Label(frame)
thresholded_label.pack(side="right", padx=10, pady=10)

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
