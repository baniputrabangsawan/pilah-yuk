# Pilah Yuk — Project Rules

## Environment
- Python 3.11
- uv
- Streamlit
- TensorFlow 2.15.1
- NumPy < 2
- Pillow
- Virtual environment: .venv

## Commands
- Run app: uv run streamlit run app.py
- Test: uv run pytest
- Lint: uv run ruff check .
- Format: uv run ruff format .

## Architecture
- app.py hanya menangani UI dan orkestrasi.
- src/classifier.py menangani model dan prediction.
- src/recommendations.py menangani rekomendasi rule-based.
- src/utils.py menangani validasi dan preprocessing gambar.
- Model disimpan di model/keras_model.h5.
- Label disimpan di model/labels.txt.

## Engineering rules
- Baca docs/DESIGN.md sebelum mengubah fitur.
- Jangan mengganti Python atau TensorFlow tanpa alasan kompatibilitas yang terbukti.
- Jangan memasang dependency tanpa alasan teknis.
- Jangan menyimpan gambar pengguna secara permanen.
- Jangan menggunakan API eksternal untuk klasifikasi.
- Inferensi harus dapat berjalan lokal.
- Jangan membuat prediksi palsu ketika model tidak tersedia.
- Gunakan type hints.
- Tambahkan error handling.
- Jangan membuat fitur di luar MVP sebelum MVP stabil.
- Jangan menghapus fitur yang sudah berjalan.
- Jalankan Ruff dan pytest sebelum menyatakan tugas selesai.
- Dokumentasikan seluruh tools, model, dataset, dan bantuan coding.
