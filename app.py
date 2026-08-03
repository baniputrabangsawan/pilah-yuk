"""Streamlit entry point for Pilah Yuk."""

from pathlib import Path
from typing import BinaryIO

import streamlit as st
from PIL import Image

from src.classifier import (
    LABELS_PATH,
    MODEL_PATH,
    ClassifierError,
    Prediction,
    load_labels,
    load_model,
    predict,
)
from src.recommendations import get_recommendation
from src.utils import InvalidImageError, load_image

CONFIDENCE_THRESHOLD = 0.60
IMAGE_FILE_TYPES = ("jpg", "jpeg", "png")
PROJECT_ROOT = Path(__file__).resolve().parent
STYLES_PATH = PROJECT_ROOT / "assets" / "styles.css"


@st.cache_resource
def get_classifier_resources() -> tuple[object, list[str]]:
    """Load local inference resources once per Streamlit process."""
    return load_model(), load_labels()


def load_styles() -> None:
    """Apply the local visual system without external assets."""
    try:
        styles = STYLES_PATH.read_text(encoding="utf-8")
    except OSError:
        return
    st.markdown(f"<style>{styles}</style>", unsafe_allow_html=True)


def show_header() -> None:
    st.markdown(
        """
        <header class="app-header">
            <div>
                <span class="eyebrow">Klasifikasi sampah berbasis AI</span>
                <h1>Pilah Yuk</h1>
                <p>Kenali jenis sampah dan tentukan tindakan yang lebih tepat.</p>
            </div>
        </header>
        """,
        unsafe_allow_html=True,
    )


def show_recommendation(category: str) -> None:
    item = get_recommendation(category)
    st.markdown(
        '<div class="section-label">Rekomendasi tindakan</div>', unsafe_allow_html=True
    )
    st.subheader("Langkah berikutnya")
    st.caption(item.description)

    st.markdown("**Yang dapat dilakukan**")
    st.markdown(f"- {item.action}\n- {item.local_alternative}")
    st.markdown("**Yang perlu dihindari**")
    st.markdown(f"- {item.warning}")
    st.markdown("**Catatan untuk kondisi lokal**")
    st.markdown(f"- {item.facility_note}")


def show_empty_state(source_type: str) -> None:
    """Show guidance relevant to the selected input source."""
    if source_type == "Kamera":
        st.markdown(
            """
            <div class="camera-state">
                <span class="section-label">Kamera siap</span>
                <h3>Ambil satu foto sampah</h3>
                <p>Pastikan objek terlihat jelas sebelum menekan tombol ambil foto.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    st.markdown(
        """
        <div class="empty-state">
            <div class="empty-symbol" aria-hidden="true"></div>
            <h3>Belum ada gambar</h3>
            <p>Unggah atau potret satu objek sampah dengan pencahayaan yang cukup.</p>
        </div>
        <div class="photo-tips">
            <span>Satu objek dominan</span>
            <span>Latar tidak terlalu ramai</span>
            <span>Gambar tidak buram</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def select_image_source(source_type: str) -> BinaryIO | None:
    """Render the selected image input widget and return its in-memory file."""
    if source_type == "Unggah file":
        return st.file_uploader(
            "Pilih gambar",
            type=IMAGE_FILE_TYPES,
            help="Format JPEG atau PNG, maksimal 10 MB.",
        )
    return st.camera_input("Ambil foto sampah")


def load_selected_image(
    source: BinaryIO | None, source_type: str
) -> Image.Image | None:
    """Validate an in-memory image and preview uploaded files."""
    if source is None:
        return None
    try:
        image = load_image(source)
    except InvalidImageError as exc:
        st.error(str(exc))
        return None

    if source_type == "Unggah file":
        st.image(image, caption="Gambar yang akan dianalisis", width="stretch")
    return image


def show_result(result: Prediction) -> None:
    item = get_recommendation(result.category)
    st.markdown(
        '<div class="section-label">Hasil analisis</div>', unsafe_allow_html=True
    )
    st.caption("Kategori utama")
    st.markdown(
        f'<div class="result-category">{item.name}</div>', unsafe_allow_html=True
    )

    confidence_percent = round(result.confidence * 100)
    confidence_label, confidence_value = st.columns([2, 1])
    with confidence_label:
        st.markdown("**Tingkat keyakinan model**")
    with confidence_value:
        st.markdown(
            f'<div class="confidence-value">{result.confidence:.1%}</div>',
            unsafe_allow_html=True,
        )
    st.progress(result.confidence, text=f"Confidence {confidence_percent}%")
    st.caption(
        "Confidence membantu membaca keyakinan model, bukan jaminan hasil benar."
    )

    if result.confidence < CONFIDENCE_THRESHOLD:
        st.warning(
            "**Model belum cukup yakin**\n\n"
            "Ambil ulang foto dari sudut lain atau periksa kategori secara manual."
        )

    st.markdown("**Prediksi lain**")
    for category, confidence in result.top_predictions:
        name = get_recommendation(category).name
        st.markdown(
            f'<div class="prediction-row"><span>{name}</span>'
            f"<strong>{confidence:.1%}</strong></div>",
            unsafe_allow_html=True,
        )

    st.markdown('<div class="result-separator"></div>', unsafe_allow_html=True)
    show_recommendation(result.category)


def show_responsible_ai() -> None:
    with st.container(key="ai_note"):
        st.markdown("**Tentang hasil AI**")
        st.write(
            "Hasil ini merupakan bantuan awal, bukan keputusan akhir. Kondisi sampah dan "
            "aturan pengelolaan setempat tetap perlu diperiksa."
        )
        with st.expander("Baca batasan hasil"):
            st.write(
                "Model dapat keliru pada sampah campuran, kotor, buram, atau yang berbeda "
                "dari data pelatihan. Confidence tinggi juga tidak selalu berarti prediksi "
                "benar. Gambar diproses di memori dan tidak disimpan oleh aplikasi."
            )


def show_disclosure() -> None:
    with st.expander("Tools, model, dan data"):
        st.markdown(
            """
            **Teknologi**

            Streamlit, TensorFlow/Keras, NumPy, dan Pillow.

            **Model**

            Model lokal hasil ekspor Google Teachable Machine. Tidak ada API klasifikasi eksternal.

            **Data**

            TrashNet menjadi sumber data awal dan dilengkapi pengujian foto lokal. Sumber dan
            lisensi dataset perlu diverifikasi sebelum digunakan atau didistribusikan.
            """
        )


def main() -> None:
    st.set_page_config(page_title="Pilah Yuk", page_icon="♻️", layout="wide")
    load_styles()
    show_header()

    model_ready = MODEL_PATH.is_file() and LABELS_PATH.is_file()
    if not model_ready:
        st.info(
            "Model lokal belum tersedia. Letakkan model di "
            f"`{MODEL_PATH}` dan label di `{LABELS_PATH}` untuk mengaktifkan analisis. "
            "Aplikasi tidak akan membuat prediksi pengganti."
        )

    with st.container(key="workspace"):
        input_column, result_column = st.columns([1, 1.08], gap="large")
        result = None

        with input_column, st.container(border=True, key="input_panel"):
            st.markdown(
                '<div class="section-label">Langkah 1</div>', unsafe_allow_html=True
            )
            st.subheader("Masukkan gambar sampah")
            source_type = st.segmented_control(
                "Sumber gambar",
                ("Unggah file", "Kamera"),
                default="Unggah file",
                label_visibility="collapsed",
                width="stretch",
            )
            source = select_image_source(source_type)
            st.caption("JPEG atau PNG · Maks. 10 MB · Tidak disimpan")

            image = load_selected_image(source, source_type)

            analyze = st.button(
                "Analisis gambar",
                type="primary",
                disabled=image is None or not model_ready,
                width="stretch",
            )

            if analyze:
                try:
                    with st.spinner("Menganalisis gambar secara lokal..."):
                        model, labels = get_classifier_resources()
                        result = predict(model, labels, image)
                except (ClassifierError, OSError, ValueError) as exc:
                    st.error(str(exc))

        with result_column, st.container(border=True, key="result_panel"):
            if result is None:
                show_empty_state(source_type)
            else:
                show_result(result)

    show_responsible_ai()
    show_disclosure()


if __name__ == "__main__":
    main()
