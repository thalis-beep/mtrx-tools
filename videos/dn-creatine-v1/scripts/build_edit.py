"""Build the V1 edit from edit/timeline.json + edit/overlays.json.

Outputs (in edit/):
  video/<slot>.mp4         conformed 1080x1920 @24fps segments, exact slot length
  DNCR5_V1_Premiere.xml    FCP7 XML (Premiere: File > Import): V1 video, V2 title/guarantee,
                           V3-V6 icons, V7 captions, A1 VO, A2+ SFX
  preview/DNCR5_V1_preview.mp4  burned preview with VO + SFX mix
Usage: python3 build_edit.py [--no-preview]
"""
import json, os, subprocess, sys
from xml.sax.saxutils import escape

ED = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "edit")
ED = os.path.abspath(ED)
T = json.load(open(f"{ED}/timeline.json"))
O = json.load(open(f"{ED}/overlays.json"))
FPS = T["fps"]
TOTAL = round(T["duration"] * FPS)
ROOT = "DNCR5_V1_Premiere"  # folder name the XML expects; relink once in Premiere if moved
fr = lambda t: round(t * FPS)
run = lambda cmd: subprocess.run(cmd, check=True)
FF = ["ffmpeg", "-nostdin", "-v", "error", "-y"]
BASE = f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps={FPS},setsar=1"


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", path], capture_output=True, text=True).stdout
    return float(out)


# ---------- 1. conform video segments ----------
os.makedirs(f"{ED}/video", exist_ok=True)
for v in T["video"]:
    n = fr(v["end"]) - fr(v["start"])
    dur = n / FPS
    src = f"{ED}/raw/{v['clip']}.mp4"
    out = f"{ED}/video/{v['slot']}.mp4"
    v["frames"] = n
    if os.path.exists(out) and os.path.getmtime(out) > os.path.getmtime(src) and "--force" not in sys.argv:
        continue
    mode = v.get("mode", "trim")
    if mode == "fit":  # slow the whole clip to fill the slot
        k = dur / probe(src)
        vf = f"setpts={k:.4f}*PTS,{BASE}"
        args = ["-i", src]
    elif mode == "speed":  # play from in at a fixed speed factor
        vf = f"setpts=PTS/{v['speed']},{BASE}"
        args = ["-ss", str(v["in"]), "-i", src]
    elif mode == "reverse":
        vf = f"reverse,{BASE}"
        args = ["-i", src]
    elif mode == "hold":  # play from in, freeze last frame to fill
        vf = f"{BASE},tpad=stop_mode=clone:stop_duration=3"
        args = ["-ss", str(v["in"]), "-i", src]
    else:
        vf = BASE
        args = ["-ss", str(v["in"]), "-i", src]
    run(FF + args + ["-vf", vf, "-frames:v", str(n), "-an", "-c:v", "libx264",
                     "-crf", "16", "-pix_fmt", "yuv420p", out])
    v["frames"] = n

# ---------- 2. FCP7 XML ----------
uid = 0
def nid():
    global uid; uid += 1; return uid

def rate():
    return f"<rate><timebase>{FPS}</timebase><ntsc>FALSE</ntsc></rate>"

SEEN = set()
def file_el(fid, name, rel, frames, kind):
    if fid in SEEN:  # FCP XML: define a file once, reference it afterwards
        return f'<file id="{fid}"/>'
    SEEN.add(fid)
    media = ("<video><samplecharacteristics><width>1080</width><height>1920</height>"
             "</samplecharacteristics></video>") if kind == "video" else \
            ("<audio><samplecharacteristics><depth>16</depth><samplerate>48000</samplerate>"
             "</samplecharacteristics><channelcount>2</channelcount></audio>")
    return (f'<file id="{fid}"><name>{escape(name)}</name>'
            f"<pathurl>file://localhost/{ROOT}/{rel}</pathurl>{rate()}"
            f"<duration>{frames}</duration><media>{media}</media></file>")

def vclip(name, rel, start, end, src_in=0, src_frames=None):
    n = end - start
    src_frames = src_frames or (src_in + n)
    return (f'<clipitem id="clip-{nid()}"><name>{escape(name)}</name><enabled>TRUE</enabled>'
            f"<duration>{src_frames}</duration>{rate()}<start>{start}</start><end>{end}</end>"
            f"<in>{src_in}</in><out>{src_in + n}</out>"
            f"{file_el('file-' + name, name, rel, src_frames, 'video')}</clipitem>")

def aclip(name, rel, start, frames, gain_db=0.0):
    lvl = 10 ** (gain_db / 20)
    filt = ("<filter><effect><name>Audio Levels</name><effectid>audiolevels</effectid>"
            "<effectcategory>audiolevels</effectcategory><effecttype>audiolevels</effecttype>"
            "<mediatype>audio</mediatype><parameter><parameterid>level</parameterid>"
            f"<name>Level</name><valuemin>0</valuemin><valuemax>3.98109</valuemax>"
            f"<value>{lvl:.5f}</value></parameter></effect></filter>")
    return (f'<clipitem id="clip-{nid()}"><name>{escape(name)}</name><enabled>TRUE</enabled>'
            f"<duration>{frames}</duration>{rate()}<start>{start}</start><end>{start + frames}</end>"
            f"<in>0</in><out>{frames}</out>{file_el('file-' + name, name, rel, frames, 'audio')}"
            f"<sourcetrack><mediatype>audio</mediatype><trackindex>1</trackindex></sourcetrack>"
            f"{filt}</clipitem>")

def track(items):
    return "<track>" + "".join(items) + "<enabled>TRUE</enabled><locked>FALSE</locked></track>"

V1 = [vclip(v["slot"], f"video/{v['slot']}.mp4", fr(v["start"]), fr(v["start"]) + v["frames"])
      for v in T["video"]]

gfx = {g["name"]: g for g in O["graphics"]}
def still(g):
    s, e = fr(g["s"]), fr(g["e"])
    return vclip(os.path.basename(g["png"]), g["png"], s, e, 0, e - s)
V2 = [still(gfx["title_why_bloat"]), still(gfx["guarantee"])]
icons = [g for g in O["graphics"] if g["name"].startswith("icon_")]
VICONS = [[still(g)] for g in icons]
VCAP = [still({"png": c["png"], "s": c["s"], "e": c["e"]}) for c in O["captions"]]

vo_frames = fr(probe(f"{ED}/audio/VO_DNCR5_V1.wav"))
A1 = [aclip("VO_DNCR5_V1.wav", "audio/VO_DNCR5_V1.wav", 0, vo_frames)]
lanes, lane_end = [], []
for s in sorted(T["sfx"], key=lambda x: x["t"]):
    n = fr(probe(f"{ED}/audio/sfx/{s['f']}.wav"))
    st = fr(s["t"])
    k = next((i for i, e in enumerate(lane_end) if st >= e), None)
    if k is None:
        lanes.append([]); lane_end.append(0); k = len(lanes) - 1
    lanes[k].append(aclip(f"{s['f']}.wav", f"audio/sfx/{s['f']}.wav", st, n, s["db"]))
    lane_end[k] = st + n

vtracks = [track(V1), track(V2)] + [track(t) for t in VICONS] + [track(VCAP)]
atracks = [track(A1)] + [track(l) for l in lanes]
xml = ('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE xmeml>\n<xmeml version="4">'
       f'<sequence id="seq-1"><name>DNCR5_V1</name><duration>{TOTAL}</duration>{rate()}'
       "<media><video><format><samplecharacteristics>"
       f"{rate()}<width>1080</width><height>1920</height><pixelaspectratio>square</pixelaspectratio>"
       "</samplecharacteristics></format>" + "".join(vtracks) + "</video>"
       "<audio><numOutputChannels>2</numOutputChannels>" + "".join(atracks) + "</audio></media>"
       "</sequence></xmeml>\n")
open(f"{ED}/DNCR5_V1_Premiere.xml", "w").write(xml)
print("XML written:", len(V1), "video,", len(VCAP), "captions,", len(T["sfx"]), "sfx")

if "--no-preview" in sys.argv:
    sys.exit()

# ---------- 3. preview render ----------
os.makedirs(f"{ED}/preview", exist_ok=True)
lst = f"{ED}/preview/concat.txt"
open(lst, "w").write("".join(f"file '{ED}/video/{v['slot']}.mp4'\n" for v in T["video"]))
run(FF + ["-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", f"{ED}/preview/base.mp4"])

ovs = [(g["png"], g["s"], g["e"]) for g in O["graphics"]] + \
      [(c["png"], c["s"], c["e"]) for c in O["captions"]]
inputs, chain, last = [], [], "0:v"
for i, (png, s, e) in enumerate(ovs, start=1):
    inputs += ["-i", f"{ED}/{png}"]
    chain.append(f"[{last}][{i}:v]overlay=0:0:enable='between(t,{s:.3f},{e - 0.001:.3f})'[v{i}]")
    last = f"v{i}"
na = len(ovs) + 1
inputs += ["-i", f"{ED}/audio/VO_DNCR5_V1.wav"]
amix = [f"[{na}:a]anull[vo]"]
labels = ["[vo]"]
for j, s in enumerate(T["sfx"]):
    inputs += ["-i", f"{ED}/audio/sfx/{s['f']}.wav"]
    ms = int(s["t"] * 1000)
    amix.append(f"[{na + 1 + j}:a]volume={s['db']}dB,adelay={ms}|{ms}[s{j}]")
    labels.append(f"[s{j}]")
amix.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0,alimiter=limit=0.89[aout]")
fc = ";".join(chain + amix)
open(f"{ED}/preview/filter.txt", "w").write(fc)
run(FF + ["-i", f"{ED}/preview/base.mp4"] + inputs +
    ["-filter_complex_script", f"{ED}/preview/filter.txt", "-map", f"[{last}]", "-map", "[aout]",
     "-c:v", "libx264", "-crf", "22", "-preset", "medium", "-pix_fmt", "yuv420p",
     "-c:a", "aac", "-b:a", "192k", "-t", f"{T['duration']}", "-movflags", "+faststart",
     f"{ED}/preview/DNCR5_V1_preview.mp4"])
os.remove(f"{ED}/preview/base.mp4")
print("preview written")
