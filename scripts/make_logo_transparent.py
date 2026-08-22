from PIL import Image
import sys

src = "assets/img/logo-mark.jpg"
out_full = "assets/img/logo-mark.png"

img = Image.open(src).convert("RGBA")
w, h = img.size
px = img.load()

LOW, HIGH = 18, 70  # luminance thresholds for alpha ramp

minx, miny, maxx, maxy = w, h, 0, 0

for y in range(h):
    for x in range(w):
        r, g, b, a = px[x, y]
        lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
        if lum <= LOW:
            alpha = 0
        elif lum >= HIGH:
            alpha = 255
        else:
            alpha = int((lum - LOW) / (HIGH - LOW) * 255)
        px[x, y] = (r, g, b, alpha)
        if alpha > 10:
            minx, miny = min(minx, x), min(miny, y)
            maxx, maxy = max(maxx, x), max(maxy, y)

pad = 12
minx = max(0, minx - pad)
miny = max(0, miny - pad)
maxx = min(w, maxx + pad)
maxy = min(h, maxy + pad)

cropped = img.crop((minx, miny, maxx, maxy))
cropped.save(out_full)
print("saved", out_full, cropped.size)

# Also export common icon sizes
for size in (512, 256, 128, 64, 32):
    resized = cropped.resize((size, size), Image.LANCZOS)
    resized.save(f"assets/img/logo-mark-{size}.png")
    print("saved", f"assets/img/logo-mark-{size}.png")
