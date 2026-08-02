Anda adalah senior Python engineer, machine learning application engineer, dan software architect. Buat rencana implementasi lengkap untuk proyek Pilah Yuk. Jangan melakukan setup, jangan menulis atau mengubah kode, jangan memasang dependency, dan jangan mengubah file proyek. Tugas Anda hanya menganalisis kondisi proyek lalu menghasilkan planning yang terstruktur dan dapat digunakan pada tahap implementasi berikutnya.

Lokasi proyek
/home/baniputrabangsawan/Projects/pilah-yuk
Kondisi saat ini
Sistem operasi: Ubuntu Linux x86_64.
uv sudah terpasang.
Python 3.11 sudah terpasang melalui uv.
File .python-version sudah tersedia.
Virtual environment tersedia di .venv.
File berikut sudah dibuat:
DESIGN.md
AGENT.md
Kedua file tersebut merupakan sumber utama kebutuhan dan aturan proyek.
Proyek menggunakan Python, Streamlit, TensorFlow/Keras, dan model lokal hasil ekspor Google Teachable Machine.
Aplikasi harus dapat berjalan lokal tanpa API klasifikasi eksternal.
Gambar pengguna tidak boleh disimpan permanen.
Aturan wajib
Masuk ke direktori proyek:
cd /home/baniputrabangsawan/Projects/pilah-yuk
Baca seluruh isi:
DESIGN.md
AGENT.md
Periksa struktur dan file proyek yang sudah tersedia.
Gunakan pemeriksaan read-only jika diperlukan, seperti:
pwd
ls -la
find . -maxdepth 3 -type f | sort
git status --short 2>/dev/null || true
uv --version
uv run python --version
Jangan menjalankan tindakan yang mengubah sistem atau proyek.
Dilarang menjalankan:
uv pip install
pip install
apt install
sudo
rm
mv
git add
git commit
git push
ruff format
pembuatan atau perubahan file
Jangan membuat model palsu, data palsu, hasil prediksi palsu, atau asumsi bahwa file model sudah tersedia.
Jangan membuat fitur di luar scope MVP yang dijelaskan dalam DESIGN.md.
Jika DESIGN.md dan AGENT.md memiliki ketentuan yang berbeda, catat konflik tersebut dalam planning. Jangan memilih secara diam-diam.
Jangan meminta konfirmasi untuk keputusan planning yang bisa dianalisis dari file proyek.
Tujuan planning

Buat rencana teknis untuk membangun MVP aplikasi Pilah Yuk, yaitu aplikasi klasifikasi sampah berbasis gambar dengan alur:

Pengguna mengunggah atau memotret gambar
→ sistem memvalidasi gambar
→ gambar diproses di memori
→ model Keras lokal melakukan klasifikasi
→ sistem menampilkan kategori dan confidence score
→ sistem menampilkan peringatan jika confidence rendah
→ sistem memberikan rekomendasi tindakan berbasis aturan
→ pengguna tetap mengambil keputusan akhir

Kategori awal:

cardboard
glass
metal
paper
plastic
trash

Model yang nantinya digunakan:

model/keras_model.h5

Label model:

model/labels.txt
Teknologi utama

Planning harus mempertimbangkan:

Python 3.11
uv
Streamlit
TensorFlow 2.15.1
NumPy < 2
Pillow
pandas
scikit-learn
matplotlib
pytest
Ruff
Git
Google Teachable Machine

Jangan mengganti stack tersebut kecuali terdapat konflik nyata dari DESIGN.md atau AGENT.md. Jika ada konflik, jelaskan dampak dan alternatifnya.

Cakupan planning

Planning harus mencakup seluruh bagian berikut.

1. Ringkasan pemahaman proyek

Jelaskan secara singkat:

masalah yang diselesaikan;
target pengguna;
solusi utama;
batas scope MVP;
fitur yang berada di luar scope;
alasan penggunaan AI;
posisi manusia dalam pengambilan keputusan.
2. Audit kondisi awal

Catat:

file yang sudah tersedia;
file yang belum tersedia;
kondisi .venv;
versi Python;
status Git;
dependency yang sudah atau belum terpasang;
keberadaan model dan label;
ketidaksesuaian struktur proyek;
risiko menimpa pekerjaan yang sudah ada.

Jangan memperbaiki kondisi tersebut. Hanya dokumentasikan.

3. Arsitektur aplikasi

Rencanakan pemisahan tanggung jawab minimal:

app.py
src/classifier.py
src/recommendations.py
src/utils.py
model/
data/
docs/
tests/

Jelaskan tanggung jawab setiap file atau modul.

app.py harus fokus pada UI dan orkestrasi.

src/classifier.py harus fokus pada:

loading model;
loading labels;
deteksi input shape;
prediksi;
confidence score;
top predictions;
penanganan model yang belum tersedia.

src/utils.py harus fokus pada:

validasi file;
JPEG dan PNG;
EXIF orientation;
konversi RGB;
resize;
normalisasi;
pembentukan batch NumPy;
pemrosesan di memori.

src/recommendations.py harus fokus pada rekomendasi rule-based yang dapat diaudit.

4. Struktur direktori target

Tampilkan struktur direktori yang direncanakan.

Pertahankan lokasi file berikut:

DESIGN.md
AGENT.md

Jangan merencanakan pemindahan atau penimpaan kedua file tersebut.

Jangan merencanakan pembuatan file kosong:

model/keras_model.h5
5. Dependency plan

Buat rencana dependency yang mencantumkan:

dependency produksi;
dependency pengujian;
fungsi setiap dependency;
kompatibilitas Python;
kompatibilitas TensorFlow dan NumPy;
dependency yang tidak diperlukan;
risiko ukuran instalasi TensorFlow;
penggunaan CPU tanpa CUDA.

Pertahankan:

TensorFlow == 2.15.1
NumPy < 2
Python 3.11
6. Rencana setup environment

Tuliskan urutan setup secara konseptual, bukan langsung mengeksekusinya:

validasi folder proyek;
validasi .venv;
validasi interpreter;
validasi dependency;
instalasi dependency;
verifikasi import;
verifikasi TensorFlow;
verifikasi Streamlit.

Setiap tahap harus memiliki:

tujuan;
pemeriksaan;
kondisi berhasil;
kemungkinan error;
strategi pemulihan.
7. Rencana implementasi utilitas gambar

Rencanakan fungsi seperti:

load_image(...)
prepare_image_for_model(...)

Jelaskan:

input;
output;
validasi;
exception;
target size dinamis;
normalisasi -1 sampai 1;
output shape (1, height, width, 3);
output dtype float32;
pencegahan penyimpanan file pengguna.
8. Rencana classifier

Rencanakan classifier dengan ketentuan:

lazy loading;
model lokal;
label lokal;
deteksi model.input_shape;
tidak hardcode ukuran model;
pembersihan prefix nomor label;
validasi jumlah label dan output model;
confidence score;
maksimal tiga kandidat teratas;
error khusus ketika model belum tersedia;
tidak menghasilkan prediksi dummy;
model tidak dimuat berulang kali;
integrasi aman dengan st.cache_resource.

Rencanakan struktur hasil menggunakan dataclass, misalnya:

@dataclass(frozen=True)
class Prediction:
    category: str
    confidence: float
    top_predictions: list[tuple[str, float]]
9. Rencana rekomendasi rule-based

Rencanakan rekomendasi untuk:

cardboard
glass
metal
paper
plastic
trash

Setiap rekomendasi minimal memiliki:

nama Indonesia;
deskripsi;
tindakan utama;
peringatan;
alternatif tindakan lokal;
catatan keterbatasan fasilitas.

Jangan menjadikan bank sampah atau fasilitas daur ulang sebagai satu-satunya solusi.

Pertimbangkan daerah kecil yang belum memiliki fasilitas daur ulang memadai.

10. Rencana antarmuka Streamlit

Rencanakan alur UI:

judul dan tagline;
penjelasan aplikasi;
uploader gambar;
input kamera;
preview;
tombol analisis;
indikator loading;
kategori hasil;
confidence score;
tiga prediksi teratas;
warning confidence rendah;
rekomendasi;
disclaimer Responsible AI;
pemberitahuan model belum tersedia;
disclosure tools dan model.

Aplikasi harus tetap dapat dibuka ketika model belum tersedia.

Dalam kondisi tersebut, aplikasi hanya boleh menampilkan instruksi pemasangan model. Jangan membuat hasil acak.

11. Confidence threshold

Rencanakan penggunaan threshold awal:

60%

Jelaskan:

arti confidence;
bahwa confidence bukan jaminan kebenaran;
kondisi confidence rendah;
tindakan UI ketika confidence rendah;
kebutuhan evaluasi ulang threshold setelah pengujian model lokal.
12. Responsible AI

Planning harus mencakup:

bias dataset;
perbedaan sampah luar negeri dan Indonesia;
salah klasifikasi;
sampah kotor atau campuran;
ketergantungan pengguna terhadap AI;
gambar yang mengandung wajah atau data pribadi;
penyimpanan gambar;
transparansi confidence;
keterbatasan fasilitas lokal;
larangan klaim lingkungan tanpa metode terverifikasi;
peran keputusan manusia;
disclosure model, dataset, tools, dan coding assistant.

Buat tabel:

Risiko
Dampak
Kemungkinan
Mitigasi teknis
Mitigasi UI
Validasi manusia

13. Rencana data dan model

Buat planning untuk:

penggunaan dataset TrashNet;
pemeriksaan sumber dan lisensi dataset;
penambahan foto sampah lokal Indonesia;
standar pengambilan gambar;
proses pelabelan;
validasi label oleh anggota tim;
pembagian data training, validation, dan test;
pencegahan data leakage;
pencatatan distribusi jumlah gambar setiap kelas;
pengujian model pada gambar yang tidak digunakan saat training;
dokumentasi proses training;
ekspor model dari Google Teachable Machine;
sinkronisasi urutan label dengan output model;
penyimpanan model di model/keras_model.h5;
penyimpanan label di model/labels.txt;
evaluasi keterbatasan model.

Gunakan kategori awal:

cardboard
glass
metal
paper
plastic
trash

Planning harus menjelaskan bahwa dataset luar negeri kemungkinan tidak sepenuhnya merepresentasikan sampah yang umum di Indonesia, seperti:

bungkus makanan lokal;
gelas plastik kotor;
kantong kresek;
kardus basah;
kaleng penyok;
sampah campuran;
kemasan multilapis;
sampah dengan latar belakang kompleks.

Rencanakan pengujian tambahan menggunakan foto lokal yang diambil tim sendiri tanpa menampilkan wajah, nomor kendaraan, alamat, dokumen, atau informasi pribadi.

Jangan mengasumsikan model telah tersedia. Catat status aktual berdasarkan pemeriksaan proyek.

14. Rencana evaluasi model

Buat planning pengukuran model yang mencakup:

accuracy;
precision;
recall;
F1-score;
confusion matrix;
performa setiap kelas;
waktu inferensi;
confidence distribution;
jumlah kasus confidence rendah;
kesalahan yang sering terjadi;
pengujian gambar lokal;
pengujian gambar buram;
pengujian pencahayaan rendah;
pengujian latar belakang ramai;
pengujian objek sebagian tertutup;
pengujian gambar yang bukan sampah.

Jangan hanya mengandalkan accuracy keseluruhan.

Planning harus menjelaskan cara mendeteksi:

kelas yang terlalu dominan;
model yang selalu memilih satu kategori;
overfitting;
data leakage;
ketidakseimbangan data;
label yang salah;
confidence tinggi pada prediksi yang salah.

Tetapkan target awal yang realistis, bukan klaim pasti:

Accuracy test set: target awal ≥ 70%
F1-score rata-rata: dievaluasi setelah training
Waktu inferensi lokal: target < 5 detik
Confidence rendah: harus ditandai
Prediksi tanpa model: dilarang

Tekankan bahwa target harus direvisi berdasarkan hasil pengujian nyata.

15. Rencana testing kode

Susun rencana unit test yang tidak membutuhkan model asli untuk seluruh test.

Minimal rencanakan:

tests/test_utils.py

Uji:

gambar JPEG valid;
gambar PNG valid;
gambar RGBA dikonversi ke RGB;
gambar grayscale dikonversi ke RGB;
file non-gambar ditolak;
file rusak ditolak;
preprocessing menghasilkan NumPy array;
dtype output adalah float32;
output memiliki batch dimension;
output shape sesuai target size;
hasil normalisasi berada pada rentang yang sesuai;
fungsi tidak menyimpan file ke disk.
tests/test_recommendations.py

Uji:

enam kategori memiliki rekomendasi;
output memiliki struktur konsisten;
kategori dengan huruf besar atau spasi dapat dinormalisasi jika direncanakan;
kategori tidak dikenal menghasilkan fallback aman;
rekomendasi tidak bergantung pada layanan daur ulang yang belum tentu tersedia;
peringatan pembakaran tersedia untuk kategori yang relevan.
tests/test_classifier.py

Rencanakan test menggunakan mock atau model kecil sintetis hanya untuk menguji logika kode, bukan untuk berpura-pura sebagai model kompetisi.

Uji:

model belum tersedia;
label belum tersedia;
file label kosong;
prefix angka label dibersihkan;
jumlah label tidak cocok dengan jumlah output;
input shape terdeteksi;
hasil prediksi diurutkan;
maksimal tiga prediksi teratas;
confidence dikonversi dengan benar;
model tidak dimuat berulang kali;
error ditampilkan dengan jelas.

Jangan memasukkan model palsu sebagai model produksi.

16. Rencana integration test

Rencanakan pengujian alur penuh:

Upload gambar
→ validasi
→ preview
→ preprocessing
→ model inference
→ hasil kategori
→ confidence
→ rekomendasi
→ disclaimer

Buat skenario:

aplikasi dijalankan tanpa model;
aplikasi dijalankan dengan model dan label valid;
model tersedia tetapi label tidak tersedia;
label tersedia tetapi model tidak tersedia;
jumlah label tidak sesuai output model;
gambar valid;
file bukan gambar;
gambar sangat besar;
gambar buram;
confidence di bawah threshold;
confidence di atas threshold;
pengguna memakai kamera;
pengguna mengganti gambar;
pengguna belum memilih gambar.

Planning harus memastikan aplikasi tidak crash pada setiap skenario.

17. Rencana quality control

Buat planning pemeriksaan kualitas menggunakan:

uv run ruff format --check .
uv run ruff check .
uv run pytest

Jelaskan:

fungsi Ruff;
fungsi pytest;
kondisi lulus;
cara menangani lint error;
cara menangani test gagal;
larangan mengabaikan error tanpa alasan;
larangan menambahkan # noqa secara sembarangan;
larangan menghapus test hanya agar pipeline lulus.

Rencanakan import test:

uv run python -c "import app; print('Import app: OK')"

Pastikan planning mempertimbangkan agar import app.py tidak menjalankan proses berat atau memuat model tanpa diperlukan.

18. Rencana smoke test Streamlit

Buat planning smoke test:

uv run streamlit run app.py \
  --server.headless true \
  --server.port 8501

Periksa:

server dapat dimulai;
tidak ada traceback;
halaman utama merespons;
aplikasi tetap terbuka tanpa model;
pesan model belum tersedia muncul dengan benar;
proses dapat dihentikan secara bersih;
tidak ada proses tertinggal di background.

Jelaskan bahwa smoke test hanya memeriksa aplikasi dapat dijalankan, bukan membuktikan akurasi model.

19. Rencana dokumentasi

Rencanakan file berikut tanpa mengubah DESIGN.md dan AGENT.md selama tahap planning:

README.md
DISCLOSURE.md
model/README.md
model/train_notes.md
data/dataset_source.md
docs/RESPONSIBLE_AI.md
docs/presentation_script.md
README.md

Rencanakan isi:

ringkasan proyek;
fitur MVP;
tech stack;
struktur folder;
persyaratan sistem;
setup menggunakan uv;
cara menjalankan aplikasi;
cara menjalankan test;
cara menjalankan Ruff;
cara memasang model;
troubleshooting;
batasan aplikasi;
peringatan bahwa hasil AI bukan keputusan akhir.
DISCLOSURE.md

Rencanakan disclosure:

Google Teachable Machine;
TensorFlow/Keras;
Streamlit;
TrashNet;
foto lokal tim;
Codex CLI;
coding assistant lain jika digunakan;
library open-source;
proses yang dikerjakan sendiri oleh tim;
keterbatasan model;
status model aktual.
model/train_notes.md

Rencanakan pencatatan:

tanggal training;
versi dataset;
jumlah gambar setiap kelas;
pembagian data;
konfigurasi training;
epoch;
augmentation;
hasil evaluasi;
masalah yang ditemukan;
versi model;
perubahan dari training sebelumnya.
data/dataset_source.md

Rencanakan:

nama dataset;
sumber;
lisensi;
tanggal akses;
jumlah data;
kategori;
modifikasi yang dilakukan;
sumber foto lokal;
persetujuan penggunaan;
batasan dataset.
20. Rencana Git

Buat planning penggunaan Git tanpa melakukan commit.

Rencanakan tahapan commit kecil:

chore: setup environment dan dependency
feat: tambah validasi dan preprocessing gambar
feat: tambah rekomendasi berbasis aturan
feat: tambah classifier model lokal
feat: tambah UI Streamlit
test: tambah unit dan integration test
docs: tambah disclosure dan responsible AI

Planning harus mempertimbangkan:

.venv tidak masuk Git;
secret tidak masuk Git;
model final diperiksa ukuran dan lisensinya;
dataset besar tidak dimasukkan tanpa alasan;
setiap commit harus memiliki satu tujuan jelas;
jangan melakukan push tanpa perintah pengguna;
periksa git diff sebelum commit.
21. Urutan implementasi yang direkomendasikan

Susun implementasi menjadi tahapan berikut.

Tahap 1 — Audit proyek
baca DESIGN.md;
baca AGENT.md;
periksa struktur;
periksa environment;
periksa dependency;
periksa model;
catat konflik.
Tahap 2 — Fondasi environment
validasi Python 3.11;
validasi .venv;
siapkan dependency;
verifikasi import;
siapkan Ruff dan pytest.
Tahap 3 — Utilitas gambar
validasi file;
load gambar;
EXIF orientation;
RGB;
resize;
normalisasi;
unit test.
Tahap 4 — Rekomendasi rule-based
buat struktur data;
isi rekomendasi enam kategori;
fallback aman;
unit test.
Tahap 5 — Classifier
lazy loading;
model path;
label path;
input shape;
inference;
top predictions;
error handling;
test dengan mock.
Tahap 6 — UI Streamlit
uploader;
kamera;
preview;
tombol analisis;
hasil;
confidence;
warning;
rekomendasi;
disclosure;
kondisi model belum tersedia.
Tahap 7 — Model dan dataset
audit dataset;
foto lokal;
training;
evaluasi;
ekspor;
integrasi;
pengujian nyata.
Tahap 8 — Responsible AI dan dokumentasi
risiko;
mitigasi;
disclosure;
dataset source;
training notes;
batasan.
Tahap 9 — Validasi akhir
Ruff;
pytest;
import test;
Streamlit smoke test;
pengujian manual;
pengecekan Git.

Untuk setiap tahap, tuliskan:

tujuan;
file yang terlibat;
hasil yang diharapkan;
dependency dengan tahap lain;
risiko;
kriteria selesai.
22. Prioritas fitur

Kelompokkan fitur menjadi:

P0 — Wajib untuk MVP
upload JPEG/PNG;
input kamera;
preview;
model lokal;
enam kategori;
confidence score;
top predictions;
warning confidence rendah;
rekomendasi rule-based;
error handling;
kondisi model belum tersedia;
disclaimer;
tidak menyimpan gambar;
disclosure dasar.
P1 — Setelah MVP stabil
riwayat lokal tanpa gambar;
statistik kategori;
ekspor hasil evaluasi;
dashboard sederhana;
pengujian model lebih luas.
P2 — Di luar MVP awal
akun pengguna;
database cloud;
klasifikasi video;
multi-object detection;
peta lokasi;
integrasi pengangkutan;
leaderboard;
API berbayar;
penyimpanan foto pengguna.

Jangan merencanakan pengerjaan P1 atau P2 sebelum P0 stabil.

23. Risiko teknis

Buat tabel risiko dengan kolom:

Risiko
Penyebab
Dampak
Probabilitas
Mitigasi
Indikator terdeteksi

Minimal masukkan:

TensorFlow gagal terpasang;
konflik NumPy;
model Teachable Machine tidak kompatibel;
format model berbeda;
jumlah label tidak cocok;
input shape tidak terdeteksi;
model terlalu lambat;
model terlalu besar;
akurasi lokal rendah;
aplikasi crash tanpa model;
gambar rusak;
penggunaan memori tinggi;
Streamlit memuat model berulang;
data leakage;
repository terlalu besar;
lisensi dataset tidak jelas.
24. Risiko kompetisi

Buat planning mitigasi untuk:

proyek terlihat seperti tutorial klasifikasi biasa;
tim tidak memahami model;
penggunaan AI tidak dapat dijelaskan;
hanya menunjukkan accuracy;
tidak memiliki pengujian lokal;
tidak mengungkapkan coding assistant;
rekomendasi tidak realistis untuk daerah kecil;
klaim dampak lingkungan tidak terbukti;
demo tergantung internet;
model gagal saat presentasi;
confidence disalahartikan sebagai jaminan benar.

Rencanakan pembeda proyek:

rekomendasi lokal;
confidence threshold;
transparansi model;
pengujian sampah Indonesia;
aplikasi tetap dapat berjalan offline;
manusia tetap memutuskan;
dokumentasi Responsible AI;
demonstrasi kegagalan model secara jujur.
25. Definition of Done

Planning harus menyatakan MVP selesai hanya jika:

Python 3.11 digunakan;
.venv valid;
dependency dapat diimpor;
TensorFlow 2.15.1 digunakan;
NumPy berada di bawah versi 2;
Streamlit dapat dijalankan;
JPEG dan PNG dapat diproses;
kamera dapat digunakan;
gambar tidak disimpan;
model lokal dapat dimuat;
label sesuai output model;
enam kategori tersedia;
confidence ditampilkan;
confidence rendah menghasilkan warning;
tiga kandidat teratas tersedia;
rekomendasi tersedia;
fallback kategori tidak dikenal tersedia;
aplikasi tidak crash tanpa model;
tidak ada prediksi dummy;
Ruff lulus;
pytest lulus;
smoke test lulus;
disclosure tersedia;
Responsible AI terdokumentasi;
tim dapat menjelaskan alur aplikasi;
pengujian gambar lokal telah dilakukan.
26. Format output planning

Berikan hasil akhir dengan format:

PLANNING IMPLEMENTASI PILAH YUK

1. Ringkasan proyek
2. Kondisi proyek saat ini
3. Konflik atau ketidakjelasan yang ditemukan
4. Arsitektur target
5. Struktur direktori target
6. Dependency plan
7. Tahapan implementasi
8. Rencana model dan dataset
9. Rencana UI
10. Rencana testing
11. Responsible AI
12. Risiko teknis dan mitigasi
13. File yang akan dibuat atau diubah
14. Prioritas P0, P1, dan P2
15. Definition of Done
16. Urutan eksekusi yang direkomendasikan

Untuk bagian file, gunakan tabel:

File
Status saat ini
Perubahan yang direncanakan
Alasan
Risiko

Untuk tahapan implementasi, gunakan tabel:

Tahap
Tujuan
File terkait
Dependency
Hasil akhir
Kriteria selesai

Untuk risiko, gunakan tabel:

Risiko
Dampak
Probabilitas
Mitigasi

Planning harus:

spesifik terhadap kondisi repository;
mengikuti DESIGN.md;
mengikuti AGENT.md;
tidak berisi kode implementasi lengkap;
tidak melakukan perubahan;
tidak melakukan instalasi;
tidak menjalankan format;
tidak membuat commit;
tidak membuat asumsi palsu;
tidak menyatakan model tersedia tanpa bukti;
cukup rinci agar agent implementasi berikutnya dapat bekerja tanpa menebak.

Akhiri dengan:

STATUS: PLANNING SELESAI — BELUM ADA PERUBAHAN PROYEK
