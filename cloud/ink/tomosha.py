"""Tomoshabin bahosi — videoni oddiy tomoshabin ko'zi bilan 100 ballik tizimda baholaydi.

Tomoshabin "swipe" qiladigan sabablar tekshiriladi:
- boshida bo'sh ekran, salom-alik yoki sekin gap;
- 3 soniyadan ko'p bir xil kadr;
- va'da qilingan narsa yo'q, raqam/fakt yo'q;
- oxirida nima qilish kerakligi aytilmagan.

85 dan past video yuklanmaydi (texnik rek-ball ham 85 dan o'tishi shart).
"""
import re

TRIG = re.compile(r"\?|\b(you|your|never|secret|why|what happens|most|only|deadly|strangest|nobody|actually|really|"
                  r"biggest|fastest|impossible|terrifying|shock|weird|truth|wrong)\b", re.I)
GREET = re.compile(r"^\s*(hi|hello|hey (guys|everyone)|welcome|in this video|today we)", re.I)
LOOP = re.compile(r"(at the (very )?end|last one|number one|stay (to|until)|wait (until|till)|later|by the end|strangest one)", re.I)
REHOOK = re.compile(r"(\bbut\b|here's|twist|\bnow\b|\?|imagine|guess)", re.I)
NUM = re.compile(r"\b\d[\d,.]*\b|\b(one|two|three|four|five|six|seven|eight|nine|ten|twenty|thirty|forty|fifty|hundred|thousand|million|billion)\b", re.I)
STOP = set("the a an and or of to in on at is are was were it its this that for with as be by from".split())


def _words(s):
    return [w for w in re.findall(r"[a-z']+", s.lower()) if w not in STOP]


def baho(script: dict, kind: str, seconds: float, max_gap: float, cta: bool, captions: bool) -> dict:
    """kind: long | short. max_gap: kadr o'zgarmay turgan eng uzun vaqt (s). -> {ball, qism, muammo}"""
    scenes = script["scenes"] if kind == "long" else script["short"]["scenes"]
    say = [s.get("say", "") for s in scenes]
    text = " ".join(say)
    first = re.split(r"(?<=[.!?])\s+", say[0].strip())[0] if say else ""
    hook = scenes[0].get("hook", "") if scenes else ""
    q, s = [], {}

    # A. Birinchi 3 soniya (30)
    a = 0
    a += 8 if hook and len(hook.split()) <= 7 else (4 if hook else 0)
    a += 6  # ovoz 0-soniyadan boshlanadi (ink.voice birinchi sahnada kechikish qo'ymaydi)
    a += 6 if len(first.split()) <= 14 else 3 if len(first.split()) <= 20 else 0
    a += 5 if TRIG.search(first + " " + hook) else 0
    a += 5 if not GREET.search(say[0] if say else "") else 0
    s["birinchi_3s"] = a
    if not hook:
        q.append("1-sahnada ekrandagi katta savol (hook) yo'q")
    if len(first.split()) > 14:
        q.append(f"birinchi gap uzun ({len(first.split())} so'z) — 14 tagacha qisqartiring")
    if not TRIG.search(first + " " + hook):
        q.append("birinchi gapda qiziqtiradigan savol/da'vo yo'q")
    if GREET.search(say[0] if say else ""):
        q.append("salom-alik bilan boshlanyapti — tomoshabin ketadi")

    # B. Ushlab turish (35)
    b = 0
    early = " ".join(say[:4])
    if kind == "long":
        b += 7 if LOOP.search(early) else 0
        if not LOOP.search(early):
            q.append("boshida 'eng qizig'i oxirida' va'dasi (open loop) yo'q")
    else:
        b += 7 if ("?" in text or TRIG.search(" ".join(say[1:3]))) else 3
    b += 8 if max_gap <= 3.0 else 4 if max_gap <= 4.5 else 0
    if max_gap > 3.0:
        q.append(f"kadr {max_gap:.1f} s o'zgarmaydi (3 s dan oshmasin)")
    sents = [x for x in re.split(r"(?<=[.!?])\s+", text) if x.strip()]
    avg = sum(len(x.split()) for x in sents) / max(1, len(sents))
    b += 6 if 6 <= avg <= 20 else 3 if avg <= 26 else 0
    if avg > 20:
        q.append(f"gaplar uzun (o'rtacha {avg:.0f} so'z) — jonli gapirgandek qisqa gaplar kerak")
    nums = len(NUM.findall(text))
    need = 8 if kind == "long" else 2
    b += 6 if nums >= need else 3 if nums >= need // 2 else 0
    if nums < need:
        q.append(f"aniq raqam/fakt kam ({nums})")
    if kind == "long":
        per_min = len(REHOOK.findall(text)) / max(1.0, seconds / 60)
        b += 4 if per_min >= 1 else 2 if per_min >= 0.5 else 0
        nn = sum(1 for x in scenes if x.get("num"))
        b += 4 if nn >= 3 else 2 if nn else 0
    else:
        b += 4 if captions else 0
        loop_ok = len(set(_words(say[-1])) & set(_words(say[0]))) >= 2 and scenes[0].get("img") == scenes[-1].get("img")
        b += 4 if loop_ok else 1
        if not loop_ok:
            q.append("Shorts oxiri boshiga ulanmaydi (loop)")
    s["ushlab_turish"] = b

    # C. Yakun (15)
    c = 8 if cta else 0
    last = " ".join(say[-2:]).lower()
    if kind == "long":
        c += 4 if ("comment" in last or "?" in last) else 0
    else:
        c += 4 if cta else 0
    c += 3 if cta else 0
    s["yakun"] = c
    if not cta:
        q.append("oxirida obuna / uzun videoga chaqiriq yo'q")

    # D. Uzunlik va ishonch (20)
    d = 0
    if kind == "long":
        d += 10 if 480 <= seconds <= 720 else 6 if 420 <= seconds < 480 or 720 < seconds <= 900 else 2
        if seconds < 480:
            q.append(f"uzun video {seconds / 60:.1f} daqiqa — 8 daqiqadan kam (o'rtadagi reklama yo'q)")
    else:
        d += 10 if 40 <= seconds <= 60 else 6 if 30 <= seconds < 40 or 60 < seconds <= 75 else 2
    d += 5 if len(script.get("sources", [])) >= 2 else 2 if script.get("sources") else 0
    title = (script.get("title") if kind == "long" else script["short"].get("title")) or ""
    d += 5 if (len(title) <= 70 and TRIG.search(title + " " + script.get("thumb_text", ""))) else 3 if len(title) <= 70 else 0
    s["uzunlik_ishonch"] = d
    return {"ball": int(sum(s.values())), "qism": s, "muammo": q}
