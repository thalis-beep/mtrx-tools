"""Synthesize the sound-effects track for the mechanism explainer.

Every cue is placed on the composition's own timeline times (index.html), so the
audio lines up with the existing silent render. Output: assets/sfx.wav (48 kHz stereo).
"""
import sys
import numpy as np
import soundfile as sf

SR = 48000
DUR = 10.0
N = int(SR * DUR)
L = np.zeros(N)
R = np.zeros(N)
rng = np.random.default_rng(1992)


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
    x = rng.standard_normal(n)
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(n, 1 / SR)
    X[(f < lo) | (f > hi)] = 0
    x = np.fft.irfft(X, n)
    return x / (np.abs(x).max() + 1e-9)


def whoosh(d=0.5, lo=250, hi=2600, rise=0.5):
    x = band_noise(d, lo, hi)
    t = np.linspace(0, 1, len(x))
    env = np.where(t < rise, (t / rise) ** 2, ((1 - t) / (1 - rise)) ** 1.5)
    return x * env


def pop(freq=900, d=0.08, drop=12):
    t = np.arange(int(d * SR)) / SR
    f = freq * np.exp(-t * drop)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 55)


def tick(freq=2600, d=0.03):
    t = np.arange(int(d * SR)) / SR
    return np.sin(2 * np.pi * freq * t) * np.exp(-t * 180)


def zap(d=0.06):
    """Tiny static crackle: bright noise burst with a quick pitch blip."""
    t = np.arange(int(d * SR)) / SR
    crackle = band_noise(d, 3000, 9000) * np.exp(-t * 90)
    blip = np.sin(2 * np.pi * (2200 + 1800 * np.exp(-t * 60)) * t) * np.exp(-t * 70)
    return 0.6 * crackle + 0.4 * blip


def thud(freq=110, d=0.35):
    t = np.arange(int(d * SR)) / SR
    f = freq * np.exp(-t * 6)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 11)


def chime(freqs, d=1.2, decay=3.0):
    t = np.arange(int(d * SR)) / SR
    s = sum(np.sin(2 * np.pi * f * t) * np.exp(-t * (decay + i)) for i, f in enumerate(freqs))
    return s / len(freqs)


def glide(f0, f1, d, decay_end=0.0):
    t = np.arange(int(d * SR)) / SR
    f = f0 * (f1 / f0) ** (t / d)
    env = np.minimum(1, t / 0.04) * (1 - (1 - decay_end) * (t / d))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env


# ---------- 0 - 2  POLYESTER FRICTION ----------
place(whoosh(0.55, 300, 3000, 0.35), 0.0, 0.16)          # lens opens
place(pop(600, 0.1), 0.05, 0.10)
place(whoosh(0.35, 900, 5000, 0.4), 0.22, 0.05)          # title in
# fabric rubbing: brushed texture following the yoyo (0.42 s sweeps from 0.1 s)
rub_d = 0.42 * 5
rub = band_noise(rub_d, 1200, 6500) * 0.6 + band_noise(rub_d, 300, 1200) * 0.4
t = np.arange(len(rub)) / SR
speed = np.abs(np.sin(np.pi * t / 0.42))                  # fastest mid-sweep
grow = np.clip(t / 0.3, 0, 1) * np.clip((rub_d - t) / 0.3, 0, 1)
place(rub * speed ** 1.5 * grow, 0.1, 0.11, pan=-0.05)
for i in range(16):                                       # cyan particles appear
    place(tick(3200 + 120 * (i % 5), 0.025), 0.5 + i * 0.05, 0.035, pan=-0.5 + i / 16)
for i in range(10):                                       # charge symbols spark
    place(zap(), 0.75 + i * 0.09, 0.10, pan=-0.6 + i * 0.13)

# ---------- 2 - 4  ELECTROSTATIC CHARGE ----------
place(whoosh(0.5, 200, 2200, 0.6), 1.92, 0.18)           # pull back
place(whoosh(0.35, 900, 5000, 0.4), 2.06, 0.04)          # title in
for i in range(16):                                       # charges pop around the swatch
    place(zap(0.05), 2.35 + i * 0.035, 0.07, pan=np.cos(i / 16 * 2 * np.pi + 0.2) * 0.8)
# field hum: swells while the lines draw, pulses twice, fades with the field
hd = 1.65
t = np.arange(int(hd * SR)) / SR
hum = (np.sin(2 * np.pi * 120 * t) + 0.5 * np.sin(2 * np.pi * 240 * t)
       + 0.25 * np.sin(2 * np.pi * 360 * t) + 0.15 * band_noise(hd, 2000, 6000))
env = np.clip(t / 0.6, 0, 1) * np.clip((hd - t) / 0.3, 0, 1)
pulse = 1 - 0.35 * np.clip(np.sin(np.pi * np.clip(t - 0.5, 0, None) / 0.32), 0, 1) * (t > 0.5) * (t < 1.14)
place(hum * env * pulse, 2.55, 0.06)
for i in range(3):                                        # each field line completes
    place(chime([1318.5, 1975.5], 0.5, 8), 3.05 + i * 0.12, 0.035)

# ---------- 4 - 6  TRAPPED HEAT ----------
place(whoosh(0.45, 150, 1500, 0.5), 3.95, 0.16)          # swatch flattens
place(whoosh(0.35, 900, 5000, 0.4), 4.06, 0.04)          # title in
place(thud(90, 0.4), 4.25, 0.22)                          # body rises into place
# warm, airy heat shimmer that builds as the glow intensifies, until the split
sd = 3.4
t = np.arange(int(sd * SR)) / SR
air = band_noise(sd, 200, 1800)
wob = 0.75 + 0.25 * np.sin(2 * np.pi * t / 0.85)          # one swell per wave cycle
rumble = np.sin(2 * np.pi * 55 * t) * 0.5
build = np.clip(t / 1.5, 0, 1) ** 1.2 * np.clip((sd - t) / 0.4, 0, 1)
place((air * wob + rumble * np.clip((t - 0.2) / 1.4, 0, 1)) * build, 4.45, 0.10, pan=0.0)
for c in range(4):                                        # soft rising sighs per wave cycle
    if 4.45 + c * 0.85 < 7.6:
        place(glide(260, 420, 0.7, 0.0) * 0.5, 4.45 + c * 0.85, 0.03)

# ---------- 6 - 8  COMBINED EFFECT ----------
place(whoosh(0.5, 300, 2600, 0.5), 5.93, 0.16)           # split screen
place(whoosh(0.35, 900, 5000, 0.4), 6.06, 0.04)          # title in
place(tick(1800, 0.05), 6.2, 0.10)                        # divider draws
place(pop(1200, 0.07), 6.4, 0.10, pan=-0.6)               # STATIC label
place(pop(900, 0.07), 6.48, 0.10, pan=0.6)                # HEAT label
# static hum on the left, heat air on the right while both run
d = 0.95
t = np.arange(int(d * SR)) / SR
env = np.clip(t / 0.2, 0, 1) * np.clip((d - t) / 0.25, 0, 1)
place((np.sin(2 * np.pi * 120 * t) + 0.4 * np.sin(2 * np.pi * 240 * t)) * env, 6.1, 0.03, pan=-0.7)
place(band_noise(d, 200, 1500) * env, 6.1, 0.05, pan=0.7)
place(pop(700, 0.12, 8), 6.95, 0.22)                      # "+" appears
place(whoosh(0.4, 400, 3000, 0.7), 7.2, 0.10, pan=-0.5)   # halves slide together
place(whoosh(0.4, 400, 3000, 0.7), 7.2, 0.10, pan=0.5)
place(thud(130, 0.35), 7.55, 0.22)                        # they merge
place(chime([523.25, 783.99, 1046.5], 1.0, 3.5), 7.55, 0.10)

# ---------- 8 - 10  POTENTIAL DISRUPTION ----------
place(whoosh(0.55, 200, 2000, 0.5), 7.95, 0.12)          # emblem settles on the node
# a soft blip as each cell leaves the node; later ones are lower and quieter (slowing output)
spawns = [8.0, 8.12, 8.24, 8.38, 8.56, 8.8, 9.12, 9.5]
for k, s in enumerate(spawns):
    place(pop(1500 - k * 110, 0.06, 10), s, 0.09 - k * 0.007)
place(glide(620, 240, 1.1, 0.0), 8.55, 0.05)              # output gauge drops
place(thud(80, 0.5), 8.6, 0.26)                           # final title lands
place(chime([392.0, 466.16, 587.33], 1.4, 2.2), 8.62, 0.08)  # minor, unresolved
place(tick(2000, 0.04), 8.95, 0.06)                       # underline draws

mix = np.stack([L, R], axis=1)
fade = int(0.25 * SR)
mix[-fade:] *= np.linspace(1, 0, fade)[:, None]
peak = np.abs(mix).max()
mix *= 0.89 / peak                                        # normalise to about -1 dBFS
out = sys.argv[1] if len(sys.argv) > 1 else "assets/sfx.wav"
sf.write(out, mix.astype(np.float32), SR)
print("peak before normalise", round(peak, 3), "->", out)
