#!/usr/bin/env python3
"""Write a Premiere-importable FCP7 XML for an assembled edit, via OpenTimelineIO.

Usage: premiere_otio.py edit.json PREMIERE_DIR [media_url_prefix]

Reads the same edit.json as assemble.py and the conformed media that assemble.py wrote to
PREMIERE_DIR/media, and writes PREMIERE_DIR/<name>.xml (a project containing one sequence).
media_url_prefix defaults to "media/" (relative; Premiere asks to relink once). Pass an
absolute folder, e.g. "file:///Users/me/Desktop/premiere/media/", to open without relinking.
"""
import json
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import opentimelineio as otio


def probe_frames(path, fps):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(path)], capture_output=True, text=True, check=True)
    return int(float(out.stdout.strip()) * fps)


def main(edit_path, pkg, prefix="media/"):
    edit = json.loads(Path(edit_path).read_text())
    pkg = Path(pkg)
    fps = edit["fps"]
    rt = lambda f: otio.opentime.RationalTime(f, fps)

    timeline = otio.schema.Timeline(name=edit["name"])
    timeline.global_start_time = rt(0)
    vtrack = otio.schema.Track(name="V1", kind=otio.schema.TrackKind.Video)
    t = 0.0
    for v in edit["video"]:
        name = Path(v["file"]).stem + ".mp4"
        length = v["src_out"] - v["src_in"]
        # frame-exact cut points on the song timeline, so nothing drifts
        n_frames = round((t + length) * fps) - round(t * fps)
        t += length
        ref = otio.schema.ExternalReference(
            target_url=prefix + name,
            available_range=otio.opentime.TimeRange(rt(0), rt(probe_frames(pkg / "media" / name, fps))))
        vtrack.append(otio.schema.Clip(
            name=name, media_reference=ref,
            source_range=otio.opentime.TimeRange(rt(round(v["src_in"] * fps)), rt(n_frames))))
    timeline.tracks.append(vtrack)

    if edit.get("audio"):
        name = Path(edit["audio"]["file"]).stem + ".wav"
        total = round(t * fps)
        afr = probe_frames(pkg / "media" / name, fps)
        ref = otio.schema.ExternalReference(
            target_url=prefix + name,
            available_range=otio.opentime.TimeRange(rt(0), rt(afr)))
        atrack = otio.schema.Track(name="A1", kind=otio.schema.TrackKind.Audio)
        atrack.append(otio.schema.Clip(
            name=name, media_reference=ref,
            source_range=otio.opentime.TimeRange(rt(round(edit["audio"].get("src_in", 0) * fps)),
                                                 rt(min(total, afr)))))
        timeline.tracks.append(atrack)

    out = pkg / (edit["name"].replace(" ", "_") + ".xml")
    otio.adapters.write_to_file(timeline, str(out), adapter_name="fcp_xml")
    fill_formats(out, fps, edit["width"], edit["height"])
    print(f"wrote {out}: {len(vtrack)} clips, {t:.2f}s")


def rate_el(fps):
    r = ET.Element("rate")
    ET.SubElement(r, "timebase").text = str(fps)
    ET.SubElement(r, "ntsc").text = "FALSE"
    return r


def video_chars(fps, w, h):
    sc = ET.Element("samplecharacteristics")
    sc.append(rate_el(fps))
    for tag, val in (("width", w), ("height", h), ("anamorphic", "FALSE"),
                     ("pixelaspectratio", "square"), ("fielddominance", "none"), ("colordepth", 24)):
        ET.SubElement(sc, tag).text = str(val)
    return sc


def audio_chars():
    sc = ET.Element("samplecharacteristics")
    ET.SubElement(sc, "depth").text = "16"
    ET.SubElement(sc, "samplerate").text = "48000"
    return sc


def fill_formats(path, fps, w, h):
    """OTIO leaves the sequence format and file media empty; Premiere needs them to build
    a vertical sequence and to know what each file contains."""
    tree = ET.parse(path)
    seq = tree.getroot().find(".//sequence")
    fmt = seq.find("media/video/format")
    fmt.clear()
    fmt.append(video_chars(fps, w, h))
    seq_audio = seq.find("media/audio")
    if seq_audio is not None and seq_audio.find("format") is None:
        seq_audio.insert(0, ET.Element("numOutputChannels"))
        seq_audio[0].text = "2"
        af = ET.Element("format")
        af.append(audio_chars())
        seq_audio.insert(1, af)
    for kind in ("video", "audio"):
        for i, clip in enumerate(seq.iterfind(f"media/{kind}/track/clipitem"), 1):
            for extra in clip.findall("rate")[1:]:
                clip.remove(extra)
            masterclip = ET.Element("masterclipid")
            masterclip.text = f"masterclip-{kind}-{i}"
            clip.insert(0, masterclip)
            enabled = ET.Element("enabled")
            enabled.text = "TRUE"
            clip.insert(2, enabled)
            if kind == "audio":
                st = ET.SubElement(clip, "sourcetrack")
                ET.SubElement(st, "mediatype").text = "audio"
                ET.SubElement(st, "trackindex").text = "1"
            # same child order Premiere itself exports
            order = ["masterclipid", "name", "enabled", "duration", "rate", "start", "end",
                     "in", "out", "file", "sourcetrack"]
            children = sorted(list(clip), key=lambda e: order.index(e.tag) if e.tag in order else 99)
            for child in list(clip):
                clip.remove(child)
            clip.extend(children)
    for f in tree.getroot().iter("file"):
        media = f.find("media")
        if media is None:
            continue
        media.clear()
        if f.findtext("name", "").endswith(".wav"):
            a = ET.SubElement(media, "audio")
            a.append(audio_chars())
            ET.SubElement(a, "channelcount").text = "2"
        else:
            ET.SubElement(media, "video").append(video_chars(fps, w, h))
    ET.indent(tree)
    tree.write(path, encoding="UTF-8", xml_declaration=True)


if __name__ == "__main__":
    main(*sys.argv[1:4])
