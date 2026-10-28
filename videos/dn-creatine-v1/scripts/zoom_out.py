"""Bottom-anchored zoom-out of a 9:16 clip, keeping the original pixels and motion.

Two Higgsfield reframe passes supply only the NEW edges:
  pass1  9:16 -> 3:4 (extends the sides; source kept at the same scale, centred)
  pass2  a top crop of pass1 -> 9:16 (extends the top; reframe may also shrink the source
         and pad every side, so its placement is MEASURED, not assumed)
Composite: pass2 = continuous background, pass1 sides fade in low in the frame,
original full-res clip on top with feathered edges. Content ends at scale S, bottom-anchored.

Usage:
  python3 zoom_out.py prep  PASS1.mp4 OUT_pass2_src.mp4
  python3 zoom_out.py comp  ORIG.mp4 PASS1.mp4 PASS2_SRC.mp4 PASS2.mp4 OUT.mp4
"""
import json, subprocess, sys
import numpy as np

S = 0.85                       # final scale of the original content (bottom-anchored)
W, H = 1080, 1920
FF = ["ffmpeg", "-nostdin", "-v", "error", "-y"]

U_H = 960                                      # pass1 working height (3:4 -> 720x960)
WF = round(540 / S / 2) * 2                    # canvas width in pass1 units (636)
E = U_H / S - U_H                              # top extension needed, pass1 units (~169)
H2 = round((WF * 16 / 9 - 2 * E) / 2) * 2      # pass2 source height (792)


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries",
                          "stream=width,height", "-of", "json", path], capture_output=True, text=True).stdout
    s = json.loads(out)["streams"][0]
    return s["width"], s["height"]


def gray(path, n, w, h):
    raw = subprocess.run(FF[:-1] + ["-i", path, "-vf", f"select=eq(n\\,{n}),scale={w}:{h}",
                                    "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "gray", "-"],
                         capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(h, w).astype(float)


def measure(src, out, n=40):
    """Find where (scale, x, y in out px) the source frame sits inside the reframe output."""
    ow, oh = probe(out)
    sw, sh = probe(src)
    q = 4
    O2 = gray(out, n, ow // q, oh // q)
    best = None
    for sc in np.arange(0.30, 1.001, 0.02):        # coarse, quarter-res
        w, h = round(sw * sc / q), round(sh * sc / q)
        if w > ow // q or h > oh // q:
            break
        Sg = gray(src, n, w, h)
        for x in range(0, ow // q - w + 1):
            for y in range(0, oh // q - h + 1):
                d = np.abs(O2[y:y + h, x:x + w] - Sg).mean()
                if best is None or d < best[0]:
                    best = (d, sc, q * x, q * y)
    _, sc0, x0, y0 = best
    O = gray(out, n, ow, oh)
    best = None
    for sc in np.arange(sc0 - 0.022, sc0 + 0.0221, 0.002):  # fine, full-res
        w, h = round(sw * sc), round(sh * sc)
        if w > ow or h > oh:
            continue
        Sg = gray(src, n, w, h)
        for x in range(max(0, x0 - 6), min(ow - w, x0 + 6) + 1):
            for y in range(max(0, y0 - 8), min(oh - h, y0 + 8) + 1):
                d = np.abs(O[y:y + h, x:x + w] - Sg).mean()
                if best is None or d < best[0]:
                    best = (d, sc, x, y)
    print(f"measure {out}: diff={best[0]:.2f} scale={best[1]:.3f} at ({best[2]},{best[3]})")
    return best[1:]


def rgb(path, n, vf, w, h):
    raw = subprocess.run(FF[:-1] + ["-i", path, "-vf", f"select=eq(n\\,{n}),{vf}", "-frames:v", "1",
                                    "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(h, w, 3).astype(float)


def colour_gains(orig, p2, aw, ah, ax, ay, ow_, oh_, ox, oy, n=40):
    """Per-channel gains that match pass2 to the original in the overlap band just below its top edge."""
    A = rgb(p2, n, f"scale={aw}:{ah},pad={max(aw, W - ax)}:{max(ah, H - ay)}:0:0,"
                   f"crop={W}:{H}:{-ax}:{-ay}", W, H)
    O = rgb(orig, n, f"scale={ow_}:{oh_}", ow_, oh_)
    band = slice(20, 260)
    a = A[oy + 20:oy + 260, ox:ox + ow_].reshape(-1, 3).mean(0)
    o = O[band].reshape(-1, 3).mean(0)
    g = np.clip(o / np.maximum(a, 1), 0.7, 1.4)
    print("colour gains r/g/b:", np.round(g, 3))
    return g


def prep(p1, out):
    vf = f"scale=-2:{U_H},crop={WF}:{H2}:(iw-{WF})/2:0,setsar=1"
    subprocess.run(FF + ["-i", p1, "-vf", vf, "-an", "-c:v", "libx264", "-crf", "12",
                         "-pix_fmt", "yuv420p", out], check=True)


def comp(orig, p1, p2src, p2, out):
    k = W / WF                                  # canvas px per pass1 unit
    # pass1: 3:4, source centred at the same scale (verified) -> pass1 layer, bottom-anchored
    bh = round(U_H * k)
    by = H - bh
    # pass2: measured placement of its source (WF x H2 units) inside the output
    sc, mx, my = measure(p2src, p2)
    p2w, p2h = probe(p2)
    srcw_px = probe(p2src)[0]
    g = (WF * k) / (sc * srcw_px)              # canvas px per pass2 output px
    aw, ah = round(p2w * g / 2) * 2, round(p2h * g / 2) * 2
    ax, ay = round(-mx * g), round(E * k - my * g)
    ow_, oh_ = round(W * S / 2) * 2, round(H * S / 2) * 2
    ox, oy = (W - ow_) // 2, H - oh_
    ft, fs = 160, 40                           # feather: top / sides of the original layer
    gr, gg, gb = colour_gains(orig, p2, aw, ah, ax, ay, ow_, oh_, ox, oy)
    seam = round((E + H2) * k) - by            # pass2's invented bottom starts here (pass1-local y)
    c0, c1 = seam - 140, seam - 40
    fc = (
        f"color=black:s={W}x{H}:r=24[bg];"
        f"[3:v]fps=24,scale={aw}:{ah},setsar=1,format=gbrp,"
        f"colorchannelmixer=rr={gr:.4f}:gg={gg:.4f}:bb={gb:.4f},format=yuv420p[a0];"
        f"[bg][a0]overlay={ax}:{ay}:shortest=1,fillborders=top={max(0, ay)}:mode=smear[a];"
        f"[1:v]fps=24,scale=-2:{bh},crop={W}:{bh},setsar=1,format=yuva420p,"
        f"geq=lum='lum(X,Y)':cb='cb(X,Y)':cr='cr(X,Y)':a='255*clip((Y-{c0})/{c1 - c0},0,1)'[b];"
        f"[0:v]fps=24,scale={ow_}:{oh_},setsar=1,format=yuva420p,"
        f"geq=lum='lum(X,Y)':cb='cb(X,Y)':cr='cr(X,Y)':"
        f"a='255*min(1,min(Y/{ft},min(X/{fs},(W-1-X)/{fs})))'[c];"
        f"[a][b]overlay=0:{by}:shortest=1[ab];[ab][c]overlay={ox}:{oy}:shortest=1,format=yuv420p[v]"
    )
    subprocess.run(FF + ["-i", orig, "-i", p1, "-i", p2src, "-i", p2, "-filter_complex", fc,
                         "-map", "[v]", "-an", "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p",
                         out], check=True)
    print(f"pass2 {aw}x{ah} at ({ax},{ay}); pass1 layer y={by}; original {ow_}x{oh_} at ({ox},{oy})")


if __name__ == "__main__":
    {"prep": prep, "comp": comp}[sys.argv[1]](*sys.argv[2:])
