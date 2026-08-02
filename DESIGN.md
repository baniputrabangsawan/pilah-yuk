	# DESIGN.md — Pilah Yuk 🗑️
### Aplikasi Klasifikasi Sampah Berbasis AI untuk Aksi Iklim Lokal
**Studi Kasus 2 — LKS Dikmen Ekshibisi Kecerdasan Artifisial (KA/AI) Tingkat Nasional 2026**

---

## 1. Ringkasan Proyek

**Nama Produk**: Pilah Yuk
**Tagline**: "Foto sampahmu, biar AI yang bantu pilah."
**Tim**: [isi nama tim/sekolah]
**Studi Kasus**: 2 — Lingkungan: Mendukung Aksi Iklim Lokal

Pilah Yuk adalah aplikasi web sederhana yang membantu siswa/warga memilah sampah secara tepat hanya dengan mengunggah atau memotret sampah. Aplikasi mengklasifikasikan jenis sampah menggunakan model computer vision, lalu memberikan saran tindakan konkret (daur ulang, kompos, atau pembuangan khusus) — mengubah kesadaran lingkungan menjadi aksi yang praktis dan terukur.

---

## 2. Latar Belakang & Masalah

Sesuai latar belakang studi kasus: banyak orang peduli lingkungan tapi kesulitan memilah sampah dengan benar karena tidak tahu kategori yang tepat, dan solusi iklim sering terasa abstrak tanpa umpan balik konkret.

**Masalah spesifik yang diangkat**:
1. Sulitnya memilah sampah secara tepat di tingkat rumah tangga/sekolah.
2. Minimnya alat yang membuat aksi lingkungan terasa praktis dan langsung terlihat hasilnya.

**Bukan masalah yang coba diselesaikan** (di luar scope, sesuai prinsip "tidak perlu menyelesaikan keseluruhan masalah"):
- Sistem pengelolaan sampah kota skala besar
- Logistik pengangkutan sampah
- Deteksi sampah dari video real-time / kamera CCTV

---

## 3. Tujuan Solusi

- Membantu individu/sekolah mengklasifikasikan sampah dengan cepat dan akurat menggunakan foto.
- Memberikan rekomendasi tindakan yang jelas dan bisa langsung dilakukan (bukan cuma label kategori).
- Menunjukkan penerapan AI yang bertanggung jawab: transparan soal keterbatasan model, dan tetap mendorong manusia mengambil keputusan akhir saat sistem ragu.

---

## 4. Target Pengguna & User Stories

**Target pengguna**: siswa, guru, pengelola kantin/sekolah, warga di lingkungan RT/RW.

| Sebagai... | Saya ingin... | Supaya... |
|---|---|---|
| Siswa | memfoto sampah dan langsung tahu kategorinya | tidak salah buang ke tempat sampah |
| Guru/pengelola sekolah | melihat rekap jenis sampah yang sering difoto | bisa evaluasi program daur ulang sekolah |
| Warga | tahu cara mengolah sampah tertentu | bisa bertindak, bukan cuma tahu kategorinya |

---

## 5. Alur Fungsional (Input → Proses → Output)

```
[INPUT]
Pengguna mengunggah/memotret 1 gambar sampah
        │
        ▼
[PROSES]
1. Gambar di-preprocess (resize, normalisasi)
2. Model klasifikasi gambar memprediksi kategori
   (kandidat kelas: cardboard, glass, metal, paper, plastic, trash)
3. Sistem menghitung confidence score
4. Jika confidence < threshold (mis. 60%) → tampilkan
   peringatan "kurang yakin" + saran verifikasi manual
5. Sistem mencocokkan kategori ke tabel rekomendasi
   tindakan (rule-based, bukan AI)
        │
        ▼
[OUTPUT]
- Label kategori sampah + confidence score
- Rekomendasi tindakan konkret (daur ulang/kompos/dsb.)
- (Opsional) Catatan ke log lokal untuk rekap sekolah
```

---

## 6. Fitur

### Wajib (MVP — harus selesai untuk lomba)
- [ ] Upload gambar sampah (dari file atau kamera device)
- [ ] Klasifikasi ke 6 kategori dasar (cardboard, glass, metal, paper, plastic, trash)
- [ ] Tampilkan confidence score
- [ ] Rekomendasi tindakan berbasis kategori (rule-based, disusun manual oleh tim)
- [ ] Disclaimer & fallback ketika confidence rendah
- [ ] Halaman disclosure (tools, model, dataset yang dipakai)

### Nice-to-have (kalau waktu memungkinkan)
- [ ] Riwayat/log foto yang pernah diklasifikasi (local storage)
- [ ] Dasbor sederhana: statistik kategori sampah terbanyak per minggu
- [ ] Mode "kuis edukasi" — user tebak dulu sebelum lihat hasil AI

### Eksplisit di luar scope
- Deteksi multi-objek dalam satu foto
- Real-time video classification
- Integrasi ke sistem pengangkutan sampah kota

---

## 7. Tech Stack

Prinsip pemilihan stack: **cepat dibangun lewat vibe coding, gratis/free-tier, mudah didemokan offline saat presentasi, dan sesuai catatan panitia bahwa "tools gratis sudah memadai."**

| Layer | Pilihan | Alasan |
|---|---|---|
| **Model AI** | Teachable Machine (Google) → export TensorFlow.js/Keras | Tidak perlu training manual dari nol, bisa dilatih ulang pakai dataset TrashNet dalam hitungan jam, cocok untuk siswa SMK |
| **Frontend + App** | Streamlit (Python) | Satu file Python bisa jadi web app lengkap (upload gambar, tampilkan hasil, styling dasar) — paling cepat untuk vibe coding |
| **Inference** | TensorFlow / Keras (`.h5` atau `.tflite`) | Load model hasil export Teachable Machine langsung di Python |
| **Bahasa utama** | Python 3.10+ | Konsisten dengan Streamlit & TensorFlow |
| **Dataset** | TrashNet (publik) | Disebutkan langsung di panduan LKS sebagai contoh sumber data terbuka |
| **Rekomendasi tindakan** | Rule-based dictionary (bukan AI) | Sengaja dipisah dari model AI agar predictable & mudah di-audit — bagian dari prinsip Responsible AI |
| **Hosting demo** | Streamlit Community Cloud (gratis) atau jalankan lokal saat presentasi | Menghindari risiko koneksi internet saat demo di lomba |
| **Version control** | GitHub (repo publik/privat) | Untuk dokumentasi & disclosure proses pengembangan |
| **AI coding assistant** | Claude / ChatGPT (dicatat di DISCLOSURE.md) | Untuk membantu generate boilerplate kode — tetap wajib dipahami tim |

**Alternatif jika waktu sangat mepet**: skip training model sendiri, langsung pakai model Teachable Machine yang sudah dilatih tim lalu export ke format `.h5`/`.tflite` — tidak perlu setup TensorFlow training environment yang berat.

---

## 8. Struktur Proyek

```
pilah-yuk/
├── app.py                     # Entry point Streamlit — UI utama
├── requirements.txt            # Daftar dependensi Python
├── README.md                   # Cara install & menjalankan aplikasi
├── DISCLOSURE.md                # Wajib: tools, model, dataset yang dipakai
│
├── model/
│   ├── keras_model.h5           # Model hasil export Teachable Machine
│   ├── labels.txt                # Daftar label kelas (cardboard, glass, dst.)
│   └── train_notes.md            # Catatan proses training (dataset, epoch, akurasi)
│
├── src/
│   ├── __init__.py
│   ├── classifier.py             # Fungsi load model + predict(image)
│   ├── recommendations.py         # Dictionary rule-based rekomendasi tindakan
│   └── utils.py                   # Preprocessing gambar, helper functions
│
├── data/
│   ├── sample_images/              # Contoh gambar untuk testing/demo
│   └── dataset_source.md            # Catatan sumber dataset (link TrashNet, lisensi)
│
├── docs/
│   ├── DESIGN.md                    # File ini
│   ├── responsible_ai.md             # Analisis risiko & mitigasi (lihat bagian 9)
│   └── presentation_script.md         # Naskah presentasi ke juri
│
└── tests/
    └── test_classifier.py            # Test dasar: model bisa load & prediksi
```

---

## 9. Responsible AI

**Risiko yang teridentifikasi**:
1. **Bias data** — dataset TrashNet mayoritas berisi sampah dari konteks negara tertentu, kemungkinan tidak mengenali jenis sampah yang umum di Indonesia (mis. kemasan jajanan lokal, daun kelapa, dsb.)
2. **Misklasifikasi pada sampah ambigu** — sampah kotor/campuran/tidak jelas bentuknya berisiko salah label.
3. **Overreliance** — pengguna bisa terlalu percaya pada hasil AI tanpa mengecek ulang.

**Strategi mitigasi**:
1. Cantumkan confidence score di setiap hasil, bukan hanya label.
2. Set threshold minimum (mis. 60%) — di bawah itu, sistem menyarankan verifikasi manual, bukan memaksakan jawaban.
3. Sediakan disclaimer jelas: *"Hasil ini adalah bantuan awal, bukan keputusan akhir. Verifikasi manual disarankan untuk sampah yang tidak jelas kategorinya."*
4. Uji model dengan beberapa foto sampah lokal Indonesia (di luar dataset asli) untuk melihat performa nyata sebelum demo.

**Manusia tetap berperan** di titik: keputusan akhir cara membuang sampah tetap di tangan pengguna, sistem hanya membantu, bukan memutuskan.

---

## 10. Rencana Data

Sesuai batasan data panduan LKS — hanya menggunakan:
- **Data publik**: dataset TrashNet untuk training model klasifikasi.
- **Data sintetis/uji coba sendiri**: foto sampah yang diambil sendiri oleh tim untuk testing tambahan (bukan data pribadi orang lain).
- **Tidak ada data pribadi/sensitif** yang dikumpulkan atau disimpan.

---

## 11. Milestone & Timeline (disarankan 3–4 minggu)

| Minggu | Fokus |
|---|---|
| 1 | Setup Teachable Machine, training model awal dengan dataset TrashNet, validasi akurasi dasar |
| 2 | Bangun Streamlit app (upload → predict → tampilkan hasil), buat dictionary rekomendasi tindakan |
| 3 | Testing dengan foto sampah lokal, perbaiki threshold & UX, tulis DISCLOSURE.md & responsible_ai.md |
| 4 | Latihan presentasi, siapkan demo offline, uji ulang alur end-to-end, buffer untuk perbaikan |

---

## 12. Definisi Selesai (Definition of Done)

Aplikasi dianggap siap untuk lomba jika:
- [ ] Bisa upload foto dan menerima hasil klasifikasi dalam < 5 detik
- [ ] Minimal 6 kategori sampah dasar terklasifikasi dengan akurasi masuk akal (>70% pada test set)
- [ ] Rekomendasi tindakan muncul untuk setiap kategori
- [ ] Disclaimer confidence rendah berfungsi
- [ ] DISCLOSURE.md dan responsible_ai.md lengkap
- [ ] Bisa dijalankan tanpa koneksi internet stabil (fallback lokal)
- [ ] Tim bisa menjelaskan alur input→proses→output tanpa membaca kode

---

## 13. Disclosure (diisi progresif selama pengembangan)

*Template — lengkapi seiring pengerjaan:*

| Kategori | Yang digunakan | Catatan |
|---|---|---|
| Model AI | Teachable Machine (Google), arsitektur MobileNet | Dilatih ulang dengan dataset TrashNet |
| Dataset | TrashNet (publik, [cantumkan link]) | Lisensi: [cek & cantumkan] |
| AI coding assistant | [Claude/ChatGPT, versi] | Digunakan untuk: boilerplate Streamlit, fungsi preprocessing |
| Library | Streamlit, TensorFlow/Keras, Pillow | Versi dicantumkan di requirements.txt |
| Hosting | Streamlit Community Cloud / lokal | — |
