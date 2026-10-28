"""Zoom-out for clips whose reframe output does NOT keep the source pixel-locked (e.g. it re-rendered
the camera move). Tracks the reframe against the original frame by frame (SIFT + RANSAC similarity),
warps it under the original, then fills the remaining top gap with a second reframe.

Usage:
  python3 zoom_track.py stage   ORIG.mp4 REFRAME1.mp4 OUTDIR     # -> OUTDIR/stageA.mp4, mask.npy, p2src.mp4
  python3 zoom_track.py final   ORIG.mp4 OUTDIR REFRAME2.mp4 OUT.mp4
"""
import os, subprocess, sys
import cv2
import numpy as np

S, W, H = 0.85, 1080, 1920
OW, OH = round(W * S / 2) * 2, round(H * S / 2) * 2
OX, OY = (W - OW) // 2, H - OH
CANVAS = np.array([[S, 0, OX], [0, S, OY]], float)     # orig px -> canvas px


def frames(path):
    cap = cv2.VideoCapture(path)
    out = []
    while True:
        ok, f = cap.read()
        if not ok:
            break
        out.append(f)
    return out


def write(path, imgs, fps=24):
    p = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24",
                          "-s", f"{imgs[0].shape[1]}x{imgs[0].shape[0]}", "-r", str(fps), "-i", "-",
                          "-c:v", "libx264", "-crf", "12", "-pix_fmt", "yuv420p", path], stdin=subprocess.PIPE)
    for im in imgs:
        p.stdin.write(np.ascontiguousarray(im).tobytes())
    p.stdin.close(); p.wait()


def track(orig, ref):
    """Per-frame similarity orig->ref (scale, rot, tx, ty), smoothed."""
    sift = cv2.SIFT_create(3000)
    bf = cv2.BFMatcher()
    params = []
    for o, r in zip(orig, ref):
        go = cv2.cvtColor(cv2.resize(o, None, fx=0.5, fy=0.5), cv2.COLOR_BGR2GRAY)
        gr = cv2.cvtColor(cv2.resize(r, None, fx=0.5, fy=0.5), cv2.COLOR_BGR2GRAY)
        ko, do = sift.detectAndCompute(go, None)
        kr, dr = sift.detectAndCompute(gr, None)
        good = [m for m, n in bf.knnMatch(do, dr, k=2) if m.distance < 0.75 * n.distance]
        po = np.float32([ko[m.queryIdx].pt for m in good]) * 2
        pr = np.float32([kr[m.trainIdx].pt for m in good]) * 2
        M, inl = cv2.estimateAffinePartial2D(po, pr, method=cv2.RANSAC, ransacReprojThreshold=4)
        s = np.hypot(M[0, 0], M[1, 0]); a = np.arctan2(M[1, 0], M[0, 0])
        params.append([s, a, M[0, 2], M[1, 2], int(inl.sum())])
    P = np.array(params)
    k = 7  # temporal smoothing window
    sm = P.copy()
    for j in range(4):
        sm[:, j] = np.convolve(np.pad(P[:, j], k // 2, mode="edge"), np.ones(k) / k, mode="valid")
    return sm, P


def to_mat(p):
    s, a, tx, ty = p[:4]
    return np.array([[s * np.cos(a), -s * np.sin(a), tx], [s * np.sin(a), s * np.cos(a), ty]])


def ref_to_canvas(p):
    M = np.vstack([to_mat(p), [0, 0, 1]])           # orig -> ref
    C = np.vstack([CANVAS, [0, 0, 1]])              # orig -> canvas
    return (C @ np.linalg.inv(M))[:2]               # ref -> canvas


def stage(orig_p, ref_p, outdir):
    os.makedirs(outdir, exist_ok=True)
    orig, ref = frames(orig_p), frames(ref_p)
    n = min(len(orig), len(ref)); orig, ref = orig[:n], ref[:n]
    sm, raw = track(orig, ref)
    print("scale range %.3f-%.3f, inliers min %d" % (sm[:, 0].min(), sm[:, 0].max(), raw[:, 4].min()))
    imgs, masks = [], []
    for r, p in zip(ref, sm):
        T = ref_to_canvas(p)
        imgs.append(cv2.warpAffine(r, T, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT))
        m = cv2.warpAffine(np.full(r.shape[:2], 255, np.uint8), T, (W, H), flags=cv2.INTER_NEAREST)
        masks.append(m)
    write(f"{outdir}/stageA.mp4", imgs)
    M = np.stack(masks)
    np.save(f"{outdir}/mask.npy", M)
    np.save(f"{outdir}/params.npy", sm)
    top = int(max(np.argmax(m.any(1)) for m in M)) + 4     # lowest first-covered row over all frames
    print("stageA top coverage edge (worst frame):", top)
    # pass2 source: the part every frame covers, full width
    hh = (H - top) // 2 * 2
    write(f"{outdir}/p2src.mp4", [im[top:top + hh] for im in imgs])
    open(f"{outdir}/top.txt", "w").write(str(top))


def measure(src_imgs, out_imgs, n):
    """Similarity src->out on one frame (for the pass2 placement)."""
    sift = cv2.SIFT_create(3000); bf = cv2.BFMatcher()
    a = cv2.cvtColor(src_imgs[n], cv2.COLOR_BGR2GRAY); b = cv2.cvtColor(out_imgs[n], cv2.COLOR_BGR2GRAY)
    ka, da = sift.detectAndCompute(a, None); kb, db = sift.detectAndCompute(b, None)
    good = [m for m, k in bf.knnMatch(da, db, k=2) if m.distance < 0.75 * k.distance]
    pa = np.float32([ka[m.queryIdx].pt for m in good]); pb = np.float32([kb[m.trainIdx].pt for m in good])
    M, inl = cv2.estimateAffinePartial2D(pa, pb, method=cv2.RANSAC, ransacReprojThreshold=3)
    return M, int(inl.sum())


def final(orig_p, outdir, p2_p, out_p):
    orig = frames(orig_p)
    A = frames(f"{outdir}/stageA.mp4")
    src2 = frames(f"{outdir}/p2src.mp4")
    P2 = frames(p2_p)
    masks = np.load(f"{outdir}/mask.npy")
    top = int(open(f"{outdir}/top.txt").read())
    n = min(len(orig), len(A), len(P2), len(src2))
    # pass2 placement (src2 -> P2), measured on a few frames and averaged
    Ms = [measure(src2, P2, i)[0] for i in (n // 4, n // 2, 3 * n // 4)]
    M = np.mean(Ms, 0)
    Mi = np.vstack([M, [0, 0, 1]])
    shift = np.array([[1, 0, 0], [0, 1, top], [0, 0, 1]], float)   # src2 px -> canvas px
    T2 = (shift @ np.linalg.inv(Mi))[:2]                            # P2 px -> canvas px
    print("pass2 scale %.3f" % np.hypot(T2[0, 0], T2[1, 0]))
    out = []
    ft, fs = 160, 40
    yy, xx = np.mgrid[0:OH, 0:OW]
    a_orig = np.minimum(1, np.minimum(yy / ft, np.minimum(xx / fs, (OW - 1 - xx) / fs)))[..., None]
    gains = None
    for i in range(n):
        bg = cv2.warpAffine(P2[i], T2, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE).astype(float)
        a = A[i].astype(float)
        if gains is None:   # match pass2 colour to stageA where both exist (band just below `top`)
            band = (slice(top + 10, top + 250), slice(0, W))
            gains = a[band].reshape(-1, 3).mean(0) / np.maximum(bg[band].reshape(-1, 3).mean(0), 1)
            print("colour gains bgr:", np.round(gains, 3))
        bg *= gains
        m = masks[i].astype(float) / 255
        m = cv2.GaussianBlur(cv2.erode(m, np.ones((9, 9))), (0, 0), 30)[..., None]  # soft top edge of stageA
        comp = bg * (1 - m) + a * m
        o = cv2.resize(orig[i], (OW, OH), interpolation=cv2.INTER_AREA).astype(float)
        reg = comp[OY:OY + OH, OX:OX + OW]
        comp[OY:OY + OH, OX:OX + OW] = reg * (1 - a_orig) + o * a_orig
        out.append(np.clip(comp, 0, 255).astype(np.uint8))
    write(out_p, out)


if __name__ == "__main__":
    {"stage": stage, "final": final}[sys.argv[1]](*sys.argv[2:])
