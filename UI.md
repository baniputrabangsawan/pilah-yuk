Anda adalah senior UI/UX designer dan Streamlit frontend engineer. Perbaiki tampilan aplikasi Pilah Yuk agar lebih modern, menarik, rapi, dan terasa dibuat oleh desainer manusia, bukan tampilan generik hasil AI.

Lokasi proyek:

/home/baniputrabangsawan/Projects/pilah-yuk

Sebelum mengubah apa pun:

Baca DESIGN.md.
Baca AGENT.md.
Periksa app.py dan seluruh file CSS atau komponen UI yang sudah ada.
Pertahankan seluruh fungsi aplikasi yang sudah berjalan.
Jangan mengubah classifier, preprocessing, model, label, rekomendasi, atau logika prediksi kecuali benar-benar diperlukan untuk integrasi UI.
Jangan menghapus fitur upload, kamera, preview, tombol analisis, confidence score, rekomendasi, disclaimer, dan disclosure.
Jangan menambah dependency baru jika CSS dan fitur bawaan Streamlit sudah cukup.
Tujuan desain

Buat tampilan yang:

modern tetapi tidak berlebihan;
profesional untuk kompetisi LKS;
ramah siswa dan masyarakat;
memiliki identitas lingkungan yang kuat;
nyaman digunakan di desktop dan mobile;
memiliki hierarki visual yang jelas;
tidak terlihat seperti template AI generik.
Hindari gaya berikut

Jangan gunakan:

terlalu banyak gradient;
efek neon;
glassmorphism berlebihan;
bayangan tebal;
terlalu banyak animasi;
emoji pada setiap judul;
ikon dekoratif tanpa fungsi;
sudut membulat berlebihan;
teks promosi yang terlalu dramatis;
hero section terlalu besar;
terlalu banyak warna;
kartu untuk setiap elemen;
tampilan seperti dashboard SaaS generik;
elemen dekoratif yang mengganggu fungsi utama.
Arah visual

Gunakan konsep visual:

Bersih
Natural
Tenang
Modern
Praktis
Terpercaya

Palet warna utama:

Hijau tua      : #166534
Hijau utama    : #16A34A
Hijau muda     : #DCFCE7
Latar terang   : #F7F9F7
Putih          : #FFFFFF
Teks utama     : #17201A
Teks sekunder  : #5F6B63
Border         : #DDE5DF
Peringatan     : #B45309
Error          : #B91C1C

Pastikan tetap terbaca pada dark mode atau tetapkan tema aplikasi yang konsisten melalui konfigurasi Streamlit.

Struktur halaman yang diinginkan
1. Header ringkas

Buat header yang tidak terlalu tinggi.

Tampilkan:

Pilah Yuk
Kenali jenis sampah dan tentukan tindakan yang lebih tepat.

Tambahkan label kecil seperti:

Klasifikasi sampah berbasis AI

Gunakan ikon sederhana berbentuk daun, recycle, atau tempat sampah hanya jika sesuai. Jangan memakai emoji besar sebagai identitas utama.

2. Area utama dua kolom

Pada desktop, gunakan dua kolom:

Kolom kiri  : input gambar
Kolom kanan : panduan singkat atau hasil analisis

Pada mobile, susun vertikal.

Kolom input berisi:

pilihan “Unggah file” dan “Kamera”;
uploader atau camera input;
preview gambar;
informasi format file;
tombol utama “Analisis gambar”.

Jadikan area upload terlihat sebagai satu panel yang jelas, bukan elemen Streamlit mentah yang terpisah-pisah.

3. Empty state

Sebelum pengguna memilih gambar, tampilkan empty state sederhana:

Belum ada gambar

Unggah atau potret satu objek sampah dengan pencahayaan yang cukup.

Tambahkan tiga panduan kecil:

satu objek dominan;
latar tidak terlalu ramai;
gambar tidak buram.
4. Tombol utama

Tombol “Analisis gambar” harus:

terlihat sebagai primary action;
menggunakan warna hijau;
memiliki ukuran yang proporsional;
disabled ketika belum ada gambar;
memiliki hover yang halus;
tidak terlalu lebar jika tidak diperlukan.
5. Hasil prediksi

Setelah analisis, tampilkan hasil dalam panel yang terstruktur:

Kategori utama
Nama kategori Bahasa Indonesia

Confidence
Persentase

Prediksi lain
Maksimal tiga kandidat

Gunakan progress bar atau indikator sederhana untuk confidence.

Jangan menggunakan confidence sebagai klaim bahwa hasil pasti benar.

Jika confidence di bawah 60%, tampilkan warning yang jelas tetapi tidak menakutkan:

Model belum cukup yakin

Ambil ulang foto dari sudut lain atau periksa kategori secara manual.
6. Rekomendasi tindakan

Tampilkan rekomendasi dalam bagian terpisah:

Yang dapat dilakukan
Yang perlu dihindari
Catatan untuk kondisi lokal

Gunakan bullet ringkas dan mudah dibaca.

Jangan membuat rekomendasi selalu bergantung pada bank sampah atau fasilitas daur ulang karena tidak semua daerah memilikinya.

7. Responsible AI

Ubah disclaimer panjang menjadi panel informasi yang ringkas:

Tentang hasil AI

Hasil ini merupakan bantuan awal, bukan keputusan akhir. Kondisi sampah dan aturan pengelolaan setempat tetap perlu diperiksa.

Detail tambahan dapat dimasukkan ke expander.

8. Disclosure

Pertahankan bagian:

Tools, model, dan data

Buat tampilannya lebih rapi dan mudah dibaca, tetapi jangan menjadikannya bagian paling dominan.

Tipografi dan spacing

Gunakan font sistem atau font yang sudah tersedia. Jangan menambahkan font eksternal jika tidak diperlukan.

Aturan:

lebar konten utama sekitar 900–1100 piksel;
jarak antarbagian konsisten;
judul utama tidak terlalu besar;
panjang baris teks dibatasi agar mudah dibaca;
label form jelas;
teks sekunder memiliki kontras cukup;
hindari terlalu banyak garis horizontal.
Implementasi Streamlit

Gunakan:

st.set_page_config;
st.container;
st.columns;
st.radio atau segmented control yang tersedia;
st.file_uploader;
st.camera_input;
st.button;
st.progress;
st.status atau st.spinner;
st.warning;
st.info;
st.expander.

Custom CSS diperbolehkan untuk:

lebar konten;
warna;
spacing;
tombol;
panel;
uploader;
tipografi;
border;
responsive layout.

Jangan bergantung pada selector CSS yang terlalu rapuh jika ada alternatif yang lebih aman.

Pisahkan CSS ke file seperti:

assets/styles.css

atau modul UI terpisah jika struktur proyek mendukungnya.

Jangan menaruh seluruh aplikasi dalam satu blok HTML besar. Gunakan komponen Streamlit untuk fungsi utama agar tetap stabil.

Fungsionalitas yang wajib dipertahankan

Pastikan setelah redesign:

upload JPEG dan PNG tetap bekerja;
kamera tetap bekerja;
preview tetap tampil;
tombol analisis hanya aktif saat gambar tersedia;
model lokal tetap dapat dipanggil;
aplikasi tetap berjalan ketika model belum tersedia;
confidence rendah tetap memiliki warning;
rekomendasi tetap berasal dari sistem rule-based;
gambar tetap diproses di memori;
tidak ada gambar yang disimpan;
tidak ada API eksternal baru;
tidak ada prediksi dummy;
tidak ada perubahan urutan label model.
Responsive design

Pastikan:

dua kolom berubah menjadi satu kolom pada layar kecil;
tombol mudah ditekan;
teks tidak terpotong;
uploader tidak melebar keluar layar;
hasil prediksi tetap mudah dibaca;
tidak ada horizontal scrolling.
Proses kerja
Audit UI saat ini.
Buat rencana perubahan singkat.
Implementasikan redesign.
Pertahankan logika aplikasi.
Jalankan formatter dan lint.
Jalankan seluruh test.
Jalankan Streamlit secara headless.
Pastikan halaman tidak crash.
Periksa tampilan desktop dan mobile.
Perbaiki masalah visual atau fungsional yang ditemukan.

Gunakan perintah proyek yang sudah ditentukan dalam AGENT.md.

Minimal jalankan:

uv run ruff format .
uv run ruff check .
uv run pytest
uv run streamlit run app.py --server.headless true
Kriteria selesai

Redesign selesai jika:

tampilan memiliki identitas Pilah Yuk;
visual lebih menarik daripada tampilan awal;
tidak terlihat seperti template AI generik;
fungsi utama langsung terlihat tanpa scroll panjang;
pengguna memahami langkah penggunaan dalam beberapa detik;
empty state jelas;
hasil analisis mudah dipahami;
warning confidence rendah terlihat;
Responsible AI tetap tersedia;
desktop dan mobile responsif;
tidak ada fitur yang rusak;
Ruff lulus;
pytest lulus;
Streamlit dapat dijalankan tanpa traceback.