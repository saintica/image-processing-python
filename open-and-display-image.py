import matplotlib.pyplot as plt
import cv2
import numpy as np

matrix = cv2.imread('lena.png')  # membaca file gambar, diubah jadi array
matrix = cv2.cvtColor(matrix, cv2.COLOR_BGR2RGB)  # change BGR to RGB

# visualisasi
plt.imshow(matrix, cmap='gray', vmin=0, vmax=255)  # menampilkan gambar greyscale

# Menyimpan gambar
# cv2.imwrite('lena.jpg', matrix)
# -----------------
plt.show()
