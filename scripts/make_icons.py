from pathlib import Path

from PIL import Image, ImageFilter

drive_path = Path(
    r"C:/Users/Misco/.cursor/projects/c-Users-Misco-Documents-Github-UCC-Manager/assets/Google_Drive_icon__2020_.svg-87cc64aa-6a78-471c-b598-0fe010e4d168.webp"
)
barrow_path = Path(
    r"C:/Users/Misco/.cursor/projects/c-Users-Misco-Documents-Github-UCC-Manager/assets/4700493-bea3b30f-4372-4eb5-8667-09e08d67b46e.png"
)
out_dir = Path(r"C:/Users/Misco/Documents/Github/GDBulk/icons")
out_dir.mkdir(parents=True, exist_ok=True)

drive = Image.open(drive_path).convert("RGBA")
barrow = Image.open(barrow_path).convert("RGBA")

pixels = barrow.load()
w, h = barrow.size
for y in range(h):
    for x in range(w):
        r, g, b, a = pixels[x, y]
        if r < 28 and g < 28 and b < 28:
            pixels[x, y] = (r, g, b, 0)

bbox = barrow.getbbox()
if bbox:
    barrow = barrow.crop(bbox)


def make_logo(size: int) -> Image.Image:
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))

    pad = max(1, size // 16)
    drive_size = size - pad * 2
    d = drive.resize((drive_size, drive_size), Image.Resampling.LANCZOS)
    canvas.alpha_composite(d, (pad, pad))

    bw = int(size * 0.62)
    bh = int(barrow.height * (bw / barrow.width))
    b = barrow.resize((bw, bh), Image.Resampling.LANCZOS)

    alpha = b.split()[-1]
    shadow_layer = Image.new("RGBA", b.size, (0, 0, 0, 110))
    shadow_layer.putalpha(alpha)
    shadow_layer = shadow_layer.filter(
        ImageFilter.GaussianBlur(radius=max(1, size // 32))
    )

    bx = (size - bw) // 2 + size // 18
    by = size - bh - max(1, size // 14) + size // 40
    sx = bx + max(1, size // 48)
    sy = by + max(1, size // 48)

    canvas.alpha_composite(shadow_layer, (sx, sy))
    canvas.alpha_composite(b, (bx, by))
    return canvas


master = make_logo(512)
master_path = out_dir / "logo.png"
master.save(master_path, "PNG")
print("wrote", master_path)

for s in (16, 32, 48, 128):
    if s < 48:
        icon = make_logo(s * 4).resize((s, s), Image.Resampling.LANCZOS)
    else:
        icon = make_logo(s)
    path = out_dir / f"icon{s}.png"
    icon.save(path, "PNG")
    print("wrote", path, icon.size)
