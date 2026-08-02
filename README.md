# Pilah Yuk

Aplikasi Streamlit untuk membantu memilah satu objek sampah melalui model Keras lokal.
Gambar diproses di memori dan tidak disimpan permanen.

## Menjalankan

Persyaratan: Python 3.11 dan `uv`.

```bash
uv pip install -r requirements.txt
uv run streamlit run app.py
```

Aplikasi dapat dibuka tanpa model, tetapi tidak akan membuat prediksi. Untuk mengaktifkan
analisis, tempatkan file ekspor asli di:

```text
model/keras_model.h5
model/labels.txt
```

Urutan label harus sama dengan urutan output model. Format label Teachable Machine seperti
`0 cardboard` didukung.

## Pemeriksaan

```bash
uv run ruff format --check .
uv run ruff check .
uv run pytest
```

## Batasan

Model hanya membantu keputusan. Confidence bukan jaminan kebenaran, terutama untuk sampah
campuran, kotor, buram, atau yang berbeda dari data training. Periksa material dan aturan
pengelolaan sampah setempat sebelum bertindak.
