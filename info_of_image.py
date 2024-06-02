import cv2
import numpy as np
from tkinter import Tk, Label
from PIL import Image, ImageTk

def calculate_brightness_contrast_dynamic_range(frame):
    # Convert the frame to grayscale for analysis
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Calculate brightness (mean pixel value)
    brightness = np.mean(gray_frame)
    
    # Calculate contrast (standard deviation of pixel values)
    contrast = np.std(gray_frame)
    
    # Calculate dynamic range (difference between max and min pixel values)
    dynamic_range = np.max(gray_frame) - np.min(gray_frame)
    
    return brightness, contrast, dynamic_range

def update_frame():
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        return
    
    # Calculate brightness, contrast, and dynamic range
    brightness, contrast, dynamic_range = calculate_brightness_contrast_dynamic_range(frame)
    
    # Update the labels with the calculated values
    brightness_label.config(text=f"Brightness: {brightness:.2f}")
    contrast_label.config(text=f"Contrast: {contrast:.2f}")
    dynamic_range_label.config(text=f"Dynamic Range: {dynamic_range}")
    
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
root.title("Webcam Video with Brightness, Contrast, and Dynamic Range")

# Initialize the video capture
cap = cv2.VideoCapture(0)

# Create and place the labels for displaying the video and information
video_label = Label(root)
video_label.pack()

brightness_label = Label(root, text="Brightness: 0.00")
brightness_label.pack()

contrast_label = Label(root, text="Contrast: 0.00")
contrast_label.pack()

dynamic_range_label = Label(root, text="Dynamic Range: 0")
dynamic_range_label.pack()

# Start updating the frame
update_frame()

# Start the Tkinter main loop
root.mainloop()

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
