import cv2

# Fungsi utama
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

        # Tampilkan frame di window
        cv2.imshow('Webcam', frame)

        # Tunggu 1ms dan periksa apakah tombol 'q' ditekan untuk keluar
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Lepaskan objek capture dan tutup semua window
    cap.release()
    cv2.destroyAllWindows()

# Panggil fungsi utama
if __name__ == "__main__":
    main()
