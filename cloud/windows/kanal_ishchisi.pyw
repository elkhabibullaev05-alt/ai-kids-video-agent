# Kanal ishchisi — kompyuterdagi 3D video ishchisining holati (ish stoli ilovasi).
# Ikki marta bosing. Hech narsani o'zgartirmaydi: faqat ko'rsatadi va "Hozir ishga tushir" tugmasi bor.
import json, subprocess, threading, datetime as dt, tkinter as tk
from tkinter import ttk

DISTRO = "Ubuntu-24.04"
NO_WIN = 0x08000000  # CREATE_NO_WINDOW
CH = [("maxcat", "Max the Curious Cat"), ("doughbros", "Dough Bros"), ("hollow", "Hollowmere Tales"), ("bolt", "Inspector Bolt")]
STAGE = {"sync": "YouTube tekshirilmoqda", "voices": "ovoz yozilmoqda", "render": "3D render", "assemble": "montaj",
         "check": "rek-ball tekshiruvi", "upload": "yuklanmoqda", "ok": "tayyor", "idle": "2 kunlik video bor — dam olmoqda",
         "queue_empty": "hikoya kutmoqda", "quota_wait": "YouTube limiti — keyinroq", "error": "XATO", "rejected": "rad etildi"}

PY = r'''
import json, os, glob, time
out = {}
for ch in ["maxcat","doughbros","hollow","bolt"]:
    d = {}
    try: d["status"] = json.load(open(f"/opt/kanal/repo/cloud/results/{ch}/status.json"))
    except Exception: d["status"] = None
    try:
        st = json.load(open(f"/root/kanal/{ch}/state.json"))
        now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        d["next"] = sorted(x["t"] for x in st.get("taken", []) if x["t"] > now)[:4]
        d["pending"] = len(st.get("pending", []))
    except Exception: d["next"], d["pending"] = [], 0
    try: d["log"] = open(f"/root/kanal/{ch}/worker.log").read().splitlines()[-4:]
    except Exception: d["log"] = []
    d["queue"] = len(glob.glob(f"/opt/kanal/repo/cloud/queue/{ch}/*.json"))
    d["done"] = len(glob.glob(f"/opt/kanal/repo/cloud/done/{ch}/*.json"))
    d["token"] = os.path.exists(f"/root/kanal/{ch}/token.json")
    out[ch] = d
print(json.dumps(out))
'''


def gather():
    p = subprocess.run(["wsl.exe", "-d", DISTRO, "-u", "root", "--", "python3", "-"], input=PY, capture_output=True,
                       text=True, encoding="utf-8", errors="replace", timeout=60, creationflags=NO_WIN)
    return json.loads(p.stdout.strip().splitlines()[-1])


def local(iso):
    try:
        t = dt.datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone()
        return t.strftime("%d.%m %H:%M")
    except Exception:
        return iso


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Kanal ishchisi")
        self.geometry("880x620")
        self.configure(bg="#14161c")
        st = ttk.Style(self); st.theme_use("clam")
        st.configure("TFrame", background="#14161c")
        st.configure("TLabel", background="#14161c", foreground="#e8e8ee", font=("Segoe UI", 10))
        st.configure("H.TLabel", font=("Segoe UI", 13, "bold"))
        st.configure("TButton", font=("Segoe UI", 10))
        top = ttk.Frame(self); top.pack(fill="x", padx=14, pady=10)
        ttk.Label(top, text="Kanal ishchisi — kompyuterdagi 3D videolar", style="H.TLabel").pack(side="left")
        ttk.Button(top, text="Hozir ishga tushir", command=self.run_now).pack(side="right", padx=4)
        ttk.Button(top, text="Yangilash", command=self.refresh).pack(side="right", padx=4)
        self.info = ttk.Label(self, text="Yuklanmoqda…"); self.info.pack(anchor="w", padx=14)
        self.cards = {}
        for key, name in CH:
            f = tk.Frame(self, bg="#1d2029", highlightthickness=1, highlightbackground="#2c3040")
            f.pack(fill="x", padx=14, pady=6)
            head = tk.Label(f, text=name, bg="#1d2029", fg="#ffffff", font=("Segoe UI", 11, "bold"), anchor="w")
            head.pack(fill="x", padx=10, pady=(8, 0))
            body = tk.Label(f, text="", bg="#1d2029", fg="#c9cbd6", font=("Consolas", 9), justify="left", anchor="w")
            body.pack(fill="x", padx=10, pady=(2, 8))
            self.cards[key] = (head, body)
        self.tick()

    def run_now(self):
        subprocess.Popen(["schtasks", "/run", "/tn", "KanalWorker"], creationflags=NO_WIN)
        self.info.config(text="Ishga tushirildi. 1–2 daqiqadan keyin Yangilash'ni bosing.")

    def refresh(self):
        self.info.config(text="Yangilanmoqda…")
        threading.Thread(target=self._load, daemon=True).start()

    def _load(self):
        try:
            data, err = gather(), None
        except Exception as e:
            data, err = None, str(e)
        self.after(0, lambda: self._show(data, err))

    def _show(self, data, err):
        if err:
            self.info.config(text=f"Ubuntu (WSL) javob bermadi: {err[:120]}")
        else:
            self.info.config(text="Oxirgi yangilanish: " + dt.datetime.now().strftime("%H:%M:%S") + "   (har 60 soniyada o'zi yangilanadi)")
            for key, name in CH:
                d = data.get(key, {})
                s = d.get("status") or {}
                stage = s.get("stage", "")
                color = "#ff6b6b" if stage in ("error", "rejected") else "#7ee787" if stage in ("ok", "idle", "upload") else "#f2cc60"
                head, body = self.cards[key]
                txt = STAGE.get(stage, stage or "hali ishlamagan")
                head.config(text=f"{name}   —   {txt}", fg=color)
                lines = [
                    f"Navbatdagi hikoyalar: {d.get('queue', 0)}   Tayyor: {d.get('done', 0)}   Yuklashni kutayotgan: {d.get('pending', 0)}"
                    + ("" if d.get("token") else "   ⚠ YouTube tokeni yo'q"),
                    "Keyingi chiqishlar: " + (", ".join(local(t) for t in d.get("next", [])) or "—"),
                ]
                if s.get("error") or s.get("reason"):
                    lines.append("Xato: " + str(s.get("error") or s.get("reason"))[:150])
                for l in d.get("log", [])[-2:]:
                    lines.append("› " + l[:120])
                body.config(text="\n".join(lines))

    def tick(self):
        self.refresh()
        self.after(60000, self.tick)


App().mainloop()
