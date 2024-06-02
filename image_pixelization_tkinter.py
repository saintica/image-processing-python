import cv2
import numpy as np
import tkinter as tk
from tkinter import Scale
from PIL import Image, ImageTk

# Function to apply pixelation to the image
def pixelate_image(image, pixel_size):
    # Get the image dimensions
    height, width, _ = image.shape
    
    # Resize the image to a smaller size
    temp_image = cv2.resize(image, (width // pixel_size, height // pixel_size), interpolation=cv2.INTER_LINEAR)
    
    # Resize back to original size
    pixelated_image = cv2.resize(temp_image, (width, height), interpolation=cv2.INTER_NEAREST)
    
    return pixelated_image

# Update function to read from webcam and apply pixelation
def update_frame():
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pixelated_image = pixelate_image(frame, pixel_size.get())
        
        img = Image.fromarray(pixelated_image)
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
    
    lmain.after(10, update_frame)

# Function to close the application
def on_closing():
    cap.release()
    root.destroy()

# Initialize the webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Create the main window
root = tk.Tk()
root.title("Webcam Image Pixelation")

# Create a label to display the video feed
lmain = tk.Label(root)
lmain.pack()

# Create a slider for adjusting pixel size
pixel_size = tk.Scale(root, from_=1, to=50, orient=tk.HORIZONTAL, label='Pixel Size')
pixel_size.set(10)
pixel_size.pack()

# Set the function to be called when the window is closed
root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the video update loop
update_frame()

# Start the Tkinter main loop
root.mainloop()
