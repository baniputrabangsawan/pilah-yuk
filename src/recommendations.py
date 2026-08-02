"""Auditable, rule-based waste recommendations."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Recommendation:
    name: str
    description: str
    action: str
    warning: str
    local_alternative: str
    facility_note: str


RECOMMENDATIONS = {
    "cardboard": Recommendation(
        "Kardus",
        "Kertas tebal yang umumnya dapat digunakan kembali atau didaur ulang.",
        "Lepaskan selotip, ratakan, dan jaga tetap kering.",
        "Kardus basah atau berminyak biasanya sulit didaur ulang.",
        "Gunakan ulang sebagai wadah; buang bagian terkontaminasi ke sampah residu.",
        "Penerimaan kardus berbeda di tiap bank sampah atau pengepul.",
    ),
    "glass": Recommendation(
        "Kaca",
        "Material kaca dapat digunakan ulang atau didaur ulang jika fasilitas tersedia.",
        "Kosongkan wadah dan pisahkan berdasarkan aturan pengelola setempat.",
        "Bungkus pecahan kaca dan beri tanda agar tidak melukai petugas.",
        "Gunakan ulang wadah yang masih utuh dan aman.",
        "Tidak semua daerah menerima semua warna atau jenis kaca.",
    ),
    "metal": Recommendation(
        "Logam",
        "Kaleng dan logam bersih umumnya memiliki nilai guna ulang atau daur ulang.",
        "Kosongkan, bilas secukupnya, keringkan, lalu pisahkan.",
        "Hati-hati terhadap tepi kaleng yang tajam dan wadah bahan berbahaya.",
        "Kumpulkan terpisah untuk pengepul, atau buang aman sesuai aturan lokal.",
        "Wadah aerosol dan bahan kimia memerlukan penanganan khusus.",
    ),
    "paper": Recommendation(
        "Kertas",
        "Kertas bersih dan kering umumnya dapat digunakan kembali atau didaur ulang.",
        "Pisahkan dari sampah basah dan gunakan kedua sisinya bila memungkinkan.",
        "Kertas berlapis plastik, tisu, dan kertas berminyak sering tidak diterima.",
        "Gunakan sebagai kertas konsep atau bahan kerajinan sebelum dibuang.",
        "Periksa jenis kertas yang diterima oleh pengelola setempat.",
    ),
    "plastic": Recommendation(
        "Plastik",
        "Jenis plastik berbeda memerlukan penanganan yang berbeda.",
        "Kosongkan kemasan, kurangi volumenya, dan pisahkan jika jenisnya dikenali.",
        "Jangan membakar plastik karena asapnya berbahaya.",
        "Gunakan ulang bila aman; jika fasilitas tidak ada, buang tertutup sebagai residu.",
        "Plastik multilapis dan plastik kotor sering tidak diterima untuk daur ulang.",
    ),
    "trash": Recommendation(
        "Sampah Residu",
        "Sampah yang tidak cocok dengan kategori material utama atau telah terkontaminasi.",
        "Bungkus dengan aman dan buang ke tempat sampah residu.",
        "Jangan membakar sampah campuran dan pisahkan benda tajam atau berbahaya.",
        "Periksa kembali apakah ada bagian yang masih dapat dipisahkan atau digunakan ulang.",
        "Ikuti jadwal dan aturan pengumpulan sampah di lingkungan setempat.",
    ),
}

UNKNOWN_RECOMMENDATION = Recommendation(
    "Kategori Belum Dikenali",
    "Material belum dapat dipastikan dari kategori yang diberikan.",
    "Periksa bahan, simbol kemasan, dan kondisi sampah secara manual.",
    "Jangan membakar atau mencampur benda tajam dan bahan berbahaya.",
    "Tanyakan kepada pengelola sampah setempat bila penanganannya tidak jelas.",
    "Layanan dan aturan pemilahan berbeda di setiap daerah.",
)


def get_recommendation(category: str) -> Recommendation:
    """Return a recommendation after normalizing a model category."""
    return RECOMMENDATIONS.get(category.strip().lower(), UNKNOWN_RECOMMENDATION)
