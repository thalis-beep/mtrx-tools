"""Raise the SFX-only track to a standalone level without flattening its dynamics.

Applies one static gain (dB), then a lookahead peak limiter that only touches the few
loudest hits. Usage: master_sfx.py in.wav out.wav gain_db
"""
import sys
import numpy as np
import soundfile as sf
from numpy.lib.stride_tricks import sliding_window_view

CEILING = 10 ** (-1.5 / 20)

x, sr = sf.read(sys.argv[1])
if x.ndim == 1:
    x = np.stack([x, x], axis=1)

gain_db = float(sys.argv[3])
y = x * 10 ** (gain_db / 20)

peak = np.abs(y).max(axis=1)
need = np.minimum(1.0, CEILING / np.maximum(peak, 1e-9))
look = int(0.005 * sr)
need = sliding_window_view(np.pad(need, look, constant_values=1.0), 2 * look + 1).min(axis=1)  # lookahead
# smooth release so gain recovers over ~60 ms instead of snapping back
rel = np.exp(-1 / (0.06 * sr))
g = np.empty_like(need)
cur = 1.0
for i, n in enumerate(need):
    cur = n if n < cur else n + (cur - n) * rel
    g[i] = cur
y *= g[:, None]
sf.write(sys.argv[2], y.astype(np.float32), sr)
print("max gain reduction dB", round(20 * np.log10(g.min()), 2), "peak", round(np.abs(y).max(), 3))
