"""TSB AI - 3-qadam: agent O'ZI o'ynaydi. Faqat SHAXSIY serverda ishlating.
F8 = agentni yoqish / to'xtatish (boshida o'chiq), F10 = chiqish. Roblox oynasi oldinda bo'lmasa hech narsa bosmaydi."""
import os, time, collections, winsound
import numpy as np, torch
from umumiy import *
from orgatish import Net

HERE = os.path.dirname(os.path.abspath(__file__))
GAIN = float(os.environ.get("TSB_MOUSE_GAIN", "1.0"))


def main():
    ck = torch.load(os.path.join(HERE, "model.pt"), map_location="cpu")
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    net = Net(len(ck["keys"])); net.load_state_dict(ck["sd"]); net.to(dev).eval()
    thr = np.array(ck["thr"]); MS = ck["MS"]; names = ck["keys"]
    g, edge = Grabber(), Edge(); buf = collections.deque(maxlen=STACK)
    held = np.zeros(len(names), bool); on = False; steps = 0
    log = open(os.path.join(HERE, "oynash_log.txt"), "a")

    def release():
        for j, nm in enumerate(names):
            if held[j]: key(nm, False); held[j] = False

    print("Tayyor. Roblox'ni oldinga chiqarib F8 bosing - agent o'ynaydi. F10 = chiqish.")
    while True:
        t0 = time.perf_counter()
        if down(VK_F10): break
        if edge(VK_F8):
            on = not on; winsound.Beep(1500 if on else 400, 150); print("AGENT YONIQ" if on else "agent to'xtadi")
            if not on: release()
        if not roblox_active():
            if held.any(): release()
            time.sleep(0.1); continue
        buf.append(g.grab())
        if on and len(buf) == STACK:
            x = torch.from_numpy(np.concatenate(list(buf), 2)).to(dev).permute(2, 0, 1)[None].float() / 255
            with torch.no_grad(): o = net(x)[0].float().cpu().numpy()
            p = 1 / (1 + np.exp(-o[:-2]))
            want = np.where(held, p > thr * 0.6, p > thr)          # gisterezis: titramasin
            for j, nm in enumerate(names):
                if want[j] != held[j]: key(nm, bool(want[j])); held[j] = want[j]
            mx, my = np.tanh(o[-2:]) * MS * GAIN; mouse_move(round(mx), round(my)); steps += 1
            if steps % (FPS * 10) == 0:
                log.write(time.strftime("%H:%M:%S ") + " ".join(n for n, h in zip(names, held) if h) + "\n"); log.flush()
        time.sleep(max(0, 1 / FPS - (time.perf_counter() - t0)))
    release(); print("chiqildi")


if __name__ == "__main__":
    main()
