"""TSB AI - 2-qadam: yozilgan o'yinlardan neyron tarmoqni o'qitadi (sizning o'ynashingizni takrorlashni o'rganadi).
usage: orgatish.py [epochs]   ->  model.pt + orgatish_hisobot.txt"""
import os, sys, glob, time
import numpy as np, torch, torch.nn as nn
from umumiy import W, H, STACK, KEYS

HERE = os.path.dirname(os.path.abspath(__file__))
dev = "cuda" if torch.cuda.is_available() else "cpu"


class Net(nn.Module):
    def __init__(s, k):
        super().__init__()
        c = lambda i, o, ks, st: [nn.Conv2d(i, o, ks, st, ks // 2), nn.BatchNorm2d(o), nn.ReLU(inplace=True)]
        s.f = nn.Sequential(*c(3 * STACK, 32, 5, 2), *c(32, 64, 3, 2), *c(64, 64, 3, 1), *c(64, 128, 3, 2),
                            *c(128, 128, 3, 2), nn.Flatten())                      # 96x160 -> 6x10
        s.h = nn.Sequential(nn.Linear(128 * 6 * 10, 512), nn.ReLU(inplace=True), nn.Dropout(0.3), nn.Linear(512, k + 2))
    def forward(s, x):
        return s.h(s.f(x))


def main(epochs=15):
    files = sorted(glob.glob(os.path.join(HERE, "data", "*.npz")))
    if not files: print("data/ bo'sh - avval 2_YOZISH bilan o'ynab yozing"); return 1
    Fs, Ks, Ms = [], [], []
    for fn in files:
        z = np.load(fn); Fs.append(z["f"]); Ks.append(z["k"]); Ms.append(z["m"])
    n = sum(len(f) for f in Fs); print(f"{len(files)} bo'lak, {n} kadr ({n / 15 / 60:.1f} daqiqa)")
    allm = np.concatenate(Ms); MS = float(np.percentile(np.abs(allm), 97) + 1e-3)
    idx = [(c, i) for c, f in enumerate(Fs) for i in range(STACK - 1, len(f))]
    rng = np.random.default_rng(0)
    nval = max(1, len(Fs) // 10); val_c = set(range(len(Fs) - nval, len(Fs))) if len(Fs) > 3 else set()
    tr = [p for p in idx if p[0] not in val_c]; va = [p for p in idx if p[0] in val_c] or tr[-2000:]
    allk = np.concatenate(Ks).astype(np.float32); pos = allk.mean(0)
    pw = torch.tensor(np.clip((1 - pos) / (pos + 1e-4), 1, 25), dtype=torch.float32, device=dev)
    print("tugmalar ulushi:", {k[0]: round(float(p), 3) for k, p in zip(KEYS, pos)})

    def batch(ps, aug):
        x = np.stack([np.concatenate([Fs[c][i - j] for j in range(STACK - 1, -1, -1)], 2) for c, i in ps])
        x = torch.from_numpy(x).to(dev).permute(0, 3, 1, 2).float() / 255
        if aug:
            b = x.shape[0]
            x = x * (0.8 + 0.4 * torch.rand(b, 1, 1, 1, device=dev)) + 0.1 * (torch.rand(b, 1, 1, 1, device=dev) - 0.5)
            sx, sy = np.random.randint(-6, 7), np.random.randint(-4, 5); x = torch.roll(x, (sy, sx), (2, 3))
        k = torch.tensor(np.stack([Ks[c][i] for c, i in ps]), dtype=torch.float32, device=dev)
        m = torch.tensor(np.clip(np.stack([Ms[c][i] for c, i in ps]) / MS, -1, 1), dtype=torch.float32, device=dev)
        return x.clamp(0, 1), k, m

    net = Net(len(KEYS)).to(dev)
    opt = torch.optim.AdamW(net.parameters(), 3e-4, weight_decay=1e-4)
    bce = nn.BCEWithLogitsLoss(pos_weight=pw); hub = nn.SmoothL1Loss()
    scaler = torch.amp.GradScaler(enabled=dev == "cuda"); B = 128
    for ep in range(epochs):
        net.train(); rng.shuffle(tr); tl, t0 = 0, time.time()
        for s in range(0, len(tr) - B + 1, B):
            x, k, m = batch(tr[s:s + B], True)
            with torch.autocast(dev, enabled=dev == "cuda"):
                o = net(x); loss = bce(o[:, :-2], k) + 2 * hub(torch.tanh(o[:, -2:]), m)
            opt.zero_grad(); scaler.scale(loss).backward(); scaler.step(opt); scaler.update(); tl += loss.item()
        print(f"davr {ep + 1}/{epochs}: xato {tl / max(1, len(tr) // B):.4f}  ({time.time() - t0:.0f} s)", flush=True)
    # val: har tugma uchun eng yaxshi chegara (F1)
    net.eval(); P, T = [], []
    with torch.no_grad():
        for s in range(0, len(va), 256):
            x, k, _ = batch(va[s:s + 256], False); P.append(torch.sigmoid(net(x)[:, :-2]).float().cpu().numpy()); T.append(k.cpu().numpy())
    P, T = np.concatenate(P), np.concatenate(T); thr, rep = [], []
    for j, (nm, _) in enumerate(KEYS):
        best = (0, 0.5)
        for th in np.arange(0.1, 0.95, 0.05):
            pr = P[:, j] > th; tp = (pr & (T[:, j] > 0)).sum()
            f1 = 2 * tp / max(1, pr.sum() + (T[:, j] > 0).sum()); best = max(best, (f1, th))
        thr.append(float(best[1])); rep.append(f"{nm:6s} F1={best[0]:.2f} chegara={best[1]:.2f}")
    torch.save({"sd": net.state_dict(), "thr": thr, "MS": MS, "keys": [k for k, _ in KEYS]}, os.path.join(HERE, "model.pt"))
    open(os.path.join(HERE, "orgatish_hisobot.txt"), "w").write(f"{n} kadr, {epochs} davr\n" + "\n".join(rep) + "\n")
    print("\n".join(rep)); print("model.pt saqlandi")


if __name__ == "__main__":
    sys.exit(main(int(sys.argv[1]) if len(sys.argv) > 1 else 15))
