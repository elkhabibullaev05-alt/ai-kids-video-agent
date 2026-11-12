import traceback, time
try:
    from umumiy import *
    import cv2, torch
    g = Grabber(); print("grabber:", "dxcam" if g.cam is not None else "mss")
    import dxcam
    cam = dxcam.create(output_color="RGB"); img = None
    for _ in range(20):
        img = cam.grab(); 
        if img is not None: break
        time.sleep(0.05)
    print("ekran:", None if img is None else img.shape)
    if img is not None: cv2.imwrite("sinov_ekran.jpg", cv2.resize(img[:, :, ::-1], (640, 360)))
    print("roblox oynasi:", roblox_hwnd())
    from orgatish import Net
    n = Net(len(KEYS)); x = torch.zeros(1, 3 * STACK, H, W); t = time.time(); [n(x) for _ in range(10)]
    print("model CPU tezligi: %.1f ms/kadr" % ((time.time() - t) * 100))
    print("SINOV OK")
except Exception:
    traceback.print_exc()
