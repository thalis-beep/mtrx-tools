#!/usr/bin/env python3
"""Assemble generated clips into a preview MP4 plus a Premiere Pro package.

Usage: assemble.py edit.json OUT_DIR

edit.json (paths relative to the edit file):
{
  "name": "Nectar pilot", "fps": 30, "width": 1080, "height": 1920,
  "video": [{"file": "clips/shot01.mp4", "src_in": 0.0, "src_out": 4.2}, ...],
  "audio": {"file": "audio/song.wav", "src_in": 0.0,          # optional
            "gain": [{"start": 89.5, "end": 100.5, "db": 2}],   # optional, song time, 0.5s ramps
            "fade_out": 2.5},                                   # optional, fades the end of the edit
  "words": "audio/words.json",                                  # optional [{word,start,end}] on the timeline
  "overlays": [{"name": "Captions", "events": "captions/captions.json"}],  # optional PNG tracks
  "title": {"text": "Nectar Creatine\\nFor men who want a change.", "start": 16.8, "end": 20.0},
  "callouts": [{"text": "ZERO SUGAR", "start": 97.3, "end": 100.2, "y": 0.3}],   # optional
  "captions_until": 179.0,                                                       # optional
  video items may also set "speed" (e.g. 0.65 to stretch a clip)
}
Clips are cut back to back. Writes OUT_DIR/preview.mp4 (captions burned in) and
OUT_DIR/premiere/{<name>.xml, media/*} for editing in Premiere (plus captions.srt when "words"
is given). Overlay events files are [{png, start, end, pop?}] with PNGs next to them, as written by
captions_png.py and graphics_png.py; each becomes its own track in the preview and in Premiere.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
import premiere_otio  # noqa: E402

FONT_DIR = Path(__file__).parent / "fonts"
FONT = "Montserrat Thin ExtraBold"


def run(cmd):
    subprocess.run(cmd, check=True)


def probe_duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(path)], capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def ts_ass(t):
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def ts_srt(t):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def caption_chunks(words, max_words=3, max_gap=0.35):
    """Group word timings into short on-screen phrases, like the reference video."""
    chunks, cur = [], []
    for w in words:
        if cur and (len(cur) >= max_words or w["start"] - cur[-1]["end"] > max_gap):
            chunks.append(cur)
            cur = []
        cur.append(w)
    if cur:
        chunks.append(cur)
    out = []
    for i, c in enumerate(chunks):
        end = c[-1]["end"]
        if i + 1 < len(chunks):
            end = min(max(end, c[-1]["end"] + 0.15), chunks[i + 1][0]["start"])
        out.append({"text": " ".join(w["word"].strip() for w in c), "start": c[0]["start"], "end": end})
    return out


def write_ass(path, chunks, title, w, h, callouts=()):
    lines = [
        "[Script Info]", "ScriptType: v4.00+", f"PlayResX: {w}", f"PlayResY: {h}", "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, "
        "Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, "
        "Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        f"Style: Cap,{FONT},74,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,6,2,2,80,80,{int(h * 0.25)},1",
        f"Style: Title,{FONT},92,&H00FFFFFF,&H00FFFFFF,&H00301A12,&H64000000,0,0,0,0,100,100,0,0,1,7,3,8,60,60,{int(h * 0.19)},1",
        f"Style: Callout,{FONT},84,&H00FFFFFF,&H00FFFFFF,&H00522A1E,&H00522A1E,0,0,0,0,100,100,2,0,3,18,0,5,60,60,0,1",
        "", "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]
    for c in chunks:
        lines.append(f"Dialogue: 0,{ts_ass(c['start'])},{ts_ass(c['end'])},Cap,,0,0,0,,{c['text']}")
    for c in callouts:
        # pop-in callout inside the upper part of the 4:5 safe zone
        lines.append(f"Dialogue: 2,{ts_ass(c['start'])},{ts_ass(c['end'])},Callout,,0,0,0,,"
                     f"{{\\pos({w // 2},{int(h * c.get('y', 0.3))})\\fscx40\\fscy40\\t(0,180,\\fscx100\\fscy100)\\fad(0,150)}}"
                     f"{c['text']}")
    if title:
        text = title["text"].replace("\n", "\\N")
        lines.append(f"Dialogue: 1,{ts_ass(title['start'])},{ts_ass(title['end'])},Title,,0,0,0,,"
                     f"{{\\fad(250,0)}}{text}")
    path.write_text("\n".join(lines) + "\n")


def write_srt(path, chunks):
    blocks = [f"{i}\n{ts_srt(c['start'])} --> {ts_srt(c['end'])}\n{c['text']}\n"
              for i, c in enumerate(chunks, 1)]
    path.write_text("\n".join(blocks))


def gain_expr(gains, ramp=0.5):
    """volume= expression (song time) that eases into and out of each gain window."""
    expr = "1"
    for g in reversed(gains):
        a, b, k = g["start"], g["end"], 10 ** (g["db"] / 20)
        expr = (f"if(between(t,{a - ramp},{a}),1+({k}-1)*(t-{a - ramp})/{ramp},"
                f"if(between(t,{a},{b}),{k},if(between(t,{b},{b + ramp}),{k}-({k}-1)*(t-{b})/{ramp},{expr})))")
    return expr


def overlay_list(events, src_dir, work, name, fps, total, w, h):
    """Concat-demuxer list that shows each PNG for its frames and a blank frame in between.
    "pop" events scale in over 5 frames, like a callout popping on."""
    blank = work / "blank.png"
    if not blank.exists():
        Image.new("RGBA", (w, h), (0, 0, 0, 0)).save(blank)
    end_f = round(total * fps)
    spans = premiere_otio.frame_spans(events, fps, end_f)
    lines, cur = ["ffconcat version 1.0"], 0

    def put(path, frames):
        lines.extend([f"file '{path}'", f"duration {frames / fps:.6f}"])

    for a, b, e in spans:
        if a > cur:
            put(blank, a - cur)
        png = src_dir / e["png"]
        if e.get("pop") and b - a > 5:
            img = Image.open(png)
            x0, y0, x1, y1 = img.getbbox()
            cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
            for i, sc in enumerate((0.45, 0.65, 0.85, 1.06, 1.0)):
                frame = Image.new("RGBA", (w, h), (0, 0, 0, 0))
                part = img.crop((x0, y0, x1, y1))
                part = part.resize((max(1, round(part.width * sc)), max(1, round(part.height * sc))))
                frame.alpha_composite(part, (round(cx - part.width / 2), round(cy - part.height / 2)))
                f = work / f"{name}_{Path(e['png']).stem}_pop{i}.png"
                frame.save(f)
                put(f, 1)
            put(png, b - a - 5)
        else:
            put(png, b - a)
        cur = b
    if cur < end_f:
        put(blank, end_f - cur)
    lines.append(f"file '{blank}'")
    lst = work / f"{name}.ffconcat"
    lst.write_text("\n".join(lines) + "\n")
    return lst


def main(edit_path, out_dir):
    edit_path, out_dir = Path(edit_path), Path(out_dir)
    base = edit_path.parent
    edit = json.loads(edit_path.read_text())
    fps, w, h = edit["fps"], edit["width"], edit["height"]
    pkg = out_dir / "premiere"
    media = pkg / "media"
    media.mkdir(parents=True, exist_ok=True)
    work = out_dir / "work"
    work.mkdir(exist_ok=True)

    # Conform every source to the sequence format, keeping its full length so the
    # editor can still slip and extend shots in Premiere.
    cuts, t = [], 0.0
    for v in edit["video"]:
        src = base / v["file"]
        conformed = media / (Path(v["file"]).stem + ".mp4")
        if not (conformed.exists() and conformed.stat().st_mtime >= src.stat().st_mtime):
            run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-an",
                 "-vf", f"setpts=PTS/{v.get('speed', 1.0)},scale={w}:{h}:force_original_aspect_ratio=increase,"
                        f"crop={w}:{h},setsar=1,fps={fps}",
                 "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", str(conformed)])
        length = v["src_out"] - v["src_in"]
        cuts.append((conformed, v["src_in"], length))
        t += length
    total = t

    audio_src = None
    if edit.get("audio"):
        a = edit["audio"]
        audio_src = media / (Path(a["file"]).stem + ".wav")
        # level fixes and the closing fade go into the WAV itself, so Premiere plays the same mix
        af = []
        if a.get("gain"):
            af.append(f"volume='{gain_expr(a['gain'])}':eval=frame")
        if a.get("fade_out"):
            af.append(f"afade=t=out:st={a.get('src_in', 0.0) + total - a['fade_out']:.3f}:d={a['fade_out']}")
        run(["ffmpeg", "-v", "error", "-y", "-i", str(base / a["file"]), *(["-af", ",".join(af)] if af else []),
             "-ar", "48000", "-ac", "2", str(audio_src)])

    chunks = []
    if edit.get("words"):
        words = json.loads((base / edit["words"]).read_text())
        if edit.get("captions_until"):
            words = [x for x in words if x["start"] < edit["captions_until"]]
        chunks = caption_chunks(words)
        write_srt(pkg / "captions.srt", chunks)
    ass = work / "captions.ass"
    write_ass(ass, chunks, edit.get("title"), w, h, edit.get("callouts", []))

    overlays = []
    for ov in edit.get("overlays", []):
        ev_path = base / ov["events"]
        events = json.loads(ev_path.read_text())
        for e in events:
            shutil.copy(ev_path.parent / e["png"], media / e["png"])
        overlays.append(overlay_list(events, ev_path.parent.resolve(), work.resolve(), ov["name"].lower(),
                                     fps, total, w, h))

    # Preview render: hard cuts, captions and title burned in, song underneath.
    # Cut on exact frame boundaries of the timeline so rounding never accumulates
    # and the picture stays locked to the song.
    inputs, parts, t = [], [], 0.0
    for i, (f, s_in, length) in enumerate(cuts):
        n_frames = round((t + length) * fps) - round(t * fps)
        first = round(s_in * fps)
        t += length
        inputs += ["-i", str(f)]
        parts.append(f"[{i}:v]trim=start_frame={first}:end_frame={first + n_frames},setpts=PTS-STARTPTS,setsar=1[v{i}]")
    n = len(cuts)
    sub = str(ass).replace(":", r"\:")
    graph = ";".join(parts) + ";" + "".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[cat]"
    last = "cat"
    for k, lst in enumerate(overlays):
        inputs += ["-f", "concat", "-safe", "0", "-i", str(lst)]
        graph += (f";[{n + k}:v]fps={fps},format=rgba[ov{k}];"
                  f"[{last}][ov{k}]overlay=0:0:eof_action=pass:format=auto[o{k}]")
        last = f"o{k}"
    if chunks or edit.get("title") or edit.get("callouts"):
        graph += f";[{last}]subtitles='{sub}':fontsdir='{FONT_DIR}'[vout]"
    else:
        graph += f";[{last}]null[vout]"
    cmd = ["ffmpeg", "-v", "error", "-y", *inputs]
    maps = ["-map", "[vout]"]
    if audio_src:
        a_idx = n + len(overlays)
        cmd += ["-ss", f"{edit['audio'].get('src_in', 0.0):.3f}", "-i", str(audio_src)]
        tail = "" if edit["audio"].get("fade_out") else f",afade=t=out:st={max(total - 0.6, 0):.3f}:d=0.6"
        graph += f";[{a_idx}:a]atrim=0:{total:.3f}{tail}[aout]"
        maps += ["-map", "[aout]", "-c:a", "aac", "-b:a", "192k"]
    run(cmd + ["-filter_complex", graph, *maps, "-c:v", "libx264", "-crf", "18",
               "-pix_fmt", "yuv420p", "-r", str(fps), "-movflags", "+faststart",
               str(out_dir / "preview.mp4")])

    premiere_otio.main(edit_path, pkg)
    if chunks:
        shutil.copy(ass, pkg / "captions_styled.ass")
    print(f"total {total:.2f}s -> {out_dir / 'preview.mp4'}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
