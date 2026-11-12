"""TSB AI - O'ZI O'RGANISH (reinforcement learning, PPO). Odam o'ynab bermaydi: agent shaxsiy serverdagi
mashq qo'g'irchoqlarini (dummy) urib, sinab-xato bilan o'rganadi.
Mukofot ekrandan o'qiladi:  + ultimate chizig'i to'lsa (= zarba tegdi),  - o'z hayot chizig'i kamaysa.
F8 = boshlash / pauza, F10 = saqlab chiqish. Birinchi F8 da roi.json bo'lmasa kalibr.png saqlaydi (Claude chiziqlarni belgilaydi).
usage: ozi_organish.py [soat]   (standart 5.2 soat)"""
import os, sys, time, json, csv, collections
import numpy as np, torch, torch.nn as nn

WIN = os.name == "nt"
if WIN:
    import winsound
    from umumiy import Grabber, Edge, down, key, mouse_move, roblox_active, roblox_hwnd, client_box, VK_F8, VK_F10, W, H

HERE = os.path.dirname(os.path.abspath(__file__))
FPS, STACK = 10, 3
W, H = 160, 96
# har bir harakat = shu qadamda bosib turiladigan tugmalar (+ sichqoncha burilishi)
ACTIONS = [((), 0), (("W",), 0), (("W", "LMB"), 0), (("LMB",), 0), (("F",), 0), (("W", "Q"), 0), (("A", "Q"), 0),
           (("D", "Q"), 0), (("1",), 0), (("2",), 0), (("3",), 0), (("4",), 0), (("G",), 0), ((), -90), ((), 90),
           (("W", "SPACE"), 0), (("S",), 0), (("W",), -45), (("W",), 45)]
# YouTube/qo'llanmalardagi Saitama kombolari (1=Normal Punch, 2=Consecutive Punches, 3=Shove, 4=Uppercut):
# "3x M1 -> Shove -> Dash -> 3x M1", "3x M1 -> M1 Downslam -> Consecutive Punches", "3x M1 -> Normal Punch".
# Makro = [(tugmalar, soniya), ...]; agent butun makroni bitta harakat sifatida tanlaydi.
M1 = [(("LMB",), 0.08), ((), 0.22)]
MACROS = [
    M1 * 3 + [(("3",), 0.1), ((), 0.35), (("W", "Q"), 0.15), ((), 0.3)] + M1 * 3,           # 3M1 > shove > dash > 3M1
    M1 * 3 + [(("SPACE",), 0.12), (("LMB",), 0.08), ((), 0.3), (("2",), 0.1), ((), 1.2)],      # 3M1 > downslam > 2
    M1 * 3 + [(("1",), 0.1), ((), 0.6)],                                                    # 3M1 > normal punch
    M1 * 3 + [(("4",), 0.1), ((), 0.5), (("D", "Q"), 0.15), ((), 0.2)] + M1 * 3,           # 3M1 > uppercut > side dash > 3M1
    M1 * 4,                                                                                 # to'liq M1 seriyasi
]
ACTIONS += [("macro", i) for i in range(len(MACROS))]
GAMMA, LAM, CLIP, ENT, LR, ROLL, EPOCHS, MB = 0.97, 0.95, 0.2, 0.02, 2.5e-4, 512, 4, 128


class Net(nn.Module):
    def __init__(s, a):
        super().__init__()
        c = lambda i, o, k, st: [nn.Conv2d(i, o, k, st, k // 2), nn.ReLU(inplace=True)]
        s.f = nn.Sequential(*c(3 * STACK, 32, 5, 2), *c(32, 64, 3, 2), *c(64, 64, 3, 2), *c(64, 128, 3, 2),
                            nn.AdaptiveAvgPool2d((3, 5)), nn.Flatten(), nn.Linear(128 * 15, 256), nn.ReLU(inplace=True))
        s.pi, s.v = nn.Linear(256, a), nn.Linear(256, 1)
    def forward(s, x):
        z = s.f(x); return s.pi(z), s.v(z).squeeze(-1)


def bar_fill(img, roi):
    """roi = [x0,y0,x1,y1] mijoz oynasi ulushlarida. Chiziq chapdan o'ngga to'ladi: rangli (to'yingan, yorug') ustunlar ulushi."""
    h, w = img.shape[:2]; x0, y0, x1, y1 = int(roi[0] * w), int(roi[1] * h), int(roi[2] * w), int(roi[3] * h)
    p = img[y0:max(y1, y0 + 1), x0:max(x1, x0 + 1)].astype(np.float32) / 255
    if p.size == 0: return 0.0
    mx, mn = p.max(2), p.min(2); sat = (mx - mn) / (mx + 1e-4)
    col = ((sat > 0.35) & (mx > 0.35)).mean(0) > 0.5
    return float(col.mean())


def gae(r, v, last_v):
    adv = np.zeros_like(r); g = 0
    for t in range(len(r) - 1, -1, -1):
        nv = last_v if t == len(r) - 1 else v[t + 1]
        g = r[t] + GAMMA * nv - v[t] + GAMMA * LAM * g; adv[t] = g
    return adv, adv + v


def ppo_update(net, opt, obs, act, logp, adv, ret):
    obs = torch.from_numpy(obs).float() / 255; act = torch.from_numpy(act); logp = torch.from_numpy(logp)
    adv = torch.from_numpy((adv - adv.mean()) / (adv.std() + 1e-8)).float(); ret = torch.from_numpy(ret).float()
    n = len(act); stats = []
    for _ in range(EPOCHS):
        for i in np.array_split(np.random.permutation(n), max(1, n // MB)):
            lo, v = net(obs[i]); d = torch.distributions.Categorical(logits=lo); nl = d.log_prob(act[i])
            ratio = torch.exp(nl - logp[i]); a = adv[i]
            pl = -torch.min(ratio * a, ratio.clamp(1 - CLIP, 1 + CLIP) * a).mean()
            loss = pl + 0.5 * ((v - ret[i]) ** 2).mean() - ENT * d.entropy().mean()
            opt.zero_grad(); loss.backward(); nn.utils.clip_grad_norm_(net.parameters(), 0.5); opt.step()
            stats.append(d.entropy().mean().item())
    return float(np.mean(stats))


def main(hours=5.2):
    torch.set_num_threads(max(1, os.cpu_count() - 2))
    roi_f = os.path.join(HERE, "roi.json"); ck_f = os.path.join(HERE, "ozi_model.pt")
    net = Net(len(ACTIONS)); opt = torch.optim.Adam(net.parameters(), LR); steps = 0
    if os.path.exists(ck_f):
        ck = torch.load(ck_f); net.load_state_dict(ck["sd"]); opt.load_state_dict(ck["opt"]); steps = ck["steps"]
        print(f"davom: oldin {steps} qadam ({steps / FPS / 3600:.2f} soat) o'rganilgan")
    g, edge = Grabber(), Edge(); buf = collections.deque(maxlen=STACK)
    logw = csv.writer(open(os.path.join(HERE, "ozi_log.csv"), "a", newline=""))
    on, held, t_end = False, set(), time.time() + hours * 3600
    O, A, L, V, R = [], [], [], [], []; ult_h, hp_h = collections.deque(maxlen=3), collections.deque(maxlen=3)
    prev_ult = prev_hp = None; ep_r, hits = 0.0, 0

    def set_keys(want):
        nonlocal held
        for k in held - want: key(k, False)
        for k in want - held: key(k, True)
        held = set(want)

    def save():
        torch.save({"sd": net.state_dict(), "opt": opt.state_dict(), "steps": steps}, ck_f)

    print("Tayyor. TSB shaxsiy serverida dummy yoniga boring, F8 bosing. F10 = saqlab chiqish.")
    while time.time() < t_end:
        t0 = time.perf_counter()
        if down(VK_F10): break
        if edge(VK_F8):
            if not os.path.exists(roi_f):
                h = roblox_hwnd()
                if h:
                    import mss, cv2
                    l, t, r, b = client_box(h)
                    img = np.asarray(mss.mss().grab({"left": l, "top": t, "width": r - l, "height": b - t}))[:, :, :3]
                    cv2.imwrite(os.path.join(HERE, "kalibr.png"), img)
                winsound.Beep(800, 120); winsound.Beep(800, 120)
                print("kalibr.png saqlandi. Claude'ga ayting - u hayot va ultimate chiziqlarini belgilaydi."); continue
            on = not on; winsound.Beep(1500 if on else 400, 150); print("O'RGANYAPTI" if on else "pauza")
            if not on: set_keys(set())
        if not on or not roblox_active():
            if held: set_keys(set())
            time.sleep(0.1); continue
        roi = json.load(open(roi_f))
        # to'liq o'lchamdagi kadr: chiziqlar uchun; kichigi: tarmoq uchun
        h = roblox_hwnd(); l, t, r, b = client_box(h)
        full = g.cam.grab(region=(max(l, 0), max(t, 0), r, b)) if g.cam is not None else None
        small = g.grab()
        if full is not None:
            ult_h.append(bar_fill(full, roi["ult"])); hp_h.append(bar_fill(full, roi["hp"]))
        buf.append(small)
        if len(buf) < STACK: continue
        ult, hp = (float(np.median(ult_h)) if ult_h else 0.0), (float(np.median(hp_h)) if hp_h else 1.0)
        rew = -0.002
        if prev_ult is not None:
            du, dh = ult - prev_ult, prev_hp - hp
            if 0.004 < du < 0.3: rew += 10 * du; hits += 1          # zarba tegdi (katta sakrash = shovqin)
            if 0.004 < dh < 0.5: rew -= 5 * dh                     # zarba yedi
        prev_ult, prev_hp = ult, hp
        if R: R[-1] = rew                                           # mukofot oldingi harakatga tegishli
        obs = np.concatenate(list(buf), 2).transpose(2, 0, 1).copy()
        with torch.no_grad():
            lo, v = net(torch.from_numpy(obs)[None].float() / 255)
            d = torch.distributions.Categorical(logits=lo[0]); a = int(d.sample())
        O.append(obs); A.append(a); L.append(float(d.log_prob(torch.tensor(a)))); V.append(float(v[0])); R.append(0.0)
        if ACTIONS[a][0] == "macro":
            for ks, dur in MACROS[ACTIONS[a][1]]:
                set_keys(set(ks)); time.sleep(dur)
            set_keys(set())
        else:
            keys, turn = ACTIONS[a]; set_keys(set(keys)); mouse_move(turn, 0)
        steps += 1; ep_r += rew
        if len(O) >= ROLL + 1:
            set_keys(set())                                         # o'qish paytida qo'lini qo'yib turadi
            last_v = V[-1]; o, ac, lp, vv, rr = (np.array(x[:-1]) for x in (O, A, L, V, R))
            adv, ret = gae(rr.astype(np.float32), vv.astype(np.float32), last_v)
            ent = ppo_update(net, opt, o, ac.astype(np.int64), lp.astype(np.float32), adv, ret.astype(np.float32))
            logw.writerow([time.strftime("%H:%M:%S"), steps, round(steps / FPS / 60, 1), round(ep_r, 3), hits, round(ent, 3)])
            print(f"{steps / FPS / 60:.1f} daq: mukofot {ep_r:+.2f}, tekkan zarba {hits}, tasodifiylik {ent:.2f}", flush=True)
            O, A, L, V, R = O[-1:], A[-1:], L[-1:], V[-1:], R[-1:]; ep_r, hits = 0.0, 0; save()
        time.sleep(max(0, 1 / FPS - (time.perf_counter() - t0)))
    set_keys(set()); save(); print("saqlandi, chiqildi")


if __name__ == "__main__":
    main(float(sys.argv[1]) if len(sys.argv) > 1 else 5.2)
