import cv2
import numpy as np
from tkinter import Tk, Label, Scale, HORIZONTAL
from PIL import Image, ImageTk

def apply_contrast_adjustment(frame, contrast_value):
    # Convert the frame to grayscale
    gray_frame = np.dot(frame[...,:3], [0.2989, 0.5870, 0.1140])
    
    # Normalize the grayscale frame to range [0, 1]
    gray_frame = gray_frame / 255.0
    
    # Apply contrast adjustment
    gray_frame = np.clip(0.5 + contrast_value * (gray_frame - 0.5), 0, 1)
    
    # Scale back to range [0, 255]
    gray_frame = (gray_frame * 255).astype(np.uint8)
    
    # Convert the single-channel grayscale image back to a 3-channel image for display
    frame = np.stack((gray_frame,)*3, axis=-1)
    
    return frame

def update_frame():
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        return
    
    # Get the current contrast value from the slider
    contrast_value = contrast_slider.get() / 100.0
    
    # Apply contrast adjustment
    frame = apply_contrast_adjustment(frame, contrast_value)
    
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
root.title("Webcam Video with Contrast Adjustment")

# Initialize the video capture
cap = cv2.VideoCapture(0)

# Create and place the video label
video_label = Label(root)
video_label.pack()

# Create a contrast slider
contrast_slider = Scale(root, from_=-100, to=100, orient=HORIZONTAL, label="Contrast")
contrast_slider.set(0)
contrast_slider.pack()

# Start updating the frame
update_frame()

# Start the Tkinter main loop
root.mainloop()

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
