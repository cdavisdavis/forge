"""one-point-perspective camera: ground plane Y=0 is what the figure stands on; camera hc metres above it."""
import numpy as np

class Cam:
    def __init__(self, vpx, yh, f=800.0, hc=0.8, zmin=0.3):
        self.vpx, self.yh, self.f, self.hc, self.zmin = vpx, yh, f, hc, zmin
    def proj(self, X, Y, Z):
        return self.vpx + self.f * X / Z, self.yh - self.f * (Y - self.hc) / Z
    def seg(self, a, b, n=16):
        a = np.asarray(a, float); b = np.asarray(b, float); z = self.zmin
        if a[2] < z and b[2] < z: return None
        if a[2] < z: a = a + (z - a[2]) / (b[2] - a[2]) * (b - a)
        if b[2] < z: b = b + (z - b[2]) / (a[2] - b[2]) * (a - b)
        t = np.linspace(0, 1, n)[:, None]; P = a + t * (b - a)
        x, y = self.proj(P[:, 0], P[:, 1], P[:, 2]); return np.c_[x, y]
    def poly(self, pts3):
        return np.array([self.proj(*p) for p in pts3], float)
