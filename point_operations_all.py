import cv2
import numpy as np
from tkinter import Tk, Label, Radiobutton, IntVar
from PIL import Image, ImageTk

def apply_point_operation(frame, operation):
    # Convert the frame to grayscale first
    gray_frame = np.dot(frame[...,:3], [0.2989, 0.5870, 0.1140])
    
    # Perform point operations on the grayscale image
    if operation == 1:  # Brightness increase
        gray_frame = np.clip(gray_frame + 50, 0, 255)
    elif operation == 2:  # Brightness decrease
        gray_frame = np.clip(gray_frame - 50, 0, 255)
    elif operation == 3:  # Contrast increase
        gray_frame = np.clip(2 * gray_frame, 0, 255)
    elif operation == 4:  # Contrast decrease
        gray_frame = np.clip(0.5 * gray_frame, 0, 255)
    elif operation == 5:  # Invert colors
        gray_frame = 255 - gray_frame
    
    # Convert the single-channel grayscale image back to a 3-channel image for display
    frame = np.stack((gray_frame,)*3, axis=-1)
    
    return frame.astype(np.uint8)

def update_frame():
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        return
    
    # Apply selected point operation
    operation = var.get()
    frame = apply_point_operation(frame, operation)
    
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
root.title("Webcam Video with Point Operations")

# Initialize the video capture
cap = cv2.VideoCapture(0)

# Create and place the video label
video_label = Label(root)
video_label.pack()

# Create a variable to store the selected operation
var = IntVar()
var.set(1)

# Create radio buttons for selecting the point operation
operations = [
    ("Brightness Increase", 1),
    ("Brightness Decrease", 2),
    ("Contrast Increase", 3),
    ("Contrast Decrease", 4),
    ("Invert Colors", 5)
]

for text, value in operations:
    Radiobutton(root, text=text, variable=var, value=value).pack(anchor='w')

# Start updating the frame
update_frame()

# Start the Tkinter main loop
root.mainloop()

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
