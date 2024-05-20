import cv2
import numpy as np

def main():
    # Membuka koneksi ke webcam (0 adalah ID perangkat default)
    cap = cv2.VideoCapture(0)

    # Periksa apakah webcam berhasil dibuka
    if not cap.isOpened():
        print("Error: Tidak dapat membuka webcam.")
        return

    while True:
        # Baca frame dari webcam
        ret, frame = cap.read()

        # Periksa apakah frame berhasil dibaca
        if not ret:
            print("Error: Tidak dapat membaca frame.")
            break

        # Ubah ukuran frame ke 150x100
        frame_resized = cv2.resize(frame, (150, 100))

        # Pisahkan channel RGB
        B, G, R = cv2.split(frame_resized)

        # Buat citra untuk masing-masing channel dengan menampilkan channel yang diinginkan
        red_channel = cv2.merge((np.zeros_like(B), np.zeros_like(G), R))
        green_channel = cv2.merge((np.zeros_like(B), G, np.zeros_like(R)))
        blue_channel = cv2.merge((B, np.zeros_like(G), np.zeros_like(R)))

        # Menyusun citra asli dan citra channel dalam satu jendela
        top_row = np.hstack((frame_resized, red_channel))
        bottom_row = np.hstack((green_channel, blue_channel))
        combined_image = np.vstack((top_row, bottom_row))

        # Tampilkan citra gabungan di jendela
        cv2.imshow('Original and RGB Channels (150x100)', combined_image)

        # Tunggu 1ms dan periksa apakah tombol 'q' ditekan untuk keluar
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Lepaskan objek capture dan tutup semua window
    cap.release()
    cv2.destroyAllWindows()

# Panggil fungsi utama
if __name__ == "__main__":
    main()
