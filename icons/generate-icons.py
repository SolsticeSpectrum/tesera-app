import os
from PIL import Image
from io import BytesIO
import struct

def resize(path, outpath, size):
    with Image.open(path) as f:
        res = f.resize(size, Image.LANCZOS)
        res.save(outpath)

def ico(path, outpath):
    imgs = []

    sizes = [
        (16, 16), (32, 32), (48, 48),
        (64, 64), (128, 128), (256, 256)
    ]

    for size in sizes:
        img = Image.open(path)
        img.thumbnail(size, Image.LANCZOS)
        imgs.append(img)

    with open(outpath, 'wb') as f:
        f.write(struct.pack('<HHH', 0, 1, len(imgs)))

        pos = f.tell() + len(imgs) * 16

        for img in imgs:
            w, h = img.size
            b = BytesIO()
            img.save(b, format='PNG')
            b = b.getvalue()

            f.write(struct.pack('<BBBB HH II',
                w if w < 256 else 0,
                h if h < 256 else 0,
                0, 0, 1, 32,
                len(b),
                pos))

            pos += len(b)

        for img in imgs:
            b = BytesIO()
            img.save(b, format='PNG')
            f.write(b.getvalue())

def icns(path, outpath):
    img = Image.open(path)
    sizes = [
        (16, 16), (32, 32), (64, 64), (128, 128),
        (256, 256), (512, 512), (1024, 1024)
    ]

    with open(outpath, 'wb') as f:
        f.write(b'icns')
        pos = f.tell()
        f.write(b'\x00\x00\x00\x00')

        for size in sizes:
            data = bitsize(img, size)
            if size == (16, 16):
                size_s = b'icp4'
            elif size == (32, 32):
                size_s = b'icp5'
            elif size == (64, 64):
                size_s = b'icp6'
            elif size == (128, 128):
                size_s = b'ic07'
            elif size == (256, 256):
                size_s = b'ic08'
            elif size == (512, 512):
                size_s = b'ic09'
            elif size == (1024, 1024):
                size_s = b'ic10'
            else:
                continue

            f.write(size_s)
            f.write(struct.pack('>I', len(data) + 8))
            f.write(data)

        end = f.tell()
        f.seek(pos)
        f.write(struct.pack('>I', end))

def bitsize(img, size):
    b = BytesIO()
    res = img.resize(size, Image.LANCZOS)
    res.save(b, format='PNG')
    return b.getvalue()

def main():
    path = "icon.png"

    files = [
        ("32x32.png", (32, 32)),
        ("128x128.png", (128, 128)),
        ("128x128@2x.png", (256, 256)),
        ("icon.ico", (256, 256)),
        ("Square30x30Logo.png", (30, 30)),
        ("Square44x44Logo.png", (44, 44)),
        ("Square71x71Logo.png", (71, 71)),
        ("Square89x89Logo.png", (89, 89)),
        ("Square107x107Logo.png", (107, 107)),
        ("Square142x142Logo.png", (142, 142)),
        ("Square150x150Logo.png", (150, 150)),
        ("Square284x284Logo.png", (284, 284)),
        ("Square310x310Logo.png", (310, 310)),
        ("StoreLogo.png", (50, 50)),
    ]

    for outpath, size in files:
        resize(path, outpath, size)

    img = Image.open("icon.ico")

    ico(path, "icon.ico")
    icns(path, "icon.icns")

    print("Done")

if __name__ == "__main__":
    main()
