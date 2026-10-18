"""managed generativity helpers: float blur, binary morphology, fills (numpy + PIL only)."""
import numpy as np
from PIL import Image, ImageDraw

def _box1d(a, r, axis):
    if r <= 0: return a
    pad = [(0, 0)] * a.ndim; pad[axis] = (r + 1, r)
    ap = np.pad(a, pad, mode='edge')
    c = np.cumsum(ap, axis=axis, dtype=np.float64)
    n = a.shape[axis]
    hi = [slice(None)] * a.ndim; lo = [slice(None)] * a.ndim
    hi[axis] = slice(2 * r + 1, 2 * r + 1 + n); lo[axis] = slice(0, n)
    return ((c[tuple(hi)] - c[tuple(lo)]) / (2 * r + 1)).astype(np.float32)

def blur(a, sigma):
    """Gaussian approx by 3 box passes (float32 array, any radius, O(N))."""
    a = a.astype(np.float32)
    if sigma <= 0: return a
    w = np.sqrt(4 * sigma * sigma + 1); r = max(1, int(round((w - 1) / 2)))
    for _ in range(3):
        a = _box1d(_box1d(a, r, 0), r, 1)
    return a

def shift(a, s, axis, fill):
    out = np.full_like(a, fill); n = a.shape[axis]
    if s == 0: return a.copy()
    if abs(s) >= n: return out
    src = [slice(None)] * a.ndim; dst = [slice(None)] * a.ndim
    if s > 0: src[axis] = slice(0, n - s); dst[axis] = slice(s, n)
    else:     src[axis] = slice(-s, n);    dst[axis] = slice(0, n + s)
    out[tuple(dst)] = a[tuple(src)]
    return out

def runmax(m, r, axis, fill=False):
    """boolean max over window [i-r, i+r] along axis (doubling trick); `fill` = value outside the image."""
    if r <= 0: return m.copy()
    L = 2 * r + 1; out = m.copy(); cov = 1
    while cov * 2 <= L:
        out = out | shift(out, -cov, axis, fill); cov *= 2
    if cov < L:
        out = out | shift(out, -(L - cov), axis, fill)
    return shift(out, r, axis, fill)

def dilate(m, rx, ry=None, fill=False):
    ry = rx if ry is None else ry
    return runmax(runmax(m, rx, 1, fill), ry, 0, fill)

def erode(m, rx, ry=None):
    ry = rx if ry is None else ry
    return ~dilate(~m, rx, ry, fill=True)        # outside the image counts as background

def close(m, r):  return erode(dilate(m, r), r)
def open_(m, r):  return dilate(erode(m, r), r)

def _run_prop(mask, seed, axis):
    """propagate seed along contiguous True runs of mask along axis (vectorised)."""
    if axis == 0: mask, seed = mask.T, seed.T
    starts = mask & ~shift(mask, 1, 1, False)
    run_id = np.cumsum(starts, axis=1, dtype=np.int64)
    run_id = run_id + (np.arange(mask.shape[0])[:, None] * (mask.shape[1] + 1))   # unique across rows
    flat_ids = run_id[mask]; hit = np.zeros(int(run_id.max()) + 2, bool)
    hit[flat_ids[seed[mask]]] = True
    out = mask & hit[run_id]
    return out.T if axis == 0 else out

def geodesic_fill(mask, seed):
    """connected True region of mask reachable (4-conn) from seed pixels, alternating row/col run passes."""
    cur = mask & seed
    while True:
        nxt = _run_prop(mask, cur, 1); nxt = _run_prop(mask, nxt, 0)
        if nxt.sum() == cur.sum(): return nxt
        cur = nxt

def floodfill_region(mask, seed_xy):
    x, y = seed_xy
    if not mask[y, x]:
        ys, xs = np.nonzero(mask); i = np.argmin((xs - x) ** 2 + (ys - y) ** 2); x, y = int(xs[i]), int(ys[i])
    seed = np.zeros_like(mask); seed[y, x] = True
    return geodesic_fill(mask, seed)

def fill_holes(mask):
    """fill enclosed background regions: flood the exterior from the border."""
    pad = np.pad(mask, 1, constant_values=False)
    seed = np.zeros_like(pad); seed[0, :] = seed[-1, :] = seed[:, 0] = seed[:, -1] = True
    ext = geodesic_fill(~pad, seed)
    return (~ext)[1:-1, 1:-1]

def smoothstep(x, lo, hi):
    t = np.clip((x - lo) / max(hi - lo, 1e-6), 0, 1)
    return t * t * (3 - 2 * t)

def to_img(a):
    return Image.fromarray(np.clip(a * 255 + 0.5, 0, 255).astype(np.uint8))

def down(mask, f):
    """downsample boolean mask by factor f with 'any' pooling."""
    H, W = mask.shape; H2, W2 = H // f * f, W // f * f
    return mask[:H2, :W2].reshape(H2 // f, f, W2 // f, f).any(axis=(1, 3))

def up(a, shape):
    """bilinear upsample float array to (H, W)."""
    H, W = shape
    return np.asarray(to_img(a).resize((W, H), Image.BILINEAR), dtype=np.float32) / 255.0
