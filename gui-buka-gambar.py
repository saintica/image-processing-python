import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider
from tkinter import filedialog
import cv2


# membuat window
wx = 8          # lebar
wy = 3          # tinggi
wr = wx / wy    # aspect ratio

fig = plt.figure(figsize= (wx, wy))
fig.canvas.manager.set_window_title("Image GUI")

# axis untuk menampilkan gambar

a = 0.1 / wr
b = 0.3
w = 0.7 / wr
h = 0.6

# axis gambar asli
axImg = fig.add_axes( [a, b, w, h] )
axImg.axis('off')

# axis grayscale
axGray = fig.add_axes( [2*a + w, b, w, h] )
axGray.axis('off')

# axis buat gambar ter-edit
axEdit = fig.add_axes( [3*a + 2*w, b, w, h] )
axEdit.axis('off')

# tombol buka gambar
axOp = plt.axes( [a, 0.1, w, 0.08] )
btnOp = Button(axOp, "Buka Gambar")


# slider
axsld = plt.axes( [3*a+2*w, 0.1, w, 0.05] )
sldr = Slider(ax=axsld, label="", valmin=0, valmax=100, valinit=0, valstep=1, color='b')

# fungsi untuk buka gambar
def bukaGambar(e):
    global imgray
    imgFile = filedialog.askopenfilename(initialfile='lena.png')
    img = cv2.imread(imgFile)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    axImg.imshow(img, cmap='gray', vmin=0, vmax=255)
    
    # convert ke grayscale    
    imgray = 0.3 * img[:, :, 0] + 0.6 * img[:, :, 1] + 0.1 * img[:, :, 2]
    
    axGray.imshow(imgray, cmap='gray', vmin=0, vmax=255)    
    axEdit.imshow(imgray, cmap='gray', vmin=0, vmax=255)
    
    plt.pause(0.01)

#fungsi slider

def brightness(e):
    val = sldr.val
    imge = imgray + val
    
    axEdit.clear()
    axEdit.axis('off')
    axEdit.imshow(imge, cmap='gray', vmin=0, vmax=255)
    plt.pause(0.01)


btnOp.on_clicked(bukaGambar)
sldr.on_changed(brightness)

plt.show()
