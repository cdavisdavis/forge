"""Stage 3: COMPOSE. paper * generated-scene (knocked out behind the figure) * tiny tints * gated sketch (verbatim)."""
import numpy as np
from PIL import Image, ImageDraw
from mg import blur

W, H = 1962, 2576
PAPER = (0.965, 0.955, 0.935)
DRESS_COLOR, DRESS_ALPHA = (0.84, 0.58, 0.62), 0.30     # dusty rose, faint
SKIN_COLOR, SKIN_ALPHA = (0.94, 0.80, 0.70), 0.30       # warm peach, faint

def load_gate():
    return np.load('diag/P.npy'), np.load('diag/sil.npy'), np.load('diag/dress.npy'), np.load('diag/skin.npy')

def paper_layer(seed=1):
    rng = np.random.default_rng(seed)
    grain = blur(rng.random((H, W)).astype(np.float32), 1.0); grain = (grain - grain.mean()) * 0.06
    out = np.empty((H, W, 3), np.float32)
    for c in range(3): out[..., c] = PAPER[c] + grain
    return out

def tint_factor(mask, color, alpha):
    a = (np.clip(mask, 0, 1) * alpha)[..., None]
    return 1 - a * (1 - np.asarray(color, np.float32))

def wash_noise(seed=4):
    rng = np.random.default_rng(seed)
    n = rng.random((H // 40 + 2, W // 40 + 2)).astype(np.float32)
    n = np.asarray(Image.fromarray((n * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC), np.float32) / 255
    n = blur(n, 12); n = (n - n.min()) / (n.max() - n.min() + 1e-6)
    return 0.55 + 0.45 * n

def radial_mask(cx, cy, sigma):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    return np.exp(-((xx - cx) ** 2 + (yy - cy) ** 2) / (2 * sigma ** 2))

def poly_mask(poly, feather=3):
    m = Image.new('L', (W, H), 0)
    ImageDraw.Draw(m).polygon([(float(x), float(y)) for x, y in poly], fill=255)
    return blur(np.asarray(m, np.float32) / 255, feather)

def compose(D_scene, out_path, extra_tints=(), scene_strength=1.0, tint=True):
    P, sil, dress, skin = load_gate()
    out = paper_layer()
    if D_scene is not None:
        out *= (1 - np.clip(D_scene, 0, 1) * scene_strength * (1 - sil))[..., None]   # scene, knocked out behind her
    if tint:
        wn = wash_noise()
        out *= tint_factor(dress * wn, DRESS_COLOR, DRESS_ALPHA)
        out *= tint_factor(skin * wn, SKIN_COLOR, SKIN_ALPHA)
    for mask, color, alpha in extra_tints:
        out *= tint_factor(mask, color, alpha)
    out *= (1 - P)[..., None]                                                           # the gate: pencil, verbatim
    img = Image.fromarray((np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8))
    img.save(out_path)
    img.resize((W // 3, H // 3), Image.LANCZOS).save(out_path.replace('.png', '_preview.png'))
    return img
