"""Parallel frame renderer: frame_fn(i) -> PIL RGB image; chunks rendered in forked workers, concatenated, muxed."""
import multiprocessing as mp
import os
import shutil
import subprocess
import tempfile

_FN = None
_ARGS = None


def _chunk(job):
    a, b, path = job
    w, h, fps = _ARGS
    p = subprocess.Popen(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                          "-s", f"{w}x{h}", "-r", str(fps), "-i", "-", "-c:v", "libx264", "-preset", "veryfast",
                          "-crf", "19", "-pix_fmt", "yuv420p", "-g", str(fps * 2), "-threads", "2", path],
                         stdin=subprocess.PIPE)
    for i in range(a, b):
        im = _FN(i)
        if im.size != (w, h) or im.mode != "RGB":
            im = im.convert("RGB").resize((w, h))
        p.stdin.write(im.tobytes())
    p.stdin.close()
    if p.wait():
        raise RuntimeError("ffmpeg chunk failed")
    return path


def render(frame_fn, nframes, w, h, fps, audio_wav, out_mp4, workers=None):
    global _FN, _ARGS
    _FN, _ARGS = frame_fn, (w, h, fps)
    workers = workers or max(1, min(8, (os.cpu_count() or 2) // 2 or 1))
    tmp = tempfile.mkdtemp(prefix="rbxr_", dir=os.path.dirname(os.path.abspath(out_mp4)))
    try:
        n = max(1, min(workers * 3, nframes // (fps * 2) or 1))
        bounds = [round(nframes * k / n) for k in range(n + 1)]
        jobs = [(bounds[k], bounds[k + 1], os.path.join(tmp, f"c{k:03d}.mp4")) for k in range(n) if bounds[k + 1] > bounds[k]]
        if workers > 1 and len(jobs) > 1:
            with mp.get_context("fork").Pool(workers) as pool:
                parts = pool.map(_chunk, jobs, chunksize=1)
        else:
            parts = [_chunk(j) for j in jobs]
        lst = os.path.join(tmp, "list.txt")
        with open(lst, "w") as f:
            for p in parts:
                f.write(f"file '{p}'\n")
        r = subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0",
                            "-i", lst, "-i", audio_wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac",
                            "-b:a", "192k", "-shortest", "-movflags", "+faststart", out_mp4],
                           capture_output=True, text=True)
        if r.returncode:
            raise RuntimeError("mux failed: " + r.stderr[-400:])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return out_mp4
