"""Stage 1: GATE the sketch. Separate pencil from paper/bleed-through, keep pencil darkness verbatim,
derive the figure silhouette (for knocking out generated lines behind her) and dress/skin regions (for tint)."""
import numpy as np
from PIL import Image
from mg import *

im = Image.open('sketch_original.jpg')
g = np.asarray(im.convert('L')).astype(np.float32)
H, W = g.shape
dark = np.load('diag/dark.npy')                       # relative darkness vs. local paper (verbatim)

# --- matte: keep pencil, drop bleed-through text. gain computed on slightly blurred darkness so
#     thin faint glyphs fall below the ramp while pencil strokes/shading stay above it.
db = np.maximum(blur(dark, 1.5), dark * 0.6)
gain = smoothstep(db, 0.075, 0.15)
gain = np.maximum(gain, smoothstep(dark, 0.17, 0.26))    # anything clearly dark is kept outright
P = dark * gain                                        # pencil darkness layer (0 = paper, 1 = black)

# --- silhouette, computed at 1/2 scale
f = 2
m = down(P > 0.15, f)
mh = dilate(m, 0, 1); horiz = dilate(erode(mh, 18, 0), 20, 2)     # long ruler-ish lines (guide lines)
mv = dilate(m, 1, 0); vert = dilate(erode(mv, 0, 60), 2, 62)      # plumb line
m2 = m & ~horiz & ~vert
closed = close(m2, 9)
filled = open_(fill_holes(closed), 4)                     # cut thin bridges to stray marks
ys, xs = np.nonzero(m2); seed = (int(xs.mean()), int(ys.mean()))
fig = open_(floodfill_region(filled, seed), 2)
fig_core = fig.copy()
sil_hard = dilate(fig, 4)                                  # small margin ("halo") around the figure
sil = blur(up(sil_hard.astype(np.float32), (H, W)), 5)     # soft edge
np.save('diag/sil.npy', sil.astype(np.float32))

# --- dust specks: tiny compact blobs far from the drawing (outside the figure and the guide column).
#     keep anything containing a straight 7px run (lines, digits, ticks) via opening-by-reconstruction.
hard_d = down(P > 0.06, f)
def erode_line(mm, r, dx, dy):
    out = mm.copy()
    for s in range(-r, r + 1):
        if s: out &= shift(shift(mm, s * dy, 0, True), s * dx, 1, True)
    return out
markers = erode_line(hard_d, 6, 1, 0) | erode_line(hard_d, 6, 0, 1) | erode_line(hard_d, 6, 1, 1) | erode_line(hard_d, 6, 1, -1)
kept = geodesic_fill(dilate(hard_d, 1), markers)
specks = hard_d & ~kept
zone = np.ones_like(specks); zone[:, 500 // f:1350 // f] = False; zone[1900 // f:, :] = True   # away from figure + digits
specks &= zone & ~dilate(fig, 10)
P = np.where(up(dilate(specks, 3).astype(np.float32), (H, W)) > 0.3, 0.0, P)
print('specks removed (half-res px):', int(specks.sum()))
np.save('diag/P.npy', P.astype(np.float32))

# --- dress vs skin from stroke density (the dress is shaded/textured; skin is outline only)
dens = blur(P, 18)
dress_d = down(dens > 0.095, f) & erode(fig_core, 3)
dress_d[:540 // f, :] = False                               # the wash belongs below the shoulder line, not on the face
dress_d = fill_holes(close(dress_d, 10)) & erode(fig_core, 2)
dress = blur(up(dress_d.astype(np.float32), (H, W)), 6)
skin_d = erode(fig_core, 6) & ~dilate(dress_d, 6)
skin = blur(up(skin_d.astype(np.float32), (H, W)), 6)
np.save('diag/dress.npy', dress.astype(np.float32)); np.save('diag/skin.npy', skin.astype(np.float32))

yy, xx = np.nonzero(fig_core)
print('figure bbox (full res): x', xx.min()*f, xx.max()*f, ' y', yy.min()*f, yy.max()*f, ' cx', int(xx.mean()*f))

# --- deliverable layers
paper = np.full((H, W), 0.965, np.float32)
to_img(paper * (1 - P)).save('sketch_gated_on_paper.png')
rgba = np.zeros((H, W, 4), np.uint8); rgba[..., 3] = np.clip(P * 255 + 0.5, 0, 255).astype(np.uint8)
Image.fromarray(rgba, 'RGBA').save('sketch_gated_alpha.png')
to_img(sil).save('mask_silhouette.png'); to_img(dress).save('mask_dress.png'); to_img(skin).save('mask_skin.png')
to_img(paper * (1 - P)).resize((W // 3, H // 3)).save('diag/gated_small.png')
gated = paper * (1 - P)
rgb = np.stack([gated]*3, -1)
rgb[..., 0] *= (1 - 0.35 * sil); rgb[..., 1] *= (1 - 0.15 * sil)
rgb[..., 1] *= (1 - 0.5 * dress); rgb[..., 2] *= (1 - 0.4 * dress); rgb[..., 2] *= (1 - 0.5 * skin)
Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8)).resize((W // 3, H // 3)).save('diag/overlay.png')
print('done')
