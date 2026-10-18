"""Stage 2b: GENERATE a pencil Manhattan street behind the gated sketch."""
import numpy as np, time
from pencil import Pencil
from camera import Cam
from compose import compose, poly_mask, W, H

t0 = time.time()
cam = Cam(vpx=1250, yh=1118)       # vanishing point to her right so the canyon opens beside her
p = Pencil(W, H, seed=23)
rng = np.random.default_rng(3)
Xs, Xf = 5.5, 9.0                  # curb and facade distances from the avenue centre line (metres)

def facade(side, bounds, heights, fire_escape_at=None):
    X = side * Xf
    for (Za, Zb), h in zip(zip(bounds[:-1], bounds[1:]), heights):
        for Z in (Za, Zb): p.stroke(cam.seg((X, 0, Z), (X, h, Z)), dark=0.32, width=2.4, jitter=1.2, overshoot=8)
        p.stroke(cam.seg((X, h, Za), (X, h, Zb)), dark=0.32, width=2.4, overshoot=6)
        p.stroke(cam.seg((X, h - 0.9, Za), (X, h - 0.9, Zb)), dark=0.16, width=1.8, passes=1)
        p.stroke(cam.seg((X, 0, Za), (X, 0, Zb)), dark=0.26, width=2.0)
        if 800 / Za > 9:   # near enough for windows
            Y = 4.0
            while Y + 1.6 < h - 1.0:
                Z = Za + 0.5
                while Z + 1.2 < Zb - 0.3:
                    q = cam.poly([(X, Y, Z), (X, Y + 1.6, Z), (X, Y + 1.6, Z + 1.2), (X, Y, Z + 1.2), (X, Y, Z)])
                    if (q[:, 0] > -40).any() and (q[:, 0] < W + 40).any() and (q[:, 1] > -40).any() and (q[:, 1] < H + 40).any() and np.ptp(q[:, 1]) > 5:
                        p.stroke(q, dark=0.2, width=1.7, jitter=0.6, passes=1, overshoot=1.5)
                    Z += 2.2
                Y += 3.3
            q = cam.poly([(X, 0.6, Za + 0.4), (X, 3.0, Za + 0.4), (X, 3.0, Zb - 0.4), (X, 0.6, Zb - 0.4), (X, 0.6, Za + 0.4)])
            p.stroke(q, dark=0.2, width=1.7, passes=1)
            Z = Za + 2.2
            while Z < Zb - 0.6:
                p.stroke(cam.seg((X, 0.6, Z), (X, 3.0, Z)), dark=0.16, width=1.5, passes=1); Z += 1.8
        else:              # far: floor lines only
            Y = 4.0
            while Y < h - 1.0:
                p.stroke(cam.seg((X, Y, Za), (X, Y, Zb)), dark=0.13, width=1.5, passes=1, gap=0.15); Y += 6.6
        if fire_escape_at and (Za, Zb) == fire_escape_at:
            Xe = X - side * 0.9
            for Yl in (4.0, 7.3, 10.6, 13.9):
                p.stroke(cam.seg((Xe, Yl, Za + 0.3), (Xe, Yl, Zb - 0.3)), dark=0.22, width=1.8, passes=1)
                p.stroke(cam.seg((Xe, Yl + 1.0, Za + 0.3), (Xe, Yl + 1.0, Zb - 0.3)), dark=0.2, width=1.6, passes=1)
                for Z in np.linspace(Za + 0.3, Zb - 0.3, 6):
                    p.stroke(cam.seg((Xe, Yl, Z), (Xe, Yl + 1.0, Z)), dark=0.16, width=1.4, passes=1, overshoot=0)
                for Z in (Za + 0.3, Zb - 0.3):
                    p.stroke(cam.seg((Xe, Yl, Z), (X, Yl, Z)), dark=0.18, width=1.5, passes=1, overshoot=0)
                p.stroke(cam.seg((Xe, Yl, Za + 0.5), (Xe, Yl + 3.3, Zb - 0.5)), dark=0.2, width=1.6, passes=1)

left_b = [5.6, 8.0, 11.5, 16, 23, 33, 48, 70, 100, 140]
left_h = [18, 22, 19, 26, 24, 35, 60, 45, 90]
right_b = [10.2, 14, 19, 26, 36, 50, 70, 100, 140]
right_h = [21, 25, 19, 20, 33, 52, 75, 110]
facade(-1, left_b, left_h, fire_escape_at=(8.0, 11.5))
facade(+1, right_b, right_h)

# water tower on the right roof (building Z 26..36, h 20)
Xw, Zw, Yb = 10.6, 31.0, 20.0; rw = 800 * 1.5 / Zw
for dX in (-1.1, 0, 1.1): p.stroke(cam.seg((Xw + dX, Yb, Zw), (Xw + dX, Yb + 2.0, Zw)), dark=0.26, width=1.8, passes=1)
for dX in (-1.5, 1.5): p.stroke(cam.seg((Xw + dX, Yb + 2.0, Zw), (Xw + dX, Yb + 5.5, Zw)), dark=0.3, width=2.0, passes=1)
for Yy in (Yb + 2.0, Yb + 5.5):
    cx, cy = cam.proj(Xw, Yy, Zw); p.loop(cx, cy, rw, rw * 0.3, dark=0.28, width=1.8, turns=1.05)
cx, cy = cam.proj(Xw, Yb + 5.5, Zw); ax, ay = cam.proj(Xw, Yb + 7.4, Zw)
p.stroke([(cx - rw, cy), (ax, ay), (cx + rw, cy)], dark=0.3, width=2.0, passes=1)

# distant stepped spire at the end of the canyon
Zs, Xsp = 260.0, 4.0
hw = [48, 36, 26, 16, 8, 2.5]; hy = [0, 120, 190, 240, 280, 320]
for i in range(len(hw)):
    top = hy[i + 1] if i + 1 < len(hy) else 385
    for s in (-1, 1):
        p.stroke(cam.seg((Xsp + s * hw[i], hy[i], Zs), (Xsp + s * hw[i], top, Zs)), dark=0.26, width=2.0, passes=1, jitter=0.8)
        if i + 1 < len(hw): p.stroke(cam.seg((Xsp + s * hw[i], top, Zs), (Xsp + s * hw[i + 1], top, Zs)), dark=0.26, width=2.0, passes=1)
for s in (-0.5, 0.5):
    p.stroke(cam.seg((Xsp + s * 30, 20, Zs), (Xsp + s * 20, 180, Zs)), dark=0.1, width=1.5, passes=1, gap=0.2)
p.stroke(cam.seg((Xsp, 385, Zs), (Xsp, 420, Zs)), dark=0.26, width=1.8, passes=1)

# street: curbs, centre dashes, crosswalk bands
for s in (-1, 1): p.stroke(cam.seg((s * Xs, 0, 0.5), (s * Xs, 0, 200)), dark=0.34, width=2.6, jitter=1.4, passes=2)
for Z0 in np.arange(2.2, 70, 3.0): p.stroke(cam.seg((0, 0, Z0), (0, 0, Z0 + 1.5)), dark=0.2, width=2.2, passes=1, overshoot=0)
for k in range(-5, 6):                 # continental crosswalk: bars parallel to the avenue, spaced across it
    X0 = -0.83 + 1.25 * k; X1 = X0 + 0.55; Za, Zb = 0.6, 4.2
    bar = cam.poly([(X0, 0, Za), (X1, 0, Za), (X1, 0, Zb), (X0, 0, Zb)])
    if (bar[:, 0] < -100).all() or (bar[:, 0] > W + 100).all(): continue
    p.stroke(np.r_[bar, bar[:1]], dark=0.2, width=2.0, passes=1, gap=0.08)
    ang = np.degrees(np.arctan2(bar[3, 1] - bar[0, 1], bar[3, 0] - bar[0, 0]))
    p.hatch(bar, ang, 16, dark=0.09, width=1.8, fill_frac=0.5)
for Z in np.arange(6.5, 22, 1.6):     # sidewalk slabs, left
    p.stroke(cam.seg((-Xs, 0, Z), (-Xf, 0, Z)), dark=0.12, width=1.5, passes=1, overshoot=0)

# yellow cab, front view, right lane
Zc = 6.5
body = [(1.9, 0.35, Zc), (3.75, 0.35, Zc), (3.75, 1.45, Zc), (1.9, 1.45, Zc), (1.9, 0.35, Zc)]
p.stroke(cam.poly(body), dark=0.34, width=2.4, overshoot=3)
p.stroke(cam.seg((1.9, 1.0, Zc), (3.75, 1.0, Zc)), dark=0.26, width=2.0, passes=1)           # hood line
wind = [(1.95, 1.0, Zc + 0.1), (3.7, 1.0, Zc + 0.1), (3.6, 1.45, Zc + 0.8), (2.05, 1.45, Zc + 0.8), (1.95, 1.0, Zc + 0.1)]
p.stroke(cam.poly(wind), dark=0.28, width=2.0, passes=1)
for Xx in (2.05, 3.6): p.stroke(cam.seg((Xx, 1.5, Zc + 0.8), (Xx, 1.5, Zc + 4.3)), dark=0.26, width=2.0, passes=1)
p.stroke(cam.seg((2.05, 1.5, Zc + 4.3), (3.6, 1.5, Zc + 4.3)), dark=0.2, width=1.8, passes=1)
p.stroke(cam.poly([(2.5, 1.5, Zc + 1.1), (3.15, 1.5, Zc + 1.1), (3.15, 1.78, Zc + 1.1), (2.5, 1.78, Zc + 1.1), (2.5, 1.5, Zc + 1.1)]), dark=0.3, width=2.0, passes=1)  # roof sign
for Xx in (2.25, 3.4):
    cx, cy = cam.proj(Xx, 0.72, Zc); p.loop(cx, cy, 800 * 0.16 / Zc, 800 * 0.13 / Zc, dark=0.3, width=1.8)
p.stroke(cam.poly([(2.6, 0.5, Zc), (3.05, 0.5, Zc), (3.05, 0.82, Zc), (2.6, 0.82, Zc), (2.6, 0.5, Zc)]), dark=0.24, width=1.8, passes=1)
for Xx in (2.1, 3.55):
    cx, cy = cam.proj(Xx, 0.33, Zc); r = 800 * 0.34 / Zc
    a = np.linspace(np.pi, 2 * np.pi, 14); p.stroke(np.c_[cx + r * np.cos(a), cy + 0.55 * r * np.sin(a)], dark=0.3, width=2.2, passes=1, overshoot=0)
cab_mask = poly_mask(np.r_[cam.poly(body[:4]), cam.poly(wind[1:4][::-1])], feather=4)

# street lamp (right) and signal pole with one-way sign (left)
p.stroke(cam.seg((6.5, 0, 9), (6.5, 8, 9)), dark=0.34, width=2.6, passes=2)
arm = np.r_[cam.seg((6.5, 8.0, 9), (5.6, 8.25, 9), n=5), cam.seg((5.6, 8.25, 9), (4.6, 7.75, 9), n=5)]
p.stroke(arm, dark=0.3, width=2.2, passes=1)
cx, cy = cam.proj(4.5, 7.6, 9); p.loop(cx, cy, 800 * 0.3 / 9, 800 * 0.2 / 9, dark=0.3, width=2.0)
Zp = 4.5
p.stroke(cam.seg((-6.2, 0, Zp), (-6.2, 3.9, Zp)), dark=0.34, width=2.6, passes=2)
sig = [(-6.45, 2.4, Zp), (-5.95, 2.4, Zp), (-5.95, 3.0, Zp), (-6.45, 3.0, Zp), (-6.45, 2.4, Zp)]
p.stroke(cam.poly(sig), dark=0.32, width=2.2)
cx, cy = cam.proj(-6.2, 2.7, Zp); p.loop(cx, cy, 800 * 0.1 / Zp, 800 * 0.13 / Zp, dark=0.22, width=1.8, turns=2.2)
sign = [(-6.65, 3.3, Zp), (-5.75, 3.3, Zp), (-5.75, 3.6, Zp), (-6.65, 3.6, Zp), (-6.65, 3.3, Zp)]
p.stroke(cam.poly(sign), dark=0.32, width=2.2)
p.stroke(cam.seg((-6.55, 3.45, Zp), (-5.85, 3.45, Zp)), dark=0.3, width=2.4, passes=1, overshoot=0)
p.stroke(np.r_[cam.seg((-6.05, 3.57, Zp), (-5.85, 3.45, Zp), n=4), cam.seg((-5.85, 3.45, Zp), (-6.05, 3.33, Zp), n=4)], dark=0.3, width=2.2, passes=1, overshoot=0)

# steam from a manhole, mid-distance right
for k in range(4):
    x0, y0 = cam.proj(1.6 + 0.15 * k, 0, 4.2); x1, y1 = cam.proj(1.4 + 0.25 * k, 2.2 + 0.4 * k, 4.2)
    p.stroke([(x0, y0), (x1, y1)], dark=0.07, width=4, passes=1, jitter=7, wobble=40, overshoot=0)

# contact shadow
a = np.linspace(0, 2 * np.pi, 48); shadow = np.c_[875 + 215 * np.cos(a), 1748 + 46 * np.sin(a)]
p.hatch(shadow, 0, 9, dark=0.09, width=1.6, fill_frac=0.8)

D = p.darkness()
np.save('diag/D_manhattan.npy', D)
print('manhattan strokes done', round(time.time() - t0, 1), 's')
compose(D, 'out_03_manhattan.png', extra_tints=[(cab_mask, (1.0, 0.93, 0.70), 0.5)])
print('manhattan composed', round(time.time() - t0, 1), 's')
