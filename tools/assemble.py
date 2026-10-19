#!/usr/bin/env python3
"""Assemble generated clips into a preview MP4 plus a Premiere Pro package.

Usage: assemble.py edit.json OUT_DIR

edit.json (paths relative to the edit file):
{
  "name": "Nectar pilot", "fps": 30, "width": 1080, "height": 1920,
  "video": [{"file": "clips/shot01.mp4", "src_in": 0.0, "src_out": 4.2}, ...],
  "audio": {"file": "audio/song.wav", "src_in": 0.0},          # optional
  "words": "audio/words.json",                                  # optional [{word,start,end}] on the timeline
  "title": {"text": "Nectar Creatine\\nFor men who want a change.", "start": 16.8, "end": 20.0},
  "callouts": [{"text": "ZERO SUGAR", "start": 97.3, "end": 100.2, "y": 0.3}],   # optional
  "captions_until": 179.0,                                                       # optional
  video items may also set "speed" (e.g. 0.65 to stretch a clip)
}
Clips are cut back to back. Writes OUT_DIR/preview.mp4 (captions burned in) and
OUT_DIR/premiere/{<name>.xml, captions.srt, media/*} for editing in Premiere.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import premiere_xml  # noqa: E402

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
    xml_video, cuts, t = [], [], 0.0
    for v in edit["video"]:
        src = base / v["file"]
        conformed = media / (Path(v["file"]).stem + ".mp4")
        if not (conformed.exists() and conformed.stat().st_mtime >= src.stat().st_mtime):
            run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-an",
                 "-vf", f"setpts=PTS/{v.get('speed', 1.0)},scale={w}:{h}:force_original_aspect_ratio=increase,"
                        f"crop={w}:{h},fps={fps}",
                 "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", str(conformed)])
        length = v["src_out"] - v["src_in"]
        xml_video.append({"file": conformed.name, "src_in": v["src_in"], "src_out": v["src_out"],
                          "start": t, "src_duration": probe_duration(conformed),
                          "dissolve_in": v.get("dissolve_in", 0)})
        cuts.append((conformed, v["src_in"], length))
        t += length
    total = t

    xml_audio, audio_src = [], None
    if edit.get("audio"):
        a = edit["audio"]
        audio_src = media / (Path(a["file"]).stem + ".wav")
        run(["ffmpeg", "-v", "error", "-y", "-i", str(base / a["file"]), "-ar", "48000", "-ac", "2",
             str(audio_src)])
        a_in = a.get("src_in", 0.0)
        a_out = min(a_in + total, probe_duration(audio_src))
        xml_audio.append({"file": audio_src.name, "src_in": a_in, "src_out": a_out, "start": 0.0,
                          "src_duration": probe_duration(audio_src)})

    chunks = []
    if edit.get("words"):
        words = json.loads((base / edit["words"]).read_text())
        if edit.get("captions_until"):
            words = [x for x in words if x["start"] < edit["captions_until"]]
        chunks = caption_chunks(words)
    write_srt(pkg / "captions.srt", chunks)
    ass = work / "captions.ass"
    write_ass(ass, chunks, edit.get("title"), w, h, edit.get("callouts", []))

    # Preview render: hard cuts, captions and title burned in, song underneath.
    # Cut on exact frame boundaries of the timeline so rounding never accumulates
    # and the picture stays locked to the song.
    inputs, parts, t = [], [], 0.0
    for i, (f, s_in, length) in enumerate(cuts):
        n_frames = round((t + length) * fps) - round(t * fps)
        first = round(s_in * fps)
        t += length
        inputs += ["-i", str(f)]
        parts.append(f"[{i}:v]trim=start_frame={first}:end_frame={first + n_frames},setpts=PTS-STARTPTS[v{i}]")
    n = len(cuts)
    sub = str(ass).replace(":", r"\:")
    graph = ";".join(parts) + ";" + "".join(f"[v{i}]" for i in range(n)) + \
        f"concat=n={n}:v=1:a=0[cat];[cat]subtitles='{sub}':fontsdir='{FONT_DIR}'[vout]"
    cmd = ["ffmpeg", "-v", "error", "-y", *inputs]
    maps = ["-map", "[vout]"]
    if audio_src:
        cmd += ["-ss", f"{edit['audio'].get('src_in', 0.0):.3f}", "-i", str(audio_src)]
        graph += f";[{n}:a]atrim=0:{total:.3f},afade=t=out:st={max(total - 0.6, 0):.3f}:d=0.6[aout]"
        maps += ["-map", "[aout]", "-c:a", "aac", "-b:a", "192k"]
    run(cmd + ["-filter_complex", graph, *maps, "-c:v", "libx264", "-crf", "18",
               "-pix_fmt", "yuv420p", "-r", str(fps), "-movflags", "+faststart",
               str(out_dir / "preview.mp4")])

    xml = premiere_xml.build({"name": edit["name"], "fps": fps, "width": w, "height": h,
                              "media_dir": "media", "video": xml_video, "audio": xml_audio})
    (pkg / (edit["name"].replace(" ", "_") + ".xml")).write_text(xml)
    shutil.copy(ass, pkg / "captions_styled.ass")
    print(f"total {total:.2f}s -> {out_dir / 'preview.mp4'}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
