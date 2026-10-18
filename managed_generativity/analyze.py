import numpy as np
from PIL import Image, ImageFilter
im = Image.open('sketch_original.jpg')
g = np.asarray(im.convert('L')).astype(np.float32)
H, W = g.shape
# background (paper) estimate: downsample, max-filter (pencil is dark), blur, upsample
small = Image.fromarray(g.astype(np.uint8)).resize((W//8, H//8), Image.BOX)
bg = small.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(6)).resize((W, H), Image.BICUBIC)
bg = np.asarray(bg).astype(np.float32)
dark = np.clip((bg - g) / np.maximum(bg, 1), 0, 1)   # relative darkness 0..1
np.save('diag/dark.npy', dark)
print('paper bg percentiles', np.percentile(bg, [1, 50, 99]))
print('dark percentiles', np.percentile(dark, [50, 90, 95, 98, 99, 99.5, 99.9]))
# visualize darkness (inverted) and a few thresholds
Image.fromarray((255 - dark*255).astype(np.uint8)).resize((W//3, H//3)).save('diag/dark_vis.png')
for t in [0.06, 0.10, 0.15, 0.22]:
    m = (dark > t)
    Image.fromarray((255 - m*255).astype(np.uint8)).resize((W//3, H//3)).save(f'diag/thr_{int(t*100):02d}.png')
    print('thr', t, 'frac', m.mean())
# histogram of darkness in a text-only region (top-right band) vs the skirt region
print('text region (y 350-700 of top, x 1500-1900) dark pct', np.percentile(dark[350:700, 1500:1900], [90, 99, 99.9]))
