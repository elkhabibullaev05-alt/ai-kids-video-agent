"""Max sing-along songs: music (MIDI → FluidSynth), character vocals (Kokoro, rhythmic chant on the beat),
segment timelines for the 3D renderer (choruses rendered twice and reused), lyric subtitles.
python3 songs/songmake.py songs/songs.json out3d/songs
Writes per song: <id>/audio.wav, <id>/plan.json, <id>/seg_<name>/timeline.json, <id>/lyrics.json
"""
import json, os, sys, random
import numpy as np, soundfile as sf, librosa, pretty_midi
from kokoro_onnx import Kokoro

SR = 44100; FPS = 12
SPEC = json.load(open(sys.argv[1])); OUT = sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
CAST = json.load(open(os.path.join(HERE, "..", "scripts3d", "cast.json")))
K = Kokoro("/opt/kokoro/kokoro.onnx", "/opt/kokoro/voices.bin")
SF2 = "/usr/share/sounds/sf2/TimGM6mb.sf2"
_tts = {}


def tts(who, text):
    key = (who, text)
    if key in _tts: return _tts[key]
    ch = CAST[who]
    a, sr = K.create(text, voice=ch["voice"], speed=ch.get("speed", 1.0) * 1.04, lang="en-gb" if ch["voice"][0] == "b" else "en-us")
    a = np.asarray(a, np.float32)
    semis = ch.get("pitch", 0)
    a = librosa.resample(a, orig_sr=sr, target_sr=SR)
    if semis: a = librosa.effects.pitch_shift(a, sr=SR, n_steps=semis)
    a, _ = librosa.effects.trim(a, top_db=35)
    a = a / (np.abs(a).max() + 1e-9) * 0.9
    _tts[key] = a
    return a


def fit(a, maxlen):
    if len(a) > maxlen:
        a = librosa.effects.time_stretch(a, rate=len(a) / maxlen)[:maxlen]
    return a


def vocal(who, text, maxlen, cast):
    if who != "all":
        return fit(tts(who, text), maxlen), who
    singers = [c for c in ("max", "mouse", "grandma", "dog", "bird") if c in cast][:3]
    parts = [tts(c, text) for c in singers]
    L = min(maxlen, int(np.mean([len(p) for p in parts])))
    mix = np.zeros(L, np.float32)
    for p in parts:
        q = librosa.effects.time_stretch(p, rate=len(p) / L)[:L]; mix[:len(q)] += q / len(parts) * 1.25
    return mix, "max"


CHORDS = {"I": [0, 4, 7], "IV": [5, 9, 12], "V": [7, 11, 14], "vi": [9, 12, 16], "ii": [2, 5, 9]}
PROG_CH = ["I", "V", "vi", "IV"]; PROG_V = ["I", "IV", "V", "I"]; PENTA = [0, 2, 4, 7, 9, 12]


def music(song, sections, bar, total):
    rnd = random.Random(song["id"])
    pm = pretty_midi.PrettyMIDI(initial_tempo=song["bpm"])
    lull = song.get("lullaby")
    chord_i = pretty_midi.Instrument(10 if lull else 24)        # music box | nylon guitar
    pad = pretty_midi.Instrument(89 if lull else 0)              # warm pad | piano
    bass = pretty_midi.Instrument(32)
    bell = pretty_midi.Instrument(9 if not lull else 10)         # glockenspiel melody
    drums = pretty_midi.Instrument(0, is_drum=True)
    root = song["key"]; beat = bar / 4
    motif = [rnd.choice(PENTA) for _ in range(8)]
    b0 = 0
    for name, nbars, kind in sections:
        prog = PROG_CH if kind == "chorus" else PROG_V
        for j in range(nbars):
            t = (b0 + j) * bar; ch = CHORDS[prog[(j // 2 if kind != "intro" else j) % 4]]
            for k in range(8 if not lull else 4):  # strum 8ths (lullaby: quarter arpeggio)
                st = t + k * bar / (8 if not lull else 4)
                notes = ch if not lull else [ch[k % 3]]
                for n_ in notes:
                    chord_i.notes.append(pretty_midi.Note(62 if k % 2 == 0 else 48, root + n_, st, st + bar / 8 * 0.9))
            for n_ in ch:
                pad.notes.append(pretty_midi.Note(34 if not lull else 40, root - 12 + n_, t, t + bar))
            bass.notes.append(pretty_midi.Note(80, root - 24 + ch[0], t, t + beat * 1.8))
            bass.notes.append(pretty_midi.Note(70, root - 24 + ch[1 if lull else 2] - (12 if not lull else 0) + 12, t + 2 * beat, t + 3.8 * beat))
            if not lull and kind != "intro" or (not lull and j >= 2):
                for q in range(4):
                    bt = t + q * beat
                    drums.notes.append(pretty_midi.Note(95 if q % 2 == 0 else 0, 36, bt, bt + 0.1))
                    if q % 2: drums.notes.append(pretty_midi.Note(80, 38 if kind != "chorus" else 39, bt, bt + 0.1))
                    for h in range(2): drums.notes.append(pretty_midi.Note(45, 42, bt + h * beat / 2, bt + h * beat / 2 + 0.05))
            # bell answers in the 2nd bar of each 2-bar line, and plays the hook in intro/outro
            if kind in ("intro", "outro") or j % 2 == 1:
                for q in range(4 if kind in ("intro", "outro") else 2):
                    st = t + (q + (0 if kind in ("intro", "outro") else 2)) * beat
                    nn = root + 12 + motif[(j * 4 + q) % 8]
                    bell.notes.append(pretty_midi.Note(70 if not lull else 55, nn, st, st + beat * 0.9))
        b0 += nbars
    pm.instruments += [chord_i, pad, bass, bell, drums]
    a = pm.fluidsynth(fs=SR, sf2_path=SF2)
    out = np.zeros(total, np.float32); out[:min(total, len(a))] = a[:total]
    return out / (np.abs(out).max() + 1e-9) * 0.8


all_meta = []
for song in SPEC["songs"]:
    D = os.path.join(OUT, song["id"]); os.makedirs(D, exist_ok=True)
    bar = 60 / song["bpm"] * 4
    secs = [("intro", 4, "intro")]
    order = ["A", 1, "B", 2, "A", 3, "B"]
    for o in order:
        secs.append((f"chorus{o}" if isinstance(o, str) else f"verse{o}", 8, "chorus" if isinstance(o, str) else "verse"))
    secs.append(("outro", 2, "outro"))
    # quantise everything to whole frames
    starts, f0 = [], 0
    for name, nb, kind in secs:
        nf = int(round(nb * bar * FPS)); starts.append((name, nb, kind, f0, nf)); f0 += nf
    total_f = f0; total = int(total_f / FPS * SR) + SR
    mus = music(song, secs, bar, total)
    voc = np.zeros(total, np.float32); duck = np.ones(total, np.float32)
    lyrics, segs = [], {}
    cast = song["cast"]
    for name, nb, kind, fs, nf in starts:
        lines = song["chorus"] if kind == "chorus" else (song["verses"][int(name[-1]) - 1] if kind == "verse" else [])
        t0 = fs / FPS
        beats = []
        if kind == "intro":
            beats.append({"cam": "wide", "hold": nb * bar, "start": 0.0, "dur": nb * bar, "do": [["all", "jump"]] + [[c, "happy"] for c in cast]})
            beats.append({"cam": f"close:{cast[0]}", "hold": 1, "start": round(nb * bar * 0.55, 3), "dur": nb * bar * 0.45, "do": [[cast[0], "spin"]]})
            lyrics.append({"t": t0 + 0.2, "end": t0 + nb * bar - 0.1, "text": song["name"], "card": True})
        elif kind == "outro":
            beats.append({"cam": "wide", "hold": nb * bar, "start": 0.0, "dur": nb * bar, "do": [["all", "laugh"]]})
        for li, (who, text) in enumerate(lines):
            st_local = li * 2 * bar + 0.06 * bar
            a, face = vocal(who, text, int(1.88 * bar * SR), cast)
            i = int((t0 + st_local) * SR); voc[i:i + len(a)] += a * (0.95 if who != "all" else 1.0)
            dl = len(a) / SR
            duck[max(0, i - 2000):i + len(a) + 4000] = 0.42
            hop = SR // FPS
            lv = [float(np.sqrt(np.mean(a[j:j + hop] ** 2))) for j in range(0, len(a), hop)]
            m = max(lv) or 1
            mouth = [round(min(1, v / m * 1.4), 2) for v in lv]
            if kind == "chorus":
                acts = [[["all", "jump"]], [[face, "spin"], ["all", "happy"]], [["all", "laugh"]], [["all", "happy"], [face, "jump"]]][li % 4]
                cams = (["wide", f"close:{face}", "overhead" if song["place"] != "house" else "wide", f"two:{cast[0]},{cast[1]}"] if name == "chorusA"
                        else [f"two:{cast[0]},{cast[2]}", "wide", f"close:{face}", "wide"])
                cam = cams[li % 4]
            else:
                others = [c for c in cast if c != face]
                acts = [[face, "happy"], [others[li % len(others)], "jump"]] + ([[face, "spin"]] if li == 3 else [])
                cam = f"close:{face}" if li % 2 == 0 else (f"two:{face},{others[li % len(others)]}" if li == 1 else "wide")
            beats.append({"who": face, "say": text, "cam": cam, "do": acts, "start": round(st_local, 3), "dur": round(dl, 3), "mouth": mouth})
            # a second camera inside the 2-bar slot keeps cuts every ~2–4 s
            beats.append({"cam": "wide" if cam != "wide" else f"close:{cast[(li + 1) % len(cast)]}", "hold": 1,
                          "start": round(li * 2 * bar + 1.2 * bar, 3), "dur": round(0.8 * bar, 3), "do": [[cast[(li + 2) % len(cast)], "laugh"]]})
            lyrics.append({"t": t0 + st_local - 0.15, "end": t0 + (li + 1) * 2 * bar - 0.1, "text": text, "who": who, "dur": dl})
        beats.sort(key=lambda b: b["start"])
        if name in ("chorusA", "chorusB", "intro", "outro") or kind == "verse":
            if name not in segs:
                segs[name] = nf
                SD = os.path.join(D, "seg_" + name); os.makedirs(SD, exist_ok=True)
                chars = {c: CAST[c] for c in cast}
                for i_, b in enumerate(beats): b["i"] = i_
                json.dump({"title": song["name"], "set": {"place": song["place"], "time": song["time"]}, "chars": chars,
                           "props": song.get("props", []), "fps": FPS, "duration": round((nf - 1) / FPS, 4), "seed": hash(song["id"] + name) % 1000,
                           "beats": beats}, open(os.path.join(SD, "timeline.json"), "w"), indent=1)
    mix = mus * duck * 0.8 + voc * 1.0
    mix = mix[:int(total_f / FPS * SR)]
    mix = mix / (np.abs(mix).max() + 1e-9) * 0.95
    sf.write(os.path.join(D, "audio.wav"), np.stack([mix, mix], 1), SR)
    plan = [{"seg": n if not n.startswith("chorus") else n, "frames": nf, "start_frame": fs} for n, nb, k, fs, nf in starts]
    json.dump({"song": song["id"], "name": song["name"], "frames": total_f, "plan": plan}, open(os.path.join(D, "plan.json"), "w"), indent=1)
    json.dump(lyrics, open(os.path.join(D, "lyrics.json"), "w"), indent=1)
    print(song["id"], "bars", sum(s[1] for s in secs), "sec", round(total_f / FPS, 1), "render frames", sum(segs.values()))
    all_meta.append((song["id"], total_f, sum(segs.values())))
print("TOTAL sec", round(sum(m[1] for m in all_meta) / FPS, 1), "render frames", sum(m[2] for m in all_meta))
