# meeting3 point operation

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from tkinter import filedialog, messagebox
import cv2
import numpy as np

# membuat window
wx = 12.5   # lebar
wy = 5      # tinggi
wr = wx/wy  # aspect ratio

fig = plt.figure(figsize=(wx, wy))
fig.canvas.manager.set_window_title("Image GUI")

a = 0.12/wr
b = 0.3
w = 0.65/wr
h = 0.6
# area gambar asli
axImg = fig.add_axes([a, b, w, h])
axImg.set_title('Gambar Asli')

# area gambar grayscale
axGray = fig.add_axes([w+2*a, b, w, h])

# area gambar hasil
axHis = fig.add_axes([2*w+3*a, b, w, h])

# tombol buka gambar
opax = plt.axes([a, 0.1, w, 0.08])
opBtn = Button(opax, "Buka Gambar")

# buat slider
slax = plt.axes([w+2*a, 0.1, w, 0.08])
sldr = Slider(slax, "", -200, 200, 0, color='red')

slab = plt.axes([2*w+3*a, 0.1, w, 0.08])
sldb = Slider(ax=slab, label="bin", valmin=1, valinit=125,
              valmax=256, valstep=1, color='g')

# fungsi untuk buka gambar


def bukagambar(event):
    global img, img0
    imgFile = filedialog.askopenfilename(initialfile='lena.jpg')
    img = cv2.imread(imgFile)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    axImg.imshow(img, cmap='gray')
    # ubah color ke gray
    img0 = (0.3 * img[:, :, 0] + 0.59 * img[:, :, 1] +
            0.11 * img[:, :, 2]) . astype(np.uint8)
    axGray.imshow(img0, cmap='gray')
    axImg.axis("off")
    axGray.axis("off")
    # tampilkan histogram
    histogram(img_=img0)

    sldr.set_val(0)
    plt.pause(.001)


# fungsi untuk slider


def atur(event):
    global img1
    val_ = sldr.val
    # print(val_)
    try:
        img1 = img0 + val_
        img1 = np.where(img1 > 255, 255, np.where(
            img1 <= 0, 0, img1)).astype(np.uint8)

        axGray.clear()
        axGray.imshow(img1, cmap='gray')
        axGray.set_title('Gambar Grayscale')
        axGray.axis("off")

        # tampilkan histogram
        histogram(img1)
        plt.pause(.001)

    except NameError:
        messagebox.showerror('Error!', 'Gambar grayscale tidak ditemukan!')


# fungsi untuk membuat histogram

def histogram(img_, bins=256):
    # histo = cv2.calcHist([img0], [0], None, [256], [0, 255])

    axHis.clear()
    # axHis.plot(histo, color='k')
    axHis.hist(img_.flatten(), bins=bins, range=(0, 256))
    axHis.set_xlabel('Nilai pixel')
    axHis.set_ylabel('Frequency')
    axHis.set_title('Histogram')
    plt.pause(0.001)


"""def histogramwarna(imgrgb):
    axHis.clear()

    warna = ('r', 'g', 'b')

    for i, w in enumerate(warna):
        histo = cv2.calcHist([imgrgb], [i], None, [256], [0, 255])
        axHis.plot(histo, color=w)"""


def sethistobin(event):
    bins = sldb.val
    histogram(img_=img1, bins=bins)


opBtn.on_clicked(bukagambar)
sldr.on_changed(atur)
sldb.on_changed(sethistobin)
# show
plt.show()
