#!/usr/bin/env python3
"""Build a Final Cut Pro 7 XML (xmeml v4) timeline that Adobe Premiere Pro imports.

Usage: premiere_xml.py edit.json out.xml

edit.json:
{
  "name": "Nectar pilot",
  "fps": 30, "width": 1080, "height": 1920,
  "media_dir": "media",                      # path written into the XML, relative to the XML
  "video": [ {"file": "shot01.mp4", "src_in": 0.0, "src_out": 4.2, "start": 0.0,
              "src_duration": 5.0, "dissolve_in": 0.0} , ... ],
  "audio": [ {"file": "song.wav", "src_in": 0.0, "src_out": 19.5, "start": 0.0,
              "src_duration": 30.0} ]
}
Times are seconds. "dissolve_in" adds a cross dissolve at the head of that clip
(centred on the cut). In Premiere: File > Import the XML, then relink media if asked
(locate one file and the rest are found in the same folder).
"""
import json
import sys
from pathlib import Path
from xml.sax.saxutils import escape


def frames(sec, fps):
    return int(round(sec * fps))


def rate(fps):
    return f"<rate><timebase>{fps}</timebase><ntsc>FALSE</ntsc></rate>"


def file_el(fid, name, media_dir, dur_f, fps, w, h, kind, emitted):
    if fid in emitted:
        return f'<file id="{fid}"/>'
    emitted.add(fid)
    media = ""
    if kind == "video":
        media = (f"<media><video><samplecharacteristics>{rate(fps)}<width>{w}</width>"
                 f"<height>{h}</height></samplecharacteristics></video>"
                 f"<audio><channelcount>2</channelcount></audio></media>")
    else:
        media = ("<media><audio><samplecharacteristics><depth>16</depth>"
                 "<samplerate>48000</samplerate></samplecharacteristics>"
                 "<channelcount>2</channelcount></audio></media>")
    url = f"{media_dir}/{name}" if media_dir else name
    return (f'<file id="{fid}"><name>{escape(name)}</name>'
            f"<pathurl>{escape(url)}</pathurl>{rate(fps)}<duration>{dur_f}</duration>{media}</file>")


def clipitem(cid, item, fps, w, h, media_dir, kind, emitted):
    name = item["file"]
    src_dur = frames(item.get("src_duration", item["src_out"]), fps)
    start = frames(item["start"], fps)
    end = start + frames(item["src_out"] - item["src_in"], fps)
    fid = "file-" + Path(name).stem
    return (f'<clipitem id="{cid}"><name>{escape(name)}</name><enabled>TRUE</enabled>'
            f"<duration>{src_dur}</duration>{rate(fps)}<start>{start}</start><end>{end}</end>"
            f"<in>{frames(item['src_in'], fps)}</in><out>{frames(item['src_out'], fps)}</out>"
            f"{file_el(fid, name, media_dir, src_dur, fps, w, h, kind, emitted)}"
            + ("<sourcetrack><mediatype>audio</mediatype><trackindex>1</trackindex></sourcetrack>"
               if kind == "audio" else "")
            + "</clipitem>")


def dissolve(at_f, half_f, fps):
    return ("<transitionitem>" + rate(fps) +
            f"<start>{at_f - half_f}</start><end>{at_f + half_f}</end>"
            "<alignment>center</alignment><effect><name>Cross Dissolve</name>"
            "<effectid>Cross Dissolve</effectid><effectcategory>Dissolve</effectcategory>"
            "<effecttype>transition</effecttype><mediatype>video</mediatype></effect>"
            "</transitionitem>")


def build(edit):
    fps, w, h = edit["fps"], edit["width"], edit["height"]
    media_dir = edit.get("media_dir", "media")
    emitted = set()
    vitems = []
    for i, v in enumerate(edit["video"], 1):
        d = v.get("dissolve_in", 0)
        if d and i > 1:
            vitems.append(dissolve(frames(v["start"], fps), frames(d / 2, fps), fps))
        vitems.append(clipitem(f"v{i}", v, fps, w, h, media_dir, "video", emitted))
    aitems = [clipitem(f"a{i}", a, fps, w, h, media_dir, "audio", emitted)
              for i, a in enumerate(edit.get("audio", []), 1)]
    total = max([frames(v["start"] + v["src_out"] - v["src_in"], fps) for v in edit["video"]] +
                [frames(a["start"] + a["src_out"] - a["src_in"], fps) for a in edit.get("audio", [])])
    fmt = (f"<format><samplecharacteristics>{rate(fps)}<width>{w}</width><height>{h}</height>"
           "<pixelaspectratio>square</pixelaspectratio></samplecharacteristics></format>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE xmeml>\n<xmeml version="4">'
            f'<sequence id="seq-1"><name>{escape(edit["name"])}</name><duration>{total}</duration>'
            f"{rate(fps)}<media><video>{fmt}<track>{''.join(vitems)}</track></video>"
            f"<audio><track>{''.join(aitems)}</track></audio></media></sequence></xmeml>\n")


if __name__ == "__main__":
    edit = json.loads(Path(sys.argv[1]).read_text())
    Path(sys.argv[2]).write_text(build(edit))
    print(f"wrote {sys.argv[2]}")
