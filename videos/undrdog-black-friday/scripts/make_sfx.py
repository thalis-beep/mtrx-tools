"""Synthesize the sound-design track for the UndrDog Black Friday spot.

Every cue sits on the composition's own timeline times (index.html):
hook hits on BLACK / FRIDAY, a speed-ramp whoosh into the deal, a tick roll
under the 30% digits with a low punch as it lands, the gift reveal, and a
resolved end-frame hit. No voice, no music bed. Output: assets/sfx.wav (48 kHz stereo).
"""
import sys
import numpy as np
import soundfile as sf

SR = 48000
DUR = 6.0
N = int(SR * DUR)
L = np.zeros(N)
R = np.zeros(N)
rng = np.random.default_rng(8)


def place(sig, t, gain=1.0, pan=0.0):
    """Mix a mono signal in at time t; pan -1 (left) .. 1 (right), constant power."""
    i = int(t * SR)
    if i >= N:
        return
    n = min(len(sig), N - i)
    a = (pan + 1) * np.pi / 4
    L[i:i + n] += sig[:n] * gain * np.cos(a)
    R[i:i + n] += sig[:n] * gain * np.sin(a)


def band_noise(d, lo, hi):
    n = int(d * SR)
    X = np.fft.rfft(rng.standard_normal(n))
    f = np.fft.rfftfreq(n, 1 / SR)
    X[(f < lo) | (f > hi)] = 0
    x = np.fft.irfft(X, n)
    return x / (np.abs(x).max() + 1e-9)


def whoosh(d, lo=200, hi=3000, rise=0.7):
    x = band_noise(d, lo, hi)
    t = np.linspace(0, 1, len(x))
    env = np.where(t < rise, (t / rise) ** 2.5, ((1 - t) / (1 - rise)) ** 1.5)
    return x * env


def impact(freq=55, d=0.9, click=0.35):
    """Low sub punch with a short transient on top."""
    t = np.arange(int(d * SR)) / SR
    f = freq * (1 + 1.8 * np.exp(-t * 30))
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 5.5)
    snap = band_noise(d, 900, 7000) * np.exp(-t * 70)
    return sub + click * snap


def tick(freq=2400, d=0.03):
    t = np.arange(int(d * SR)) / SR
    return np.sin(2 * np.pi * freq * t) * np.exp(-t * 200)


def shimmer(d=0.8):
    t = np.arange(int(d * SR)) / SR
    x = band_noise(d, 5000, 12000)
    env = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 2
    return x * env


def tone(freqs, d, decay):
    t = np.arange(int(d * SR)) / SR
    s = sum(np.sin(2 * np.pi * f * t) * np.exp(-t * (decay + 0.6 * i)) for i, f in enumerate(freqs))
    return s * np.minimum(1, t / 0.01) / len(freqs)


# ---------- 0.0 - 1.2  HOOK ----------
d = 1.2                                                    # low air as the light comes up
t = np.arange(int(d * SR)) / SR
place(band_noise(d, 60, 400) * np.clip(t / 0.9, 0, 1) * np.clip((d - t) / 0.2, 0, 1), 0.0, 0.10)
place(impact(52, 0.9), 0.12, 0.55)                         # BLACK
place(impact(64, 0.6, 0.25), 0.22, 0.32)                   # FRIDAY
place(shimmer(0.7), 0.45, 0.04, pan=-0.4)                  # light sweep across the polo

# ---------- speed ramp ----------
place(whoosh(0.26, 150, 4000, 0.85), 0.98, 0.32)
place(whoosh(0.4, 2000, 9000, 0.4), 1.06, 0.06, pan=0.5)  # light sweep cut

# ---------- 1.2 - 3.3  MAIN DEAL ----------
place(impact(70, 0.35, 0.2), 1.22, 0.18)
for k in range(9):                                         # digit roll, slowing as it settles
    place(tick(2600 - k * 60, 0.025), 1.3 + 0.62 * (1 - (1 - k / 9) ** 2), 0.07, pan=-0.15)
place(tick(1500, 0.05), 1.58, 0.08, pan=0.3)               # % slides in
place(whoosh(0.18, 300, 3000, 0.8), 1.7, 0.08)             # OFF
place(impact(46, 1.1, 0.4), 1.96, 0.7)                     # 30% lands
place(tone([110, 165], 1.1, 3.0), 1.96, 0.10)
place(shimmer(0.8), 2.3, 0.045, pan=-0.3)                  # light sweep

# ---------- 3.3 - 5.0  FREE GIFT ----------
place(whoosh(0.3, 150, 3500, 0.8), 3.06, 0.26)             # deal out, products slide
place(impact(80, 0.4, 0.2), 3.36, 0.2, pan=0.4)            # beanie lands
for k in range(10):                                        # FREE BEANIE letters
    place(tick(3200 + 40 * k, 0.02), 3.4 + k * 0.025, 0.03, pan=-0.5 + k / 10)
place(tone([523.25, 783.99], 0.9, 4.0), 3.7, 0.06)         # WITH EVERY ORDER
place(shimmer(0.7), 3.95, 0.05, pan=0.4)                   # light sweep over the beanie

# ---------- 5.0 - 6.0  END FRAME ----------
place(whoosh(0.24, 150, 3500, 0.8), 4.78, 0.24)
place(impact(50, 1.0, 0.35), 5.08, 0.6)
place(tone([98, 146.83, 196, 293.66], 0.95, 2.6), 5.08, 0.14)  # resolved tail under the hold

mix = np.stack([L, R], axis=1)
fade = int(0.12 * SR)
mix[-fade:] *= np.linspace(1, 0, fade)[:, None]
peak = np.abs(mix).max()
mix *= 0.89 / peak                                         # normalise to about -1 dBFS
out = sys.argv[1] if len(sys.argv) > 1 else "assets/sfx.wav"
sf.write(out, mix.astype(np.float32), SR)
print("peak before normalise", round(peak, 3), "->", out)
