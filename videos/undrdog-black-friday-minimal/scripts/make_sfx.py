"""Quiet sound design for the minimal UndrDog Black Friday spot.

A soft low hit as the header lands, light ticks as the offer and gift card
settle, a breath of air under each product sheen, and a warm tone tail.
Cue times match index.html. Output: assets/sfx.wav (48 kHz stereo).
"""
import sys
import numpy as np
import soundfile as sf

SR = 48000
DUR = 6.0
N = int(SR * DUR)
L = np.zeros(N)
R = np.zeros(N)
rng = np.random.default_rng(6)


def place(sig, t, gain=1.0, pan=0.0):
    i = int(t * SR)
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


def soft_hit(freq=58, d=1.4):
    t = np.arange(int(d * SR)) / SR
    f = freq * (1 + 0.8 * np.exp(-t * 25))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 3.2) * np.minimum(1, t / 0.006)


def tick(freq, d=0.05):
    t = np.arange(int(d * SR)) / SR
    return np.sin(2 * np.pi * freq * t) * np.exp(-t * 120)


def air(d, lo=3000, hi=10000):
    t = np.arange(int(d * SR)) / SR
    return band_noise(d, lo, hi) * np.sin(np.pi * t / d) ** 2


def tone(freqs, d, decay):
    t = np.arange(int(d * SR)) / SR
    s = sum(np.sin(2 * np.pi * f * t) * np.exp(-t * (decay + 0.4 * i)) for i, f in enumerate(freqs))
    return s * np.minimum(1, t / 0.08) / len(freqs)


place(air(0.4, 400, 4000), 0.0, 0.10)                     # rise into the header
place(soft_hit(), 0.08, 0.7)                               # BLACK FRIDAY lands
place(tick(1760), 0.2, 0.10, pan=-0.2)                     # UP TO
place(soft_hit(70, 0.8), 0.28, 0.35)                       # 30% OFF
place(tick(2350), 0.48, 0.09, pan=0.2)                     # gift card
place(tone([196, 293.66, 392], 4.5, 0.9), 0.3, 0.12)       # warm bed that decays across the hold
place(air(1.3), 1.9, 0.05, pan=-0.3)                       # polo sheen
place(air(1.0), 3.3, 0.04, pan=0.3)                        # beanie sheen

mix = np.stack([L, R], axis=1)
fade = int(0.3 * SR)
mix[-fade:] *= np.linspace(1, 0, fade)[:, None]
mix *= 0.8 / np.abs(mix).max()
out = sys.argv[1] if len(sys.argv) > 1 else "assets/sfx.wav"
sf.write(out, mix.astype(np.float32), SR)
print("->", out)
