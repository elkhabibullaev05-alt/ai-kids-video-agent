"""TSB AI - 1-qadam: SIZ o'ynaysiz, bu dastur ekran + tugmalar + sichqonchani yozadi (agent shundan o'rganadi).
F8 = yozishni boshlash / pauza (ovozli signal), F10 = tugatish. Faqat Roblox oynasi oldinda bo'lganda yozadi."""
import os, time, threading, winsound
import numpy as np
from umumiy import *

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "data"); os.makedirs(OUT, exist_ok=True)
lock = threading.Lock(); acc = [0.0, 0.0]


def on_move(x, y):           # past darajali hook: hodisa nuqtasi - hozirgi kursor = haqiqiy siljish
    p = wintypes.POINT(); user32.GetCursorPos(ctypes.byref(p))
    with lock: acc[0] += x - p.x; acc[1] += y - p.y


def main():
    from pynput import mouse
    mouse.Listener(on_move=on_move).start()
    g, edge = Grabber(), Edge()
    stamp = time.strftime("%Y%m%d_%H%M%S"); part = 0
    F, K, M = [], [], []
    active, total = False, 0

    def save():
        nonlocal part, F, K, M
        if len(F) > FPS * 5:
            fn = os.path.join(OUT, f"s_{stamp}_{part:03d}.npz")
            np.savez_compressed(fn, f=np.stack(F), k=np.array(K, np.uint8), m=np.array(M, np.float32))
            print("saqlandi:", os.path.basename(fn), len(F), "kadr"); part += 1
        F, K, M = [], [], []

    print("Tayyor. Roblox'da TSB shaxsiy serverga kiring, F8 bosing va o'ynang. F10 = tugatish.")
    while True:
        t0 = time.perf_counter()
        if down(VK_F10): break
        if edge(VK_F8):
            active = not active
            winsound.Beep(1200 if active else 500, 150)
            print("YOZILYAPTI" if active else "pauza"); save() if not active else None
        if active and roblox_active():
            fr = g.grab()
            with lock: m = (acc[0], acc[1]); acc[0] = acc[1] = 0.0
            F.append(fr); K.append([down(vk) for _, vk in KEYS]); M.append(m); total += 1
            if len(F) >= FPS * 60: save()
            if total % (FPS * 60) == 0: print(f"jami {total / FPS / 60:.0f} daqiqa yozildi")
        else:
            with lock: acc[0] = acc[1] = 0.0
        time.sleep(max(0, 1 / FPS - (time.perf_counter() - t0)))
    save(); winsound.Beep(400, 300)
    print(f"tugadi. Bu safar {total / FPS / 60:.1f} daqiqa.")


if __name__ == "__main__":
    main()
