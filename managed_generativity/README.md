# managed_generativity

A first local try at *managed generativity*: **gate** a part of an input (keep it verbatim), **generate**
everything around it. Input: a pencil fashion croquis photographed on tracing paper over a page of Java.

    gate      the pencil marks (kept pixel-for-pixel as a multiply layer)
    generate  paper, a tiny colour wash, and a procedurally drawn pencil scene behind her

## Outputs

    out_01_gated_tinted.png     the gated sketch on clean paper + the faint dress / skin wash
    out_02_runway.png           + a pencil runway (audience, backdrop, lighting truss)
    out_03_manhattan.png        + a pencil Manhattan street (canyon, crosswalk, cab, water tower, spire)
    *_preview.png               1/3-size versions of the above
    sketch_gated_on_paper.png   the gate alone, on paper (drop into any editor as a Multiply layer)
    sketch_gated_alpha.png      the gate alone, black with alpha = pencil darkness
    mask_silhouette.png         soft figure silhouette (what the scene is knocked out behind)
    mask_dress.png, mask_skin.png   where the two washes go
    survey.md                   Path A: the tool-landscape map, organised by how hard the gate is

## Pipeline (numpy + PIL only; no model weights, no network)

    analyze.py   estimate the paper tone per pixel -> relative darkness map        (diag/dark.npy)
    gate.py      soft matte that keeps pencil and drops bleed-through text; figure silhouette;
                 dress vs skin by stroke density; dust cleanup far from the drawing
    pencil.py    a procedural pencil: jittered multi-pass strokes, scribbled loops, hatching, tooth
    camera.py    one-point perspective; the ground plane is what she stands on
    scene_runway.py / scene_manhattan.py   draw the scene in metres, compose, save
    compose.py   paper * scene * (1 - silhouette) * washes * (1 - pencil)   <- the gate goes on last

    python3 analyze.py && python3 gate.py && python3 scene_runway.py && python3 scene_manhattan.py

## Knobs

    compose.py          PAPER tone; DRESS_COLOR / DRESS_ALPHA; SKIN_COLOR / SKIN_ALPHA
    gate.py             matte ramp (0.075..0.15 of relative darkness), halo width (dilate 4 @ half res),
                        dress density threshold (0.095)
    scene_*.py          Cam(vpx, yh): vanishing point and horizon; everything else is in metres
    pencil.py           stroke dark / width / jitter / passes / gap; darkness(tooth=...)

## Swapping the generator

The gate files are the contract. To go up the hardness ladder (see survey.md), generate the
background with any diffusion / instruction model, load it as `D_scene`-equivalent RGB, and run
`compose()` unchanged: the silhouette knockout and the verbatim pencil multiply are what make it
"managed". Verify with a pixel diff of the pencil layer: it should be identical by construction.
