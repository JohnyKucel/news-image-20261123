"""Entri make.fun news-image-20261123: halaman depan koran 33 berita.

Gambarnya adalah karya Grey (dibuat dengan Gemini atas arahannya):
koran "Monday 23 November 2026" — 33 berita dunia + kripto, lead COP31
runtuh tanpa kesepakatan di Antalya, band CRYPTO NEWS (BTC $61,368,
ETH $1,722, SOL $70.79), peta dunia, strip timeline UTC, dan kotak
DATE CHECK & METHODOLOGY. Gambar dipakai apa adanya, tanpa edit.

Program ini stdlib-only dan hanya menyalin aset tersebut byte-identik
ke out/entry.png — pola yang diizinkan aturan lomba ("the simplest
program copies an image the repository holds"). Asetnya JPEG 1024x1024,
321.488 byte (di bawah batas 1 MiB); nama output tetap entry.png,
isinya dikenali dari byte pertamanya sebagai JPEG, sesuai aturan.
Tidak ada network, tidak ada timestamp, tidak ada random — setiap run
menghasilkan byte yang sama persis.
"""

import os
import shutil

ASSET = "entry_gemini.jpg"
EXPECTED_SHA256 = "fbc047544e3855febcedf8f4f81ea4bf5de048322349ba83451156aa0ef29c73"


def _sha256(path):
    import hashlib

    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def copy_entry(assets_dir, out_dir):
    src = os.path.join(assets_dir, ASSET)
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    return dst


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    assets = os.path.join(here, "assets")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.path.join(here, "out")

    src = os.path.join(assets, ASSET)
    if _sha256(src) != EXPECTED_SHA256:
        raise ValueError("aset berubah, sha tidak cocok: %s" % src)

    out_path = copy_entry(assets, out_dir)

    if _sha256(out_path) != EXPECTED_SHA256:
        raise ValueError("output tidak byte-identik dengan aset")
    print(out_path)


if __name__ == "__main__":
    main()
