"""Frame engine: moving 'camera' over sketch images, timed overlays, parallel segment encoding, final mux."""
import math
import multiprocessing as mp
import os
import random
import subprocess

import numpy as np
from PIL import Image

import art

FPS = 30
_G = {}  # filled before the pool forks (copy-on-write in the workers)


def ff(args, **kw):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostdin", "-v", "error", "-y"] + args, capture_output=True, text=True, **kw)
    if r.returncode:
        raise RuntimeError("ffmpeg: " + r.stderr[-800:])
    return r


# ------------------------------------------------------------------ camera
def plan_shots(dur, rng, shot_len, first=False, end_at=None):
    """List of shots (t0, t1, (z0, cx0, cy0), (z1, cx1, cy1)). A jump between shots = 'punch-in' cut."""
    shots, t = [], 0.0
    lens = []
    while t < dur - 0.05:
        L = shot_len * rng.uniform(0.85, 1.15)
        if first and t < 3.2:
            L = 1.0
        if dur - (t + L) < shot_len * 0.5:
            L = dur - t
        lens.append((t, min(dur, t + L)))
        t += L
    prev_z = None
    for i, (a, b) in enumerate(lens):
        if first and i == 0:
            s0, s1 = (1.42, 0.5, 0.45), (1.12, 0.5, 0.45)  # slam-in on frame 0
        else:
            z = rng.uniform(1.02, 1.32)
            if prev_z is not None and abs(z - prev_z) < 0.12:
                z = 1.02 + (z - 1.02 + 0.15) % 0.30
            cx, cy = rng.uniform(0.38, 0.62), rng.uniform(0.38, 0.6)
            dz = rng.choice([0.07, 0.09, -0.06])
            s0 = (z, cx, cy)
            s1 = (max(1.0, z + dz), cx + rng.uniform(-0.04, 0.04), cy + rng.uniform(-0.03, 0.03))
        prev_z = s0[0]
        shots.append((a, b, s0, s1))
    if end_at is not None and shots:
        a, b, s0, _ = shots[-1]
        shots[-1] = (a, b, s0, end_at)
    return shots


def cam_at(shots, t):
    for a, b, s0, s1 in shots:
        if t < b or (a, b, s0, s1) == shots[-1]:
            u = min(1.0, max(0.0, (t - a) / max(1e-3, b - a)))
            if s0[0] > 1.3 and s1[0] < s0[0] - 0.2:  # slam: ease out fast
                u = 1 - (1 - min(1.0, u * 2.2)) ** 3
            else:
                u = u * u * (3 - 2 * u)
            return tuple(s0[i] + (s1[i] - s0[i]) * u for i in range(3))
    return shots[-1][3]


def view(base_img, out_w, out_h, z, cx, cy):
    """Crop of a PIL base image at zoom z (1 = whole image) centred at (cx, cy) (0..1), resampled to out size."""
    bw, bh = base_img.size
    cw, ch = bw / z, bh / z
    x0 = min(max(cx * bw - cw / 2, 0), bw - cw)
    y0 = min(max(cy * bh - ch / 2, 0), bh - ch)
    im = base_img.transform((out_w, out_h), Image.EXTENT, (x0, y0, x0 + cw, y0 + ch), Image.BILINEAR)
    return np.asarray(im)


def reveal_mask(w, h, seed):
    rng = np.random.default_rng(seed)
    low = Image.fromarray((rng.random((h // 24 + 1, w // 24 + 1)) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
    n = np.asarray(low, np.float32) / 255
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    g = (xx / w * 0.6 + yy / h * 0.4)
    return (0.55 * g + 0.45 * n).astype(np.float32)


# ------------------------------------------------------------------ segment worker
def _render_scene(i):
    S = _G["scenes"][i]
    W, H = _G["W"], _G["H"]
    out = os.path.join(_G["work"], f"seg_{i:03d}.mp4")
    n = S["n"]
    p = subprocess.Popen(["ffmpeg", "-hide_banner", "-nostdin", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                          "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast",
                          "-crf", "20", "-pix_fmt", "yuv420p", "-threads", "2", "-r", str(FPS), out],
                         stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    base = Image.fromarray(_G["bases"][S["base"]]) if S.get("base") is not None else None
    ovs = [(art.to_overlay(Image.open(o["png"]).convert("RGBA"), o["x"], o["y"]), o) for o in S["overlays"]]
    card = S.get("card")  # (x, y, w, h) where the camera view goes; None = full frame
    bg = _G["bgs"].get(S.get("bg"))
    rmask = None
    if S.get("reveal"):
        cw, ch = (card[2], card[3]) if card else (W, H)
        rmask = reveal_mask(cw, ch, i)
        rpaper = art.paper(cw, ch, 11).astype(np.float32)
    for f in range(n):
        t = f / FPS
        if S.get("special") == "subscribe":
            fr = _G["subscribe"](t)
        else:
            z, cx, cy = cam_at(S["shots"], t)
            if card:
                fr = bg.copy()
                v = view(base, card[2], card[3], z, cx, cy)
            else:
                v = view(base, W, H, z, cx, cy).copy()
            if rmask is not None and t < 0.4:
                pr = t / 0.4 * 1.25
                m = np.clip((pr - rmask) / 0.18, 0, 1)[..., None]
                v = (rpaper * (1 - m) + v.astype(np.float32) * m).astype(np.uint8)
            if card:
                fr[card[1]:card[1] + card[3], card[0]:card[0] + card[2]] = v
            else:
                fr = v if v.flags.writeable else v.copy()
        for ov, o in ovs:
            if o["t0"] <= t < o["t1"]:
                a = 1.0
                if o.get("fade_in"):
                    a = min(1.0, (t - o["t0"]) / o["fade_in"])
                if o.get("fade_out"):
                    a = min(a, max(0.0, (o["t1"] - t) / o["fade_out"]))
                if a > 0:
                    art.composite(fr, ov, a)
        try:
            p.stdin.write(np.ascontiguousarray(fr, dtype=np.uint8).tobytes())
        except BrokenPipeError:
            raise RuntimeError(f"ffmpeg died (scene {i}, frame shape {fr.shape}): " + p.stderr.read().decode()[-400:])
    p.stdin.close()
    err = p.stderr.read().decode()
    if p.wait():
        raise RuntimeError("segment encode failed: " + err[-400:])
    return out


def render_video(scenes, bases, bgs, W, H, work, audio_wav, out_mp4, subscribe=None, procs=None):
    """scenes: list of dicts {n, base, shots, overlays, card?, bg?, reveal?, special?}."""
    _G.update(scenes=scenes, bases=bases, bgs=bgs, W=W, H=H, work=work, subscribe=subscribe)
    procs = procs or max(1, min(10, (os.cpu_count() or 2) // 2))
    if procs > 1:
        with mp.get_context("fork").Pool(procs) as pool:
            segs = pool.map(_render_scene, range(len(scenes)), chunksize=1)
    else:
        segs = [_render_scene(i) for i in range(len(scenes))]
    lst = os.path.join(work, "segs.txt")
    with open(lst, "w") as fh:
        for s in segs:
            fh.write(f"file '{s}'\n")
    vid = os.path.join(work, "video.mp4")
    ff(["-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", vid])
    ff(["-i", vid, "-i", audio_wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
        "-af", "loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-shortest", "-movflags", "+faststart", out_mp4])
    return out_mp4
