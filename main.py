"""Entri make.fun news-image-20261123 v4: halaman depan koran broadsheet.

"Monday 23 November 2026 \u2014 35 dated stories, 7 regions: COP31 ends
with no deal, 165 missiles over Ukraine, Bitcoin reclaims $61,368".

Konsep: satu hari, satu halaman, satu gambar. Grid 6 kolom, hairline
1px, radius 0, newsprint #F1ECE0 + tinta #111111 + SATU warna spot
merah (kicker, stempel NO DEAL, red topic bars, band CRYPTO NEWS).
Masthead blackletter THE WORLD + ears + double rule. Lead COP31
headline 36pt satu baris, deck satu baris, body 2 baris per kolom;
hero-nya panel before/after 976x190 selebar halaman penuh (Sabtu
"deal expected", 3 delegasi besar tersenyum di meja perundingan, vs
Minggu "talks collapse", 2 kursi kosong + pakta robek + 2 delegasi
besar pergi sambil cemberut) + stempel NO DEAL di jahitan panel.
Kyiv turun jadi small story; Brent turun jadi brief. Setiap cerita
membawa tanggalnya (WED/THU/FRI/SAT/SUN 19-22 Nov 2026): 1 feature
+ 12 berita kecil + 5 sel CRYPTO NEWS + 17 brief = 35 cerita
bertanggal, 7 region, peta + legenda, tabel timeline UTC, DATE CHECK.

Semua angka dari riset 23 Nov 2026 (snapshot pagi 23 Nov: BTC $61,368,
ETH $1,722, SOL $70,79). Semua gambar kartun orisinal hasil code
(garis tinta + wash cat air datar, satu gaya garis konsisten).
Tanpa nomor cerita, tanpa sebut testnet.

File ini stdlib-only (os, struct, zlib) dan hanya merakit aset yang
sudah di-render sebelumnya di assets/ menjadi satu PNG deterministik
1024x1024. Urutan lapisan: kertas, grain, ilustrasi, bingkai dan garis
pemisah, lalu teks. Tidak ada timestamp dan tidak ada random, jadi
setiap run menghasilkan byte yang sama persis.
"""

import os
import struct
import zlib

SIGNATURE = b"\x89PNG\r\n\x1a\n"
WIDTH = 1024
HEIGHT = 1024
BG = (241, 236, 224)
INK = (17, 17, 17)
DIVIDER = (180, 170, 145)

TEXT = [
    ("t_topband.png", 24, 9),
    ("t_masthead.png", 24, 33),
    ("t_dateline.png", 291, 125),
    ("t_ticker.png", 231, 141),
    ("t_stats.png", 28, 158),
    ("t_regions.png", 24, 196),
    ("t_feat0.png", 24, 222),
    ("t_small0_0.png", 24, 536),
    ("t_small0_1.png", 188, 536),
    ("t_small0_2.png", 352, 536),
    ("t_small0_3.png", 516, 536),
    ("t_small0_4.png", 680, 536),
    ("t_small0_5.png", 844, 536),
    ("t_small1_0.png", 24, 652),
    ("t_small1_1.png", 188, 652),
    ("t_small1_2.png", 352, 652),
    ("t_small1_3.png", 516, 652),
    ("t_small1_4.png", 680, 652),
    ("t_small1_5.png", 844, 652),
    ("t_crypto.png", 24, 764),
    ("t_map.png", 24, 822),
    ("t_timeline.png", 24, 926),
    ("t_briefs.png", 374, 822),
    ("t_datecheck.png", 804, 820),
    ("t_footband.png", 0, 1000),
]

ART = [
    ("illo_cop31_ba.png", 24, 336),
    ("illo_mexico_s.png", 27, 612),
    ("illo_peru_s.png", 191, 612),
    ("illo_trump_s.png", 355, 612),
    ("illo_wallst_s.png", 519, 612),
    ("illo_gta_s.png", 683, 612),
    ("illo_korea_s.png", 847, 612),
    ("illo_bepi_s.png", 27, 728),
    ("illo_gaza_s.png", 191, 728),
    ("illo_eisenkot_s.png", 355, 728),
    ("illo_hormuz_s.png", 519, 728),
    ("illo_russia_w_s.png", 683, 728),
    ("illo_cricket_s.png", 847, 728),
]

BARS_H = [155, 216, 530, 646, 761, 817]

BARS_V = [
    (184, 532, 642),
    (348, 532, 642),
    (512, 532, 642),
    (676, 532, 642),
    (840, 532, 642),
    (184, 648, 758),
    (348, 648, 758),
    (512, 648, 758),
    (676, 648, 758),
    (840, 648, 758),
    (589, 822, 993),
]


def _paeth(left, up, up_left):
    p = left + up - up_left
    pa = abs(p - left)
    pb = abs(p - up)
    pc = abs(p - up_left)
    if pa <= pb and pa <= pc:
        return left
    if pb <= pc:
        return up
    return up_left


def _unfilter(raw, width, height, bpp):
    stride = width * bpp
    out = bytearray(height * stride)
    prev = bytearray(stride)
    pos = 0
    for y in range(height):
        f = raw[pos]
        pos += 1
        row = raw[pos:pos + stride]
        pos += stride
        cur = bytearray(stride)
        if f == 0:
            cur[:] = row
        elif f == 1:
            for i in range(stride):
                left = cur[i - bpp] if i >= bpp else 0
                cur[i] = (row[i] + left) & 0xFF
        elif f == 2:
            for i in range(stride):
                cur[i] = (row[i] + prev[i]) & 0xFF
        elif f == 3:
            for i in range(stride):
                left = cur[i - bpp] if i >= bpp else 0
                cur[i] = (row[i] + (left + prev[i]) // 2) & 0xFF
        elif f == 4:
            for i in range(stride):
                left = cur[i - bpp] if i >= bpp else 0
                up_left = prev[i - bpp] if i >= bpp else 0
                cur[i] = (row[i] + _paeth(left, prev[i], up_left)) & 0xFF
        else:
            raise ValueError("filter tidak dikenal: %d" % f)
        out[y * stride:(y + 1) * stride] = cur
        prev = cur
    return bytes(out)


def read_png(path):
    with open(path, "rb") as fh:
        data = fh.read()
    if data[:8] != SIGNATURE:
        raise ValueError("bukan PNG: %s" % path)
    offset = 8
    width = height = None
    bit_depth = None
    color_type = None
    idat = []
    while offset < len(data):
        length = struct.unpack(">I", data[offset:offset + 4])[0]
        name = data[offset + 4:offset + 8]
        payload = data[offset + 8:offset + 8 + length]
        offset += 12 + length
        if name == b"IHDR":
            width, height, bit_depth, color_type = struct.unpack(
                ">IIBB", payload[:10])
            interlace = payload[12]
            if bit_depth != 8:
                raise ValueError("bit depth harus 8: %s" % path)
            if interlace != 0:
                raise ValueError("interlace harus 0: %s" % path)
            if color_type not in (0, 2, 6):
                raise ValueError("color type tidak didukung: %d" % color_type)
        elif name == b"IDAT":
            idat.append(payload)
        elif name == b"IEND":
            break
    if width is None:
        raise ValueError("IHDR tidak ditemukan: %s" % path)
    if color_type == 0:
        bpp = 1
    elif color_type == 2:
        bpp = 3
    else:
        bpp = 4
    raw = zlib.decompress(b"".join(idat))
    plain = _unfilter(raw, width, height, bpp)
    if color_type == 0:
        pixels = bytearray(width * height * 3)
        for i, v in enumerate(plain):
            pixels[i * 3] = v
            pixels[i * 3 + 1] = v
            pixels[i * 3 + 2] = v
        return width, height, bytes(pixels), False
    if color_type == 2:
        return width, height, plain, False
    return width, height, plain, True


def _chunk(name, payload):
    out = struct.pack(">I", len(payload))
    out += name
    out += payload
    out += struct.pack(">I", zlib.crc32(name + payload) & 0xFFFFFFFF)
    return out


def write_png(path, width, height, rgb):
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    stride = width * 3
    raw0 = bytearray()
    raw2 = bytearray()
    for y in range(height):
        row = rgb[y * stride:(y + 1) * stride]
        raw0.append(0)
        raw0 += row
        raw2.append(2)
        if y == 0:
            raw2 += row
        else:
            prev = rgb[(y - 1) * stride:y * stride]
            raw2 += bytes((row[i] - prev[i]) & 0xFF for i in range(stride))
    comp0 = zlib.compress(bytes(raw0), 9)
    comp2 = zlib.compress(bytes(raw2), 9)
    if len(comp2) < len(comp0):
        idat = comp2
    else:
        idat = comp0
    with open(path, "wb") as fh:
        fh.write(SIGNATURE)
        fh.write(_chunk(b"IHDR", ihdr))
        fh.write(_chunk(b"IDAT", idat))
        fh.write(_chunk(b"IEND", b""))


def paste(canvas, sw, sh, pixels, has_alpha, dx, dy):
    if has_alpha:
        step = 4
    else:
        step = 3
    for sy in range(sh):
        ty = dy + sy
        if ty < 0 or ty >= HEIGHT:
            continue
        for sx in range(sw):
            tx = dx + sx
            if tx < 0 or tx >= WIDTH:
                continue
            so = (sy * sw + sx) * step
            do = (ty * WIDTH + tx) * 3
            if has_alpha:
                a = pixels[so + 3]
                if a == 0:
                    continue
                if a == 255:
                    canvas[do] = pixels[so]
                    canvas[do + 1] = pixels[so + 1]
                    canvas[do + 2] = pixels[so + 2]
                else:
                    inv = 255 - a
                    canvas[do] = (pixels[so] * a + canvas[do] * inv + 127) // 255
                    canvas[do + 1] = (pixels[so + 1] * a + canvas[do + 1] * inv + 127) // 255
                    canvas[do + 2] = (pixels[so + 2] * a + canvas[do + 2] * inv + 127) // 255
            else:
                canvas[do] = pixels[so]
                canvas[do + 1] = pixels[so + 1]
                canvas[do + 2] = pixels[so + 2]


def frame(canvas, x0, y0, x1, y1, rgb, thickness=1):
    r, g, b = rgb
    for t in range(thickness):
        for x in range(x0 + t, x1 - t + 1):
            for y in (y0 + t, y1 - t):
                o = (y * WIDTH + x) * 3
                canvas[o] = r
                canvas[o + 1] = g
                canvas[o + 2] = b
        for y in range(y0 + t, y1 - t + 1):
            for x in (x0 + t, x1 - t):
                o = (y * WIDTH + x) * 3
                canvas[o] = r
                canvas[o + 1] = g
                canvas[o + 2] = b


def hbar(canvas, y, thickness):
    top = y - (thickness - 1) // 2
    r, g, b = DIVIDER
    for yy in range(top, top + thickness):
        if yy < 0 or yy >= HEIGHT:
            continue
        base = yy * WIDTH * 3
        for x in range(24, 1000 + 1):
            o = base + x * 3
            canvas[o] = r
            canvas[o + 1] = g
            canvas[o + 2] = b


def vbar(canvas, x, y0, y1):
    r, g, b = DIVIDER
    for yy in range(y0, y1 + 1):
        if yy < 0 or yy >= HEIGHT:
            continue
        o = (yy * WIDTH + x) * 3
        canvas[o] = r
        canvas[o + 1] = g
        canvas[o + 2] = b


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    assets = os.path.join(here, "assets")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.path.join(here, "out")
    os.makedirs(out_dir, exist_ok=True)

    canvas = bytearray(WIDTH * HEIGHT * 3)
    r, g, b = BG
    for i in range(0, len(canvas), 3):
        canvas[i] = r
        canvas[i + 1] = g
        canvas[i + 2] = b

    gw, gh, grain, galpha = read_png(os.path.join(assets, "grain_256.png"))
    for gy in range(0, HEIGHT, gh):
        for gx in range(0, WIDTH, gw):
            paste(canvas, gw, gh, grain, galpha, gx, gy)

    for name, x, y in ART:
        w, h, pixels, alpha = read_png(os.path.join(assets, name))
        paste(canvas, w, h, pixels, alpha, x, y)

    frame(canvas, 24, 336, 999, 525, INK)

    for y in BARS_H:
        hbar(canvas, y, 1)

    for x, y0, y1 in BARS_V:
        vbar(canvas, x, y0, y1)

    for name, x, y in TEXT:
        w, h, pixels, alpha = read_png(os.path.join(assets, name))
        paste(canvas, w, h, pixels, alpha, x, y)

    out_path = os.path.join(out_dir, "entry.png")
    write_png(out_path, WIDTH, HEIGHT, bytes(canvas))
    print(out_path)


if __name__ == "__main__":
    main()
