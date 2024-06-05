import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def calculate_histogram(image):
    hist = cv2.calcHist([image], [0], None, [256], [0, 256])
    return hist

def equalize_histogram(image):
    # Calculate histogram
    hist, bins = np.histogram(image.flatten(), 256, [0, 256])
    
    # Calculate cumulative distribution function (CDF)
    cdf = hist.cumsum()
    cdf_normalized = cdf * hist.max() / cdf.max()
    
    # Mask all zero values and normalize the cdf
    cdf_m = np.ma.masked_equal(cdf, 0)
    cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.min())
    cdf = np.ma.filled(cdf_m, 0).astype('uint8')
    
    # Apply the cdf to get the equalized image
    equalized_image = cdf[image]
    return equalized_image

# Initialize webcam
cap = cv2.VideoCapture(0)

# Create the figure and the axes
fig, axs = plt.subplots(2, 2, figsize=(10, 8))

def update(frame):
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    if not ret:
        return
    
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Apply histogram equalization from scratch
    equalized = equalize_histogram(gray)
    
    # Calculate histograms
    original_hist = calculate_histogram(gray)
    equalized_hist = calculate_histogram(equalized)
    
    # Clear previous plots
    for ax in axs.flatten():
        ax.clear()
    
    # Display original image
    axs[0, 0].imshow(gray, cmap='gray')
    axs[0, 0].set_title('Original Image')
    axs[0, 0].axis('off')
    
    # Display equalized image
    axs[0, 1].imshow(equalized, cmap='gray')
    axs[0, 1].set_title('Equalized Image')
    axs[0, 1].axis('off')
    
    # Plot original histogram
    axs[1, 0].plot(original_hist, color='black')
    axs[1, 0].set_title('Original Histogram')
    axs[1, 0].set_xlim([0, 256])
    axs[1, 0].set_xlabel('Pixel Value')
    axs[1, 0].set_ylabel('Frequency')
    
    # Plot equalized histogram
    axs[1, 1].plot(equalized_hist, color='black')
    axs[1, 1].set_title('Equalized Histogram')
    axs[1, 1].set_xlim([0, 256])
    axs[1, 1].set_xlabel('Pixel Value')
    axs[1, 1].set_ylabel('Frequency')
    
    # Redraw the plots
    plt.tight_layout()
    fig.canvas.draw()

ani = FuncAnimation(fig, update, interval=50)

plt.show()

# Release the capture and destroy all windows after closing the plot window
cap.release()
cv2.destroyAllWindows()
