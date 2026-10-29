"""Assemble V1 on a timeline in CS-script order. Each segment is normalised to 1080x1920/30fps/48k stereo, then concatenated."""
import subprocess, os, json
S = os.path.dirname(os.path.abspath(__file__)); C, G, T = f"{S}/clips", f"{S}/gfx", f"{S}/timeline_v2"
os.makedirs(T, exist_ok=True)
V = "scale=1080:1920:flags=lanczos,setsar=1,fps=30,format=yuv420p"
ENC = ["-c:v", "libx264", "-preset", "medium", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2"]

def run(args): subprocess.run(["ffmpeg", "-v", "error", "-y", *args], check=True)

def clip(name, src, a, b, overlays=(), crop=None):
    """Trim src[a:b]; overlays = [(png, t0, t1)] in segment time; crop = 'L'/'R' trims 14% off that side (stray-person fix)."""
    d = b - a; inputs = ["-ss", str(a), "-t", str(d), "-i", f"{C}/{src}.mp4"]
    cf = {"L": "crop=iw*0.86:ih*0.86:iw*0.14:ih*0.04,", "R": "crop=iw*0.86:ih*0.86:0:ih*0.04,"}.get(crop, "")
    fc = f"[0:v]{cf}{V}[v0]"; last = "v0"
    for i, (png, t0, t1) in enumerate(overlays, 1):
        inputs += ["-loop", "1", "-t", str(d), "-i", f"{G}/{png}"]
        fc += f";[{i}:v]format=rgba,fade=t=in:st={t0}:d=0.25:alpha=1[o{i}];[{last}][o{i}]overlay=enable='between(t,{t0},{t1})'[v{i}]"; last = f"v{i}"
    fc += f";[0:a]aformat=sample_rates=48000:channel_layouts=stereo,afade=t=in:d=0.04,afade=t=out:st={d - 0.08:.2f}:d=0.08[a]"
    out = f"{T}/{name}.mp4"; run([*inputs, "-filter_complex", fc, "-map", f"[{last}]", "-map", "[a]", "-t", str(d), *ENC, out]); return out

def still(name, png, d, fade=True):
    vf = V + (f",fade=t=in:d=0.4,fade=t=out:st={d - 0.4}:d=0.4" if fade else "")
    out = f"{T}/{name}.mp4"
    run(["-loop", "1", "-t", str(d), "-i", f"{G}/{png}", "-f", "lavfi", "-t", str(d), "-i", "anullsrc=r=48000:cl=stereo",
         "-vf", vf, "-shortest", *ENC, out]); return out

def nectar_clean(src="c22b", d=7.6, cut=1.55, calls=(1.78, 2.6, 3.92, 5.12, 5.84)):
    """22b audio: `cut` s of the daughter on camera, then the product hero (shot 23, slowed) with callouts timed to her words."""
    hero = d - cut; k = hero / 4.0
    inputs = ["-ss", "0", "-t", str(d), "-i", f"{C}/{src}.mp4", "-t", "4", "-i", f"{C}/c23.mp4"]
    fc = f"[0:v]trim=0:{cut},setpts=PTS-STARTPTS,{V}[va];[1:v]setpts={k:.4f}*PTS,{V},trim=0:{hero:.2f},setpts=PTS-STARTPTS[vb]"
    last = "vb"
    for i, t in enumerate(calls, 1):
        t0 = t - cut; t1 = calls[i] - cut if i < len(calls) else hero
        inputs += ["-loop", "1", "-t", str(hero), "-i", f"{G}/callout{i}.png"]
        fc += f";[{i + 1}:v]format=rgba[o{i}];[{last}][o{i}]overlay=enable='between(t,{t0:.2f},{t1:.2f})'[vb{i}]"; last = f"vb{i}"
    fc += f";[va][{last}]concat=n=2:v=1:a=0[v];[0:a]aformat=sample_rates=48000:channel_layouts=stereo,afade=t=out:st={d - 0.1}:d=0.1[a]"
    out = f"{T}/22b_23.mp4"; run([*inputs, "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-t", str(d), *ENC, out]); return out

# ---- TIMELINE V2 (CS script order; client revisions 2026-10-29) ----
segs = [
 # HOOK 1 — staircase (no laundry; mom falls to her knees)
 clip("h1", "v2h1", 0, 5.0),                      # walks up, stumbles, falls to her knees
 clip("h2", "v3h2", 0, 2.3),                      # on her knees: "These stairs are getting harder lately..."
 clip("h3", "v2h3", 0, 2.1),                      # daughter: "Mom! Are you okay?" (clean floor)
 clip("h4", "v2h4", 0, 2.75),                     # close-up on her knees: "I'm fine, I'm fine..."
 clip("h5", "c05", 0.9, 3.0),                     # "...Are you sure?"
 # SCRIPT — couch: locked WIDE / MOM single / DAUGHTER single
 clip("11", "c11", 0, 4.9),                       # WIDE
 clip("12", "v3_12", 0, 5.35),                    # MOM
 clip("13", "v2_13", 0, 6.95),                    # WIDE
 clip("14", "c14", 0, 1.9),                       # DAUGHTER
 clip("15", "v2_15", 0, 5.35),                    # MOM
 clip("16", "v3_16", 0, 4.8, crop="L"),           # DAUGHTER
 clip("17", "v3_17", 0.5, 2.3, crop="R"),         # MOM
 clip("18", "v2_18", 0, 6.55),                    # WIDE + product handoff
 clip("19", "v2_19", 0, 3.35),                    # MOM + stick
 clip("20a", "v2_20a", 0, 6.35, [("atp1.png", 0.8, 6.35)]),   # DAUGHTER + pouch
 clip("20b", "v2_20b", 0, 7.4, [("atp2.png", 0.0, 7.4)]),     # WIDE + product
 clip("21", "v3_21", 0, 7.2),                     # MOM + stick
 clip("22a", "v2_22a", 0, 7.3),                   # DAUGHTER + pouch
 nectar_clean("v2_22b", 7.5, 1.25, (1.42, 2.66, 3.8, 5.0, 5.74)),  # WIDE -> product hero + callouts
 clip("24", "v4_24", 0, 2.95),                     # MOM + stick
 still("title", "title_3months.png", 2.2),
 # ACT 3 — trail (unchanged from V1)
 clip("25", "c25v2", 0, 7.4),
 clip("26", "c26", 0, 2.95),
 clip("27", "c27", 0, 7.45),
 clip("28", "c28", 0, 6.0),
 still("black1", "black1.png", 2.0, fade=False),
 still("black2", "black2.png", 1.8, fade=False),
 still("black3", "black3.png", 2.0, fade=False),
 still("black4", "black4.png", 2.4, fade=False),
 still("end", "endcard.png", 3.0),
]
with open(f"{T}/list.txt", "w") as f: f.writelines(f"file '{p}'\n" for p in segs)
out = f"{S}/MTRX_DNCR5_Al_SA_BGANM5_V2.mp4"
run(["-f", "concat", "-safe", "0", "-i", f"{T}/list.txt", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out])
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out], capture_output=True, text=True).stdout)
print(f"{out}  {dur:.1f}s")
