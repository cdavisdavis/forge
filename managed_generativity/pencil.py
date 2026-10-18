"""A tiny procedural pencil: jittered multi-pass strokes, scribbled loops, hatching, graphite tooth texture."""
import math
import numpy as np
from PIL import Image, ImageDraw
from mg import blur

class Pencil:
    def __init__(self, W, H, seed=7):
        self.W, self.H = W, H
        self.canvas = np.zeros((H, W), np.float32)      # accumulated darkness 0..1
        self.rng = np.random.default_rng(seed)

    # ---- geometry helpers
    def _resample(self, pts, step=7.0):
        pts = np.asarray(pts, np.float32)
        if len(pts) < 2: return pts
        seg = np.diff(pts, axis=0); L = np.hypot(seg[:, 0], seg[:, 1]); cum = np.r_[0, np.cumsum(L)]
        if cum[-1] < 1e-3: return pts
        n = max(2, int(cum[-1] / step) + 1); t = np.linspace(0, cum[-1], n)
        return np.c_[np.interp(t, cum, pts[:, 0]), np.interp(t, cum, pts[:, 1])]

    def _jitter(self, pts, amp, overshoot=0.0, wobble=18.0):
        p = self._resample(pts)
        inb = (p[:, 0] > -60) & (p[:, 0] < self.W + 60) & (p[:, 1] > -60) & (p[:, 1] < self.H + 60)
        if inb.any():
            i0, i1 = np.argmax(inb), len(inb) - np.argmax(inb[::-1]); p = p[max(0, i0 - 1):i1 + 1]
        else:
            return p[:0]
        n = len(p)
        if n < 2: return p
        d = np.gradient(p, axis=0); nrm = np.hypot(d[:, 0], d[:, 1]) + 1e-6
        perp = np.c_[-d[:, 1] / nrm, d[:, 0] / nrm]
        # smooth random offset (low-frequency wobble + a little high-frequency tremor)
        k = max(1, int(wobble / 7))
        noise = np.convolve(self.rng.normal(size=n + 2 * k), np.ones(2 * k + 1) / (2 * k + 1), mode='valid')
        noise = noise / (noise.std() + 1e-6) * amp + self.rng.normal(size=n) * amp * 0.15
        q = p + perp * noise[:, None]
        if overshoot > 0:   # hand-drawn overshoot at the ends
            a = self.rng.uniform(0, overshoot); b = self.rng.uniform(0, overshoot)
            d0 = q[1] - q[0]; d0 /= np.hypot(*d0) + 1e-6; q[0] -= d0 * a
            d1 = q[-1] - q[-2]; d1 /= np.hypot(*d1) + 1e-6; q[-1] += d1 * b
        return q

    # ---- marks
    def stroke(self, pts, dark=0.35, width=2.2, jitter=1.2, passes=2, overshoot=4.0, gap=0.0, wobble=18.0):
        """draw a polyline as `passes` slightly different graphite lines. gap: probability of dropping a segment."""
        if pts is None: return
        pts = np.asarray(pts, np.float32)
        if len(pts) < 2: return
        for i in range(passes):
            q = self._jitter(pts, jitter * (1 if i == 0 else 1.6), overshoot, wobble)
            if len(q) < 2: continue
            if gap > 0 and len(q) > 4:
                keep = self.rng.random(len(q) - 1) > gap
                runs = []; cur = [q[0]]
                for j in range(1, len(q)):
                    if keep[j - 1]: cur.append(q[j])
                    else:
                        if len(cur) > 1: runs.append(cur)
                        cur = [q[j]]
                if len(cur) > 1: runs.append(cur)
            else:
                runs = [q]
            w = width * (1.0 if i == 0 else 0.7)
            dk = dark * (1.0 if i == 0 else 0.55) * self.rng.uniform(0.8, 1.0)
            for r in runs: self._raster(np.asarray(r), w, dk)

    def loop(self, cx, cy, rx, ry, dark=0.3, width=1.8, turns=1.35, jitter=None, phase=None):
        """a scribbled ellipse (audience head, lamp, wheel)."""
        phase = self.rng.uniform(0, 2 * math.pi) if phase is None else phase
        t = np.linspace(0, 2 * math.pi * turns, max(12, int(2 * math.pi * turns * max(rx, ry) / 6)))
        pts = np.c_[cx + rx * np.cos(t + phase), cy + ry * np.sin(t + phase)]
        self.stroke(pts, dark, width, jitter=(jitter if jitter is not None else max(0.6, rx * 0.08)), passes=1, overshoot=0, wobble=12)

    def hatch(self, poly, angle_deg, spacing, dark=0.18, width=1.6, jitter=1.0, gap=0.08, fill_frac=1.0):
        """parallel pencil hatching clipped to a polygon."""
        poly = np.asarray(poly, np.float32)
        x0, y0 = np.floor(poly.min(0)).astype(int); x1, y1 = np.ceil(poly.max(0)).astype(int)
        x0, y0 = max(x0, 0), max(y0, 0); x1, y1 = min(x1, self.W - 1), min(y1, self.H - 1)
        if x1 <= x0 or y1 <= y0: return
        mask = Image.new('L', (x1 - x0 + 1, y1 - y0 + 1), 0)
        ImageDraw.Draw(mask).polygon([(float(px - x0), float(py - y0)) for px, py in poly], fill=255)
        m = np.asarray(mask) > 0
        a = math.radians(angle_deg); ux, uy = math.cos(a), math.sin(a); vx, vy = -uy, ux
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; R = math.hypot(x1 - x0, y1 - y0) / 2 + spacing
        n = int(2 * R / spacing) + 1
        for k in range(n):
            if self.rng.random() > fill_frac: continue
            off = -R + k * spacing + self.rng.uniform(-0.2, 0.2) * spacing
            ts = np.arange(-R, R, 3.0)
            xs = cx + vx * off + ux * ts; ys = cy + vy * off + uy * ts
            ix = np.round(xs - x0).astype(int); iy = np.round(ys - y0).astype(int)
            ok = (ix >= 0) & (ix < m.shape[1]) & (iy >= 0) & (iy < m.shape[0])
            inside = np.zeros(len(ts), bool); inside[ok] = m[iy[ok], ix[ok]]
            # runs of inside
            idx = np.nonzero(np.diff(np.r_[False, inside, False].astype(int)))[0].reshape(-1, 2)
            for s, e in idx:
                if e - s < 3: continue
                self.stroke(np.c_[xs[s:e], ys[s:e]], dark * self.rng.uniform(0.7, 1.0), width, jitter, passes=1, overshoot=2, gap=gap, wobble=10)

    def _raster(self, pts, width, dark):
        """anti-aliased polyline into the canvas (2x supersampled on a bbox-sized layer)."""
        pad = int(width) + 3
        x0 = int(np.floor(pts[:, 0].min())) - pad; y0 = int(np.floor(pts[:, 1].min())) - pad
        x1 = int(np.ceil(pts[:, 0].max())) + pad; y1 = int(np.ceil(pts[:, 1].max())) + pad
        x0c, y0c = max(x0, 0), max(y0, 0); x1c, y1c = min(x1, self.W), min(y1, self.H)
        if x1c <= x0c or y1c <= y0c: return
        w, h = x1 - x0, y1 - y0
        if w * h > 30_000_000: return
        layer = Image.new('L', (2 * w, 2 * h), 0)
        ImageDraw.Draw(layer).line([(2 * (px - x0), 2 * (py - y0)) for px, py in pts], fill=255,
                                   width=max(1, int(round(2 * width))), joint='curve')
        small = np.asarray(layer.resize((w, h), Image.BOX), np.float32) / 255.0
        sub = small[y0c - y0:y1c - y0, x0c - x0:x1c - x0] * dark
        region = self.canvas[y0c:y1c, x0c:x1c]
        np.maximum(region, sub, out=region)

    def darkness(self, tooth=0.45, seed=3):
        """final darkness with graphite tooth texture (paper grain) and gentle pressure variation."""
        rng = np.random.default_rng(seed)
        H, W = self.canvas.shape
        grain = blur(rng.random((H, W)).astype(np.float32), 0.8)
        grain = (grain - grain.min()) / (grain.max() - grain.min() + 1e-6)
        pressure = blur(rng.random((H // 16 + 1, W // 16 + 1)).astype(np.float32), 3)
        pressure = np.asarray(Image.fromarray((pressure * 255).astype(np.uint8)).resize((W, H), Image.BILINEAR), np.float32) / 255
        pressure = 0.75 + 0.5 * (pressure - pressure.min()) / (pressure.max() - pressure.min() + 1e-6)
        d = self.canvas * ((1 - tooth) + tooth * grain) * pressure
        return np.clip(blur(d, 0.6), 0, 1)
