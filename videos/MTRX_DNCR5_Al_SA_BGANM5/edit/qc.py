# usage: python3 qc.py name=url ...  -> downloads to clips/<name>.mp4, prints whisper transcript, writes clips/<name>_strip.png
import sys, subprocess, numpy as np, os
from faster_whisper import WhisperModel
C = os.path.join(os.path.dirname(os.path.abspath(__file__)), "clips")
m = WhisperModel("base.en", device="cpu", compute_type="int8")
for kv in sys.argv[1:]:
    name, url = kv.split("=", 1)
    mp4 = f"{C}/{name}.mp4"
    if not os.path.exists(mp4):
        subprocess.run(["curl", "-sS", "-o", mp4, url], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp4, "-vf", "fps=1.5,scale=200:-1,tile=12x1", f"{C}/{name}_strip.png"], check=True)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", mp4, "-ar", "16000", "-ac", "1", "-f", "f32le", "-"], capture_output=True).stdout
    segs, _ = m.transcribe(np.frombuffer(raw, dtype=np.float32), word_timestamps=True)
    words = [w for s in segs for w in s.words]
    txt = "".join(w.word for w in words).strip()
    span = f"{words[0].start:.1f}-{words[-1].end:.1f}s" if words else "-"
    print(f"{name}: [{span}] {txt}")
