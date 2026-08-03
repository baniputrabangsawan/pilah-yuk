# Pilah Yuk

> Foto sampahmu, biar AI yang bantu pilah.

Pilah Yuk adalah aplikasi web berbasis [Streamlit](https://streamlit.io/) yang membantu siswa, warga, dan pengelola sekolah mengenali **satu objek sampah** dari foto. Aplikasi menjalankan model klasifikasi gambar Keras secara lokal, menampilkan kategori serta tingkat keyakinan (*confidence*), lalu memberi rekomendasi pemilahan yang dapat ditindaklanjuti.

Aplikasi ini dibuat untuk Studi Kasus 2, Lingkungan: Mendukung Aksi Iklim Lokal, pada LKS Dikmen Ekshibisi Kecerdasan Artifisial (KA/AI) Tingkat Nasional 2026.

## Daftar Isi

- [Masalah dan tujuan](#masalah-dan-tujuan)
- [Fitur](#fitur)
- [Demo penggunaan](#demo-penggunaan)
- [Kategori sampah](#kategori-sampah)
- [Arsitektur](#arsitektur)
- [Struktur proyek](#struktur-proyek)
- [Teknologi](#teknologi)
- [Menjalankan aplikasi sendiri](#menjalankan-aplikasi-sendiri)
- [Menggunakan model sendiri](#menggunakan-model-sendiri)
- [Validasi dan batasan gambar](#validasi-dan-batasan-gambar)
- [Responsible AI dan privasi](#responsible-ai-dan-privasi)
- [Pengujian dan kualitas kode](#pengujian-dan-kualitas-kode)
- [Dokumentasi terkait](#dokumentasi-terkait)
- [Kontribusi](#kontribusi)

## Masalah dan Tujuan

Memilah sampah di rumah, sekolah, atau lingkungan sekitar sering kali sulit karena jenis material tidak selalu jelas. Kesalahan pemilahan dapat membuat material yang seharusnya dapat digunakan ulang atau didaur ulang menjadi terkontaminasi.

Pilah Yuk membantu pengguna melakukan langkah awal berikut:

1. Memotret atau mengunggah gambar satu objek sampah.
2. Mendapatkan prediksi kategori dari model AI lokal.
3. Membaca tingkat keyakinan dan alternatif prediksi model.
4. Menerima rekomendasi tindakan berbasis aturan untuk kategori tersebut.
5. Tetap memeriksa material, kondisi sampah, dan aturan pengelolaan setempat sebelum mengambil keputusan akhir.

Fokus MVP ini adalah klasifikasi gambar tunggal dan rekomendasi tindakan. Aplikasi ini **bukan** sistem pengangkutan sampah, pendeteksi banyak objek, kamera video real-time, atau penentu akhir cara membuang sampah.

## Fitur

- Unggah gambar JPEG/JPG atau PNG.
- Ambil foto langsung dari kamera perangkat yang didukung browser.
- Validasi gambar di memori: format, ukuran berkas, resolusi, dan orientasi EXIF.
- Inferensi menggunakan model Keras/TensorFlow lokal, tanpa API klasifikasi eksternal.
- Kategori utama, nilai *confidence*, dan maksimal tiga prediksi teratas.
- Peringatan jika *confidence* di bawah ambang awal 60%.
- Rekomendasi tindakan *rule-based* yang terpisah dari model AI agar mudah ditinjau.
- Pesan yang jelas saat model belum tersedia; aplikasi tidak membuat prediksi palsu.
- Gambar pengguna diproses di memori dan tidak disimpan permanen oleh aplikasi.

## Demo Penggunaan

1. Jalankan aplikasi dan buka alamat lokal yang ditampilkan Streamlit, biasanya `http://localhost:8501`.
2. Pilih **Unggah file** atau **Kamera**.
3. Masukkan foto dengan satu objek sampah dominan, pencahayaan cukup, dan latar yang tidak ramai.
4. Tekan **Analisis gambar**.
5. Baca kategori, *confidence*, prediksi lain, dan rekomendasi tindakan.
6. Jika muncul peringatan *Model belum cukup yakin*, ambil ulang foto dari sudut lain atau periksa material secara manual.

## Kategori Sampah

Model bawaan saat ini menggunakan enam kelas berikut. Nama kelas pada `labels.txt` dipetakan ke nama dan rekomendasi berbahasa Indonesia di aplikasi.

| Label model | Nama di aplikasi | Contoh tindakan awal |
|---|---|---|
| `cardboard` | Kardus | Lepaskan selotip, ratakan, dan jaga tetap kering. |
| `glass` | Kaca | Kosongkan wadah; bungkus pecahan dan beri tanda. |
| `metal` | Logam | Kosongkan, bilas secukupnya, keringkan, lalu pisahkan. |
| `paper` | Kertas | Pisahkan dari sampah basah dan jaga tetap kering. |
| `plastic` | Plastik | Kosongkan kemasan, kurangi volumenya, dan jangan dibakar. |
| `trash` | Sampah Residu | Bungkus dengan aman lalu buang ke tempat sampah residu. |

Rekomendasi tidak menggantikan aturan daerah. Tidak semua bank sampah, pengepul, atau fasilitas menerima material dan kondisi yang sama.

## Arsitektur

Pilah Yuk memisahkan antarmuka, inferensi model, pengolahan gambar, dan rekomendasi agar tiap bagian mudah diuji serta diaudit.

```text
Pengguna
  |
  | unggah file / ambil foto
  v
app.py (Streamlit: UI dan orkestrasi)
  |
  +--> src.utils.load_image()
  |      Validasi JPEG/PNG, batas ukuran, EXIF, RGB
  |
  +--> src.classifier.predict()
  |      Resize -> normalisasi -> model Keras lokal -> top 3 prediksi
  |
  +--> src.recommendations.get_recommendation()
         Rekomendasi tindakan berbasis aturan
  |
  v
Kategori, confidence, peringatan, dan rekomendasi untuk pengguna
```

### Alur data

1. Streamlit menerima gambar dari pengunggah berkas atau kamera.
2. `load_image()` membaca gambar sepenuhnya di memori, menolak berkas tidak valid, menerapkan orientasi EXIF, lalu mengonversinya ke RGB.
3. Saat pengguna menekan tombol analisis, model dan label lokal dimuat sekali per proses Streamlit melalui `st.cache_resource`.
4. `prepare_image_for_model()` menyesuaikan gambar dengan tinggi dan lebar input model, kemudian menormalisasi piksel dari `0..255` menjadi `-1..1`.
5. Model Keras menghasilkan skor setiap kelas. Aplikasi memeriksa kesesuaian jumlah skor dengan jumlah label dan mengurutkan tiga skor tertinggi.
6. Prediksi teratas ditampilkan bersama *confidence*. Nilai di bawah 60% memunculkan peringatan, tetapi hasil tetap tidak dianggap sebagai keputusan akhir.
7. Label kategori digunakan untuk mencari rekomendasi statis dari `src/recommendations.py`.

### Mengapa rekomendasi tidak memakai AI?

Rekomendasi tindakan menggunakan kamus aturan yang eksplisit, bukan model generatif atau API eksternal. Pendekatan ini membuat isi rekomendasi konsisten, dapat diperiksa, dan tetap dapat berjalan lokal. Model hanya bertugas mengklasifikasikan gambar; manusia tetap menentukan tindakan akhir sesuai kondisi benda dan fasilitas lokal.

## Struktur Proyek

```text
pilah-yuk/
├── app.py                     # Entry point Streamlit, UI, dan orkestrasi alur
├── requirements.txt           # Dependensi Python produksi
├── runtime.txt                # Runtime deployment bila diperlukan platform hosting
├── README.md                  # Dokumentasi utama proyek ini
├── DESIGN.md                  # Desain, scope, dan kebutuhan produk
├── DISCLOSURE.md              # Transparansi tools, model, data, dan bantuan coding
├── AGENTS.md                  # Aturan engineering proyek
│
├── assets/
│   └── styles.css             # Gaya visual antarmuka lokal
├── model/
│   ├── keras_model.h5         # Model Keras lokal hasil ekspor Teachable Machine
│   ├── labels.txt             # Label model, satu kelas per baris dan berurutan
│   ├── README.md              # Ketentuan file model
│   └── train_notes.md         # Catatan training dan evaluasi model
├── src/
│   ├── classifier.py          # Muat model/label, validasi shape, dan prediksi
│   ├── recommendations.py     # Rekomendasi pemilahan berbasis aturan
│   └── utils.py               # Validasi dan preprocessing gambar di memori
├── tests/
│   ├── test_classifier.py     # Uji logika classifier tanpa model produksi
│   ├── test_recommendations.py# Uji rekomendasi setiap kategori
│   └── test_utils.py          # Uji validasi serta preprocessing gambar
├── data/
│   └── dataset_source.md      # Status sumber, lisensi, dan penggunaan dataset
└── docs/
    └── RESPONSIBLE_AI.md      # Risiko, batasan, dan mitigasi AI
```

`converted_keras/` dapat muncul sebagai folder kerja sementara saat konversi ekspor model. Folder tersebut diabaikan oleh Git dan bukan lokasi model yang dibaca aplikasi.

## Teknologi

| Komponen | Teknologi | Kegunaan |
|---|---|---|
| Bahasa | Python 3.11 | Bahasa utama aplikasi. |
| Web UI | Streamlit | Antarmuka upload, kamera, hasil, dan rekomendasi. |
| Inferensi | TensorFlow 2.15.1 / Keras | Memuat dan menjalankan model `.h5` lokal. |
| Pengolahan numerik | NumPy `< 2` | Membentuk batch dan menangani skor prediksi. |
| Pengolahan gambar | Pillow | Membaca, memvalidasi, memutar EXIF, resize, dan RGB. |
| Quality control | pytest dan Ruff | Pengujian otomatis, lint, dan format kode. |
| Manajemen environment | uv | Menjalankan Python dan tool proyek secara konsisten. |
| Pembuatan model | Google Teachable Machine | Melatih dan mengekspor model klasifikasi gambar. |

## Menjalankan Aplikasi Sendiri

### Prasyarat

- Sistem operasi Linux, macOS, atau Windows dengan terminal.
- [Python 3.11](https://www.python.org/downloads/).
- [uv](https://docs.astral.sh/uv/getting-started/installation/) untuk mengelola environment dan menjalankan perintah.
- Model Keras lokal dan file label jika ingin melakukan analisis. Antarmuka tetap bisa dibuka tanpa model.

Periksa versi yang aktif:

```bash
uv --version
uv run python --version
```

Versi Python harus menunjukkan `3.11.x`.

### 1. Clone repositori

```bash
git clone <URL-REPOSITORI-ANDA>
cd pilah-yuk
```

Ganti `<URL-REPOSITORI-ANDA>` dengan URL GitHub proyek, misalnya `https://github.com/username/pilah-yuk.git`.

### 2. Instal dependensi

```bash
uv pip install -r requirements.txt
```

TensorFlow berukuran cukup besar dan biasanya menggunakan CPU secara default. Instalasi pertama dapat memerlukan waktu lebih lama dibanding dependensi lain.

### 3. Pastikan model tersedia

Untuk mengaktifkan tombol analisis, dua berkas berikut harus ada:

```text
model/keras_model.h5
model/labels.txt
```

Repositori dapat dibuka tanpa model. Dalam kondisi itu aplikasi menampilkan instruksi penempatan model dan menonaktifkan analisis, bukan menghasilkan klasifikasi acak.

Jika Anda memakai model sendiri, ikuti panduan [Menggunakan model sendiri](#menggunakan-model-sendiri).

### 4. Jalankan web

```bash
uv run streamlit run app.py
```

Buka alamat yang dicetak pada terminal, biasanya:

```text
http://localhost:8501
```

Untuk menghentikan server, tekan `Ctrl+C` pada terminal yang menjalankan Streamlit.

### Troubleshooting menjalankan aplikasi

| Gejala | Penyebab umum | Tindakan |
|---|---|---|
| `uv: command not found` | uv belum terinstal atau belum masuk `PATH`. | Instal uv sesuai dokumentasi resminya, tutup-buka terminal, lalu ulangi. |
| Python bukan 3.11 | Interpreter sistem berbeda dengan kebutuhan proyek. | Instal Python 3.11 dan jalankan ulang melalui `uv run`. |
| `ModuleNotFoundError` | Dependensi belum terinstal pada environment proyek. | Jalankan `uv pip install -r requirements.txt`. |
| Tombol analisis nonaktif | Gambar belum valid atau model/label tidak tersedia. | Unggah JPEG/PNG yang valid dan pastikan kedua berkas model ada. |
| `Model gagal dimuat` | File `.h5` rusak atau tidak kompatibel. | Ekspor ulang model Keras dari Teachable Machine dan gunakan TensorFlow 2.15.1. |
| Jumlah label tidak sama dengan output model | `labels.txt` tidak sinkron dengan model. | Perbaiki urutan/jumlah label sesuai ekspor model. |

## Menggunakan Model Sendiri

Bagian ini menjelaskan cara membuat model klasifikasi gambar di [Google Teachable Machine](https://teachablemachine.withgoogle.com/), mengekspornya ke Keras, dan memasangnya pada Pilah Yuk.

### Syarat kompatibilitas model

Classifier Pilah Yuk mendukung model dengan ketentuan berikut:

- File model berformat Keras HDF5: `keras_model.h5`.
- Model mempunyai tepat satu input gambar berbentuk `(batch, tinggi, lebar, 3)`.
- Input gambar harus tiga kanal RGB.
- Model menghasilkan satu baris skor berbentuk `(1, jumlah_kelas)`.
- Setiap output model memiliki tepat satu label pada `model/labels.txt` dengan urutan yang sama.
- Preprocessing aplikasi mengikuti pola ekspor Teachable Machine: resize ke ukuran input model dan normalisasi `(pixel / 127.5) - 1.0`.

Model multi-input, input non-RGB, atau output yang bukan satu vektor kelas belum didukung.

### A. Rencanakan kelas dan data

Sebelum membuka Teachable Machine, tentukan kelas yang benar-benar ingin dibedakan. Untuk menjaga kompatibilitas rekomendasi bawaan, gunakan enam label berikut:

```text
cardboard
metal
paper
plastic
trash
```

Anda boleh menggunakan kategori lain, tetapi kategori yang tidak ada di `src/recommendations.py` akan ditampilkan sebagai **Kategori Belum Dikenali** dengan rekomendasi aman yang umum. Tambahkan atau sesuaikan rekomendasi hanya bila kategori baru memang diperlukan.

Prinsip data yang disarankan:

- Gunakan jumlah gambar yang cukup dan relatif seimbang untuk setiap kelas.
- Sertakan variasi sudut, jarak, cahaya, latar, kondisi bersih/kotor, serta bentuk kemasan yang realistis.
- Gunakan satu objek utama pada tiap gambar, sesuai perilaku aplikasi.
- Jangan masukkan wajah, alamat, nomor kendaraan, dokumen, atau data pribadi.
- Pisahkan foto uji lokal yang tidak pernah dimasukkan saat training untuk evaluasi setelah ekspor.
- Catat sumber, tanggal akses, lisensi, jumlah gambar, dan perubahan data sebelum menggunakan dataset publik.

TrashNet dapat menjadi data awal, tetapi status sumber dan lisensinya harus diverifikasi sebelum digunakan atau didistribusikan. Lihat [`data/dataset_source.md`](data/dataset_source.md).

### B. Buat proyek Image Project

1. Buka [Teachable Machine](https://teachablemachine.withgoogle.com/).
2. Pilih **Get Started**.
3. Pilih **Image Project**.
4. Pilih **Standard image model**. Opsi ini sesuai untuk satu objek/kategori dominan dalam satu gambar.
5. Ubah nama setiap kelas sesuai kategori yang direncanakan, misalnya `plastic`, `glass`, `paper`, `trash`, `cardboard`, dan `metal`.
6. Pastikan setiap kelas mewakili material, bukan warna, merek, atau lokasi foto.

Urutan kelas di Teachable Machine penting. Urutan tersebut menjadi urutan output model dan harus dipertahankan pada `labels.txt`.

### C. Tambahkan gambar training

Untuk setiap kelas:

1. Pilih kelas yang dituju pada panel kiri.
2. Klik **Upload** untuk memasukkan kumpulan gambar, atau **Webcam** bila mengambil contoh langsung.
3. Periksa kembali apakah semua gambar pada kelas itu benar dan tidak tercampur kategori lain.
4. Ulangi pada setiap kelas sampai distribusi gambar cukup seimbang.

Hindari gambar duplikat atau gambar yang sangat mirip antara kelas. Foto produk yang sama dari rangkaian pemotretan yang sama sebaiknya tidak semuanya dipakai sebagai data latih, karena dapat membuat hasil evaluasi terlihat lebih baik dari kondisi nyata.

### D. Latih dan evaluasi model

1. Klik **Train Model**.
2. Mulai dengan konfigurasi bawaan Teachable Machine.
3. Setelah selesai, gunakan bagian **Preview** untuk mencoba gambar yang tidak dipakai saat mengumpulkan data training.
4. Uji setiap kelas, terutama sampah kotor, penyok, buram, berlatar ramai, tertutup sebagian, dan sampah campuran.
5. Jika model sering keliru, perbaiki data atau label terlebih dahulu. Tambahkan variasi contoh yang representatif, bukan hanya menambah gambar yang hampir sama.
6. Ulangi training dan catat hasilnya.

Jangan hanya melihat akurasi yang ditampilkan saat training. Uji dengan foto lokal yang benar-benar baru, lalu catat kelas yang sering tertukar, contoh salah klasifikasi, waktu inferensi, dan kasus *confidence* rendah.

### E. Ekspor model Keras

1. Dari halaman model yang sudah dilatih, klik **Export Model**.
2. Pilih tab atau opsi **TensorFlow**.
3. Pilih **Keras** sebagai format ekspor.
4. Klik **Download my model**.
5. Ekstrak file ZIP hasil unduhan.

Ekspor Keras Teachable Machine biasanya menyediakan `keras_model.h5` dan `labels.txt`. Gunakan berkas asli tersebut; jangan membuat model kosong, model dummy, atau menulis label berdasarkan tebakan.

> Jika tampilan Teachable Machine berubah, cari pilihan ekspor **TensorFlow** dan format **Keras**. Aplikasi ini memerlukan berkas `.h5`, bukan ekspor TensorFlow.js atau TFLite.

### F. Pasang model pada Pilah Yuk

Salin dua berkas dari hasil ekspor ke folder `model/` proyek dan gunakan nama berikut:

```text
model/keras_model.h5
model/labels.txt
```

Di Linux/macOS, dari folder proyek:

```bash
cp /lokasi/hasil-ekspor/keras_model.h5 model/keras_model.h5
cp /lokasi/hasil-ekspor/labels.txt model/labels.txt
```

Di Windows PowerShell:

```powershell
Copy-Item C:\lokasi\hasil-ekspor\keras_model.h5 model\keras_model.h5
Copy-Item C:\lokasi\hasil-ekspor\labels.txt model\labels.txt
```

Ganti lokasi contoh dengan folder hasil ekstraksi Anda. Mulai ulang Streamlit setelah mengganti model agar resource cache dimuat ulang.

### G. Periksa `labels.txt`

`labels.txt` berisi satu label per baris. Prefix angka dari Teachable Machine didukung dan akan dihapus otomatis oleh aplikasi. Contoh yang valid:

```text
0 Plastic
1 Glass
2 Paper
3 Trash
4 Cardboard
5 Metal
```

Contoh di atas menghasilkan label internal `plastic`, `glass`, `paper`, `trash`, `cardboard`, dan `metal`.

Aturan penting:

- Jangan mengubah urutan baris label setelah ekspor.
- Jumlah baris label harus sama dengan jumlah kelas output model.
- Label duplikat tidak diterima.
- Kapitalisasi tidak menjadi masalah karena aplikasi menormalkan label menjadi huruf kecil.
- Jika Anda mengubah urutan kelas atau jumlah kelas di Teachable Machine, ekspor ulang **kedua** berkas, bukan hanya `labels.txt`.

### H. Uji model yang dipasang

1. Jalankan aplikasi dengan `uv run streamlit run app.py`.
2. Unggah foto baru untuk setiap kelas, bukan hanya gambar yang dipakai saat training.
3. Pastikan kategori utama, urutan prediksi, dan rekomendasi sesuai label yang diharapkan.
4. Uji gambar dengan cahaya kurang, latar ramai, objek kotor, dan objek ambigu.
5. Catat tanggal, sumber data, lisensi, jumlah data per kelas, konfigurasi training, hasil uji, dan masalah pada [`model/train_notes.md`](model/train_notes.md).

Jika aplikasi menampilkan kesalahan jumlah label dan output model, pasang kembali pasangan `keras_model.h5` dan `labels.txt` dari ekspor yang sama.

### Memperbarui rekomendasi untuk kategori baru

Rekomendasi kategori bawaan didefinisikan di [`src/recommendations.py`](src/recommendations.py). Setiap kategori memiliki:

- nama tampilan;
- deskripsi;
- tindakan yang disarankan;
- peringatan;
- alternatif bila fasilitas lokal tidak tersedia;
- catatan keterbatasan fasilitas.

Untuk model dengan kelas baru, tambahkan rekomendasi yang lengkap dan dapat dipertanggungjawabkan pada `RECOMMENDATIONS`. Tanpa perubahan itu, kategori baru tetap dapat diprediksi tetapi menggunakan *fallback* aman yang umum.

## Validasi dan Batasan Gambar

Aplikasi menerima JPEG/JPG dan PNG. Berkas diproses hanya di memori dan tidak ditulis sebagai file pengguna.

| Aturan | Nilai |
|---|---|
| Format yang diterima | JPEG dan PNG |
| Ukuran berkas maksimum | 10 MB |
| Resolusi maksimum | 25.000.000 piksel |
| Kanal setelah pemrosesan | RGB, 3 kanal |
| Orientasi foto | Diperbaiki dari metadata EXIF bila tersedia |
| Resize | Mengikuti input shape model secara dinamis |
| Normalisasi | `(pixel / 127.5) - 1.0` |
| Bentuk batch model | `(1, tinggi, lebar, 3)` |

Hasil terbaik diperoleh dari foto dengan satu objek dominan, fokus tajam, pencahayaan memadai, dan latar yang sederhana. Aplikasi tidak dirancang untuk mendeteksi banyak objek dalam satu gambar.

## Responsible AI dan Privasi

AI pada Pilah Yuk adalah bantuan awal, bukan keputusan akhir. Nilai *confidence* mengukur tingkat keyakinan relatif model terhadap kelas outputnya, bukan bukti bahwa prediksi tersebut benar.

| Risiko | Mitigasi dalam aplikasi | Tindakan pengguna |
|---|---|---|
| Sampah campuran, kotor, buram, atau tertutup | Peringatan ditampilkan ketika confidence di bawah 60%. | Foto ulang atau periksa material secara manual. |
| Dataset tidak mewakili konteks Indonesia | Model dapat dilatih ulang dengan foto lokal yang relevan. | Uji model pada kemasan dan kondisi sampah lokal. |
| Terlalu percaya pada hasil AI | Disclaimer dan prediksi alternatif selalu tersedia. | Jadikan hasil sebagai pertimbangan, bukan keputusan final. |
| Perbedaan fasilitas setempat | Rekomendasi mencantumkan alternatif dan catatan fasilitas lokal. | Ikuti aturan pengelola sampah daerah Anda. |
| Privasi foto | Aplikasi tidak menyimpan gambar secara permanen. | Hindari memotret wajah atau data pribadi. |

Ambang 60% adalah nilai awal. Nilai tersebut perlu dievaluasi ulang berdasarkan hasil pengujian model nyata, terutama untuk data lokal dan kelas yang sering tertukar.

Untuk detail risiko dan batasan, baca [`docs/RESPONSIBLE_AI.md`](docs/RESPONSIBLE_AI.md). Transparansi tools, model, dataset, dan bantuan coding tersedia di [`DISCLOSURE.md`](DISCLOSURE.md).

## Pengujian dan Kualitas Kode

Jalankan pemeriksaan berikut dari root proyek sebelum membuat perubahan atau membagikan versi baru:

```bash
uv run ruff format --check .
uv run ruff check .
uv run pytest
```

Untuk menerapkan format Ruff bila diperlukan:

```bash
uv run ruff format .
```

Test unit tidak membutuhkan model produksi untuk memeriksa logika penting, termasuk validasi gambar, preprocessing, label, input shape, pengurutan prediksi, dan rekomendasi.

## Dokumentasi Terkait

- [`DESIGN.md`](DESIGN.md): tujuan produk, scope MVP, desain arsitektur, dan rencana data.
- [`DISCLOSURE.md`](DISCLOSURE.md): teknologi, status model/dataset, dan bantuan coding yang digunakan.
- [`docs/RESPONSIBLE_AI.md`](docs/RESPONSIBLE_AI.md): risiko AI, privasi, dan mitigasi.
- [`model/README.md`](model/README.md): ketentuan penyimpanan model lokal.
- [`model/train_notes.md`](model/train_notes.md): template catatan training dan evaluasi.
- [`data/dataset_source.md`](data/dataset_source.md): status audit sumber dan lisensi dataset.

## Kontribusi

1. Buat branch dari perubahan yang diperlukan.
2. Pertahankan pemisahan tanggung jawab: UI di `app.py`, classifier di `src/classifier.py`, rekomendasi di `src/recommendations.py`, dan pemrosesan gambar di `src/utils.py`.
3. Jangan menambahkan API klasifikasi eksternal atau menyimpan gambar pengguna secara permanen.
4. Jangan membuat prediksi pengganti ketika model tidak tersedia.
5. Tambahkan atau perbarui test untuk perubahan logika non-trivial.
6. Jalankan Ruff dan pytest sebelum membuka pull request.
7. Perbarui `DISCLOSURE.md`, `model/train_notes.md`, dan dokumentasi data bila model, dataset, tools, atau proses training berubah.

## Lisensi dan Atribusi

Lisensi repositori belum ditetapkan dalam proyek ini. Sebelum distribusi publik, tambahkan file lisensi yang sesuai dan verifikasi lisensi seluruh dataset, model, aset, serta dependensi yang digunakan.
