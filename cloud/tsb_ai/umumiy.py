"""TSB AI - umumiy qismlar (Windows). The Strongest Battlegrounds, faqat SHAXSIY serverda ishlatiladi."""
import ctypes, time
from ctypes import wintypes
import numpy as np

W, H, FPS, STACK = 160, 96, 15, 3
# (nomi, virtual-key) - model shu tugmalarni o'rganadi
KEYS = [("W", 0x57), ("A", 0x41), ("S", 0x53), ("D", 0x44), ("SPACE", 0x20), ("Q", 0x51), ("F", 0x46),
        ("1", 0x31), ("2", 0x32), ("3", 0x33), ("4", 0x34), ("G", 0x47), ("E", 0x45), ("R", 0x52),
        ("LMB", 0x01), ("RMB", 0x02)]
SCAN = {"W": 0x11, "A": 0x1E, "S": 0x1F, "D": 0x20, "SPACE": 0x39, "Q": 0x10, "F": 0x21, "1": 0x02, "2": 0x03,
        "3": 0x04, "4": 0x05, "G": 0x22, "E": 0x12, "R": 0x13}
VK_F8, VK_F10 = 0x77, 0x79

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    try: ctypes.windll.user32.SetProcessDPIAware()
    except Exception: pass
user32 = ctypes.windll.user32


def down(vk):
    return bool(user32.GetAsyncKeyState(vk) & 0x8000)


class Edge:
    def __init__(s): s.prev = {}
    def __call__(s, vk):
        d = down(vk); r = d and not s.prev.get(vk, False); s.prev[vk] = d; return r


def roblox_hwnd():
    h = user32.FindWindowW(None, "Roblox")
    return h or None


def roblox_active():
    h = roblox_hwnd()
    return h is not None and user32.GetForegroundWindow() == h


def client_box(h):
    r = wintypes.RECT(); user32.GetClientRect(h, ctypes.byref(r))
    p = wintypes.POINT(0, 0); user32.ClientToScreen(h, ctypes.byref(p))
    return (p.x, p.y, p.x + r.right, p.y + r.bottom)


class Grabber:
    """Roblox oynasini oladi va 160x96 ga kichraytiradi. dxcam (tez), bo'lmasa mss."""
    def __init__(s):
        import cv2; s.cv2 = cv2; s.last = np.zeros((H, W, 3), np.uint8)
        try:
            import dxcam; s.cam = dxcam.create(output_color="RGB"); s.mss = None
        except Exception:
            import mss; s.cam = None; s.mss = mss.mss()
    def grab(s):
        h = roblox_hwnd()
        if not h: return s.last
        l, t, r, b = client_box(h)
        if r - l < 50 or b - t < 50: return s.last
        if s.cam is not None:
            img = s.cam.grab(region=(max(l, 0), max(t, 0), r, b))
            if img is None: return s.last
        else:
            img = np.asarray(s.mss.grab({"left": l, "top": t, "width": r - l, "height": b - t}))[:, :, 2::-1]
        s.last = s.cv2.resize(img, (W, H), interpolation=s.cv2.INTER_AREA)
        return s.last


# ---------- SendInput (o'ynash uchun) ----------
PUL = ctypes.POINTER(ctypes.c_ulong)
class KI(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort), ("wScan", ctypes.c_ushort), ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong), ("dwExtraInfo", PUL)]
class MI(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long), ("dy", ctypes.c_long), ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong), ("time", ctypes.c_ulong), ("dwExtraInfo", PUL)]
class HI(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong), ("wParamL", ctypes.c_short), ("wParamH", ctypes.c_ushort)]
class _U(ctypes.Union):
    _fields_ = [("ki", KI), ("mi", MI), ("hi", HI)]
class INPUT(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong), ("u", _U)]


def _send(inp):
    user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(inp))


def key(name, press):
    if name in ("LMB", "RMB"):
        f = {("LMB", 1): 0x2, ("LMB", 0): 0x4, ("RMB", 1): 0x8, ("RMB", 0): 0x10}[(name, int(press))]
        i = INPUT(type=0); i.u.mi = MI(0, 0, 0, f, 0, None); _send(i); return
    i = INPUT(type=1); i.u.ki = KI(0, SCAN[name], 0x8 | (0 if press else 0x2), 0, None); _send(i)


def mouse_move(dx, dy):
    if dx or dy:
        i = INPUT(type=0); i.u.mi = MI(int(dx), int(dy), 0, 0x1, 0, None); _send(i)
