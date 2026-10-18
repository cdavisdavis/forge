"""Stage 2a: GENERATE a pencil runway behind the gated sketch."""
import numpy as np, time
from pencil import Pencil
from camera import Cam
from compose import compose, radial_mask, poly_mask, W, H

t0 = time.time()
cam = Cam(vpx=930, yh=1118)            # horizon at her mid-thigh: a kneeling photographer at the end of the runway
p = Pencil(W, H, seed=11)
rng = np.random.default_rng(5)
Xr, hp, Zn, Zf = 0.8, 0.5, 0.42, 6.0   # runway half-width, platform height, near/far depth (metres)

# runway platform: top edges, base edges, side faces
for s in (-1, 1):
    p.stroke(cam.seg((s * Xr, 0, Zn), (s * Xr, 0, Zf)), dark=0.52, width=3.4, jitter=1.4, passes=2, overshoot=10)
    p.stroke(cam.seg((s * Xr, -hp, Zn), (s * Xr, -hp, Zf)), dark=0.34, width=2.4, jitter=1.4, passes=2, overshoot=10)
    face = np.r_[cam.seg((s * Xr, 0, Zn), (s * Xr, 0, Zf)), cam.seg((s * Xr, -hp, Zf), (s * Xr, -hp, Zn))]
    p.hatch(face, 78 if s < 0 else 102, 26, dark=0.11, width=1.6, fill_frac=0.5)
p.stroke(cam.seg((-Xr, 0, Zf), (Xr, 0, Zf)), dark=0.32, width=2.4)
for Z in (1.35, 1.9, 2.8, 4.2):        # panel seams
    p.stroke(cam.seg((-Xr, 0, Z), (Xr, 0, Z)), dark=0.14, width=1.8, passes=1, gap=0.12)

# stage + backdrop at the far end (mostly behind her)
Zb, Xb, Yb = 6.5, 3.2, 4.5
p.stroke(cam.seg((-Xb, 0, Zb), (Xb, 0, Zb)), dark=0.3, width=2.4)
for s in (-1, 1): p.stroke(cam.seg((s * Xb, 0, Zb), (s * Xb, Yb, Zb)), dark=0.3, width=2.4, overshoot=8)
p.stroke(cam.seg((-Xb, Yb, Zb), (Xb, Yb, Zb)), dark=0.3, width=2.4, overshoot=8)
for s in (-1, 1): p.stroke(cam.seg((s * 0.7, 0, Zb), (s * 0.7, 3.0, Zb)), dark=0.25, width=2.0)
p.stroke(cam.seg((-0.7, 3.0, Zb), (0.7, 3.0, Zb)), dark=0.25, width=2.0)
p.hatch(cam.poly([(-Xb, 0, Zb), (Xb, 0, Zb), (Xb, Yb, Zb), (-Xb, Yb, Zb)]), 62, 20, dark=0.08, width=1.5, fill_frac=0.6)

# audience: front row with bodies seated against the platform; back rows on risers, heads only
for s_ in (-1, 1):
    Z = 1.75 + rng.uniform(0, 0.25)
    while Z < 6.4:
        Xh = s_ * (Xr + 0.55) + rng.uniform(-0.05, 0.05); Yh = 0.62 + rng.uniform(-0.05, 0.08)
        cx, cy = cam.proj(Xh, Yh, Z); r = 800 * 0.105 / Z
        if -80 < cx < W + 80:
            p.loop(cx, cy, r * rng.uniform(0.9, 1.05), r * rng.uniform(1.05, 1.2), dark=0.22, width=1.8)
            shL = cam.proj(Xh - 0.28, Yh - 0.2, Z); shR = cam.proj(Xh + 0.28, Yh - 0.2, Z)
            p.stroke([shL, (cx, cy + r * 1.15), shR], dark=0.18, width=1.7, passes=1, overshoot=0, jitter=1.5)
            p.stroke([shL, cam.proj(Xh - 0.24, 0.0, Z)], dark=0.13, width=1.6, passes=1, overshoot=0)
            p.stroke([shR, cam.proj(Xh + 0.24, 0.0, Z)], dark=0.13, width=1.6, passes=1, overshoot=0)
        Z += 0.52 + rng.uniform(0, 0.12)
    for k in (1, 2, 3):
        Z = 1.9 + rng.uniform(0, 0.4)
        while Z < 6.4:
            Xh = s_ * (Xr + 0.55 + 0.7 * k) + rng.uniform(-0.1, 0.1); Yh = 0.62 + 0.13 * k + rng.uniform(-0.05, 0.05)
            cx, cy = cam.proj(Xh, Yh, Z); r = 800 * 0.105 / Z
            if -80 < cx < W + 80:
                p.loop(cx, cy, r * 0.95, r * 1.1, dark=0.15, width=1.6)
                sh = cam.seg((Xh - 0.26, Yh - 0.17, Z), (Xh + 0.26, Yh - 0.17, Z), n=6)
                sh[:, 1] += np.array([0, -4, -6, -6, -4, 0]) * (r / 40)
                p.stroke(sh, dark=0.11, width=1.5, passes=1, overshoot=0)
            Z += 0.6 + rng.uniform(0, 0.2)

# lighting truss overhead
Yt = 7.5
for s in (-1, 1): p.stroke(cam.seg((s * 1.8, Yt, 4.6), (s * 1.8, Yt, 6.6)), dark=0.26, width=2.2)
p.stroke(cam.seg((-1.8, Yt, 5.6), (1.8, Yt, 5.6)), dark=0.26, width=2.2, overshoot=10)
for X in (-1.35, -0.45, 0.45, 1.35):
    cx, cy = cam.proj(X, Yt - 0.3, 5.6); r = 800 * 0.12 / 5.6
    p.stroke([(cx, cy - 2.2 * r), (cx, cy - r)], dark=0.24, width=2.0, passes=1)
    p.loop(cx, cy, r, r * 0.9, dark=0.24)
    for dx in (-1, 0, 1):
        p.stroke([(cx + dx * 5, cy + 1.3 * r), (cx + dx * 70, cy + 1.3 * r + 220)], dark=0.05, width=4, passes=1, jitter=0.4)

# contact shadow under her feet
a = np.linspace(0, 2 * np.pi, 48); shadow = np.c_[875 + 215 * np.cos(a), 1748 + 46 * np.sin(a)]
p.hatch(shadow, 0, 9, dark=0.09, width=1.6, fill_frac=0.8)

D = p.darkness()
np.save('diag/D_runway.npy', D)
print('runway strokes done', round(time.time() - t0, 1), 's')
pool = radial_mask(870, 1850, 520)                                    # faint warm light pool on the runway
compose(None, 'out_01_gated_tinted.png')
compose(D, 'out_02_runway.png', extra_tints=[(pool, (1.0, 0.985, 0.955), 1.0)])
print('runway composed', round(time.time() - t0, 1), 's')
