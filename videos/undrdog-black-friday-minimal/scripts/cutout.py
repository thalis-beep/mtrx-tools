"""Cut a dark product off a light studio background, keeping the original pixels.

The product photos are dark garments on white / light-grey sweeps, so the
matte comes from luminance: a solid core (everything dark and connected),
a soft edge band where the pixel is un-mixed from a reconstructed background
plate, and nothing beyond it (drops studio contact shadows).

usage: python3 scripts/cutout.py in.jpg out.png [core_threshold] [choke_px]
"""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

src, out = sys.argv[1], sys.argv[2]
thr = float(sys.argv[3]) if len(sys.argv) > 3 else 120
choke = int(sys.argv[4]) if len(sys.argv) > 4 else 0
I = np.asarray(Image.open(src).convert("RGB")).astype(np.float64)
L = I @ [0.299, 0.587, 0.114]

# core: dark pixels, holes filled, largest component only
core = L < thr
core = ndi.binary_opening(core, iterations=2)
lab, n = ndi.label(core)
sizes = ndi.sum(core, lab, range(1, n + 1))
core = lab == (1 + int(np.argmax(sizes)))
core = ndi.binary_fill_holes(core)

# background plate: normalised blur of the pixels outside a dilated core
outside = ~ndi.binary_dilation(core, iterations=8)
w = ndi.gaussian_filter(outside.astype(float), 40)
B = np.stack([ndi.gaussian_filter(I[..., c] * outside, 40) for c in range(3)], -1) / np.maximum(w, 1e-6)[..., None]
BL = B @ [0.299, 0.587, 0.114]

# edge band: a few px either side of the core boundary
inner = ndi.binary_erosion(core, iterations=3)
band = ndi.binary_dilation(core, iterations=3) & ~inner
FG = 40.0                                     # typical garment luminance near its edge
a = np.clip((BL - L) / np.maximum(BL - FG, 1), 0, 1)
# outside the core, fade out light pixels: a soft contact shadow is not fabric
a = np.where(core, a, a * np.clip((150 - L) / 40, 0, 1))
alpha = np.where(inner, 1.0, np.where(band, a, 0.0))
alpha = ndi.gaussian_filter(alpha, 0.6) * (inner | band)
alpha[inner] = 1.0
if choke:                                     # pull the edge in to drop a shadow fringe
    alpha = ndi.grey_erosion(alpha, size=(2 * choke + 1, 2 * choke + 1))

# un-mix the background from edge pixels so no white halo remains
am = np.maximum(alpha, 1e-3)[..., None]
C = np.clip((I - (1 - alpha[..., None]) * B) / am, 0, 255)
C = np.where(inner[..., None], I, C)

rgba = np.dstack([C, alpha * 255]).round().astype(np.uint8)
im = Image.fromarray(rgba, "RGBA")
im = im.crop(im.getbbox())
im.save(out, optimize=True)
print(out, im.size)
