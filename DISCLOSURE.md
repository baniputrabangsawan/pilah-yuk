# Disclosure

## Tools dan Library

- Python 3.11
- Streamlit untuk antarmuka web
- TensorFlow/Keras untuk inferensi model lokal
- NumPy dan Pillow untuk preprocessing gambar
- pytest dan Ruff untuk quality control
- OpenCode dengan model `cx/gpt-5.6-sol` membantu perencanaan, implementasi kode,
  pengujian, dan dokumentasi awal. Tim tetap perlu meninjau dan memahami hasilnya.

## Model dan Dataset

Lokasi model yang didukung adalah `model/keras_model.h5`, dengan label di
`model/labels.txt`. Model belum disertakan saat implementasi awal sehingga aplikasi tidak
menghasilkan prediksi sampai model asli tersedia.

Model direncanakan diekspor dari Google Teachable Machine. TrashNet direncanakan sebagai
sumber data awal, tetapi sumber, lisensi, versi, pembagian data, dan hasil evaluasinya harus
dicatat sebelum klaim penggunaan final. Foto lokal tim harus bebas wajah dan data pribadi.

## Keterbatasan

Dataset luar negeri mungkin tidak mewakili sampah Indonesia. Sampah campuran, kotor,
tertutup, atau berlatar ramai dapat salah diklasifikasikan. Confidence ditampilkan untuk
transparansi dan bukan jaminan kebenaran. Keputusan akhir tetap pada pengguna.
