# Managed generativity: a map of the AI-graphics landscape (as of 2026-10-18)

Path A of the session: not depth, just the categories, the sources, and a way to think about it.
Organised by how hard the **gate** is, because that is the axis your concept introduces and the one
the market does not label.

## Vocabulary

    gate       the part held verbatim (here: the pencil marks of the sketch)
    generate   everything else
    hardness   how literally a tool honours the gate
        hard   pixels untouched: layers, masks, compositing; nothing re-paints the gate
        firm   geometry kept, strokes re-rendered: structure conditioning (ControlNet-style)
        soft   the gate is a request in a prompt or a reference image; the model may redraw it
    surface    where it runs: chat app / pro app / node graph / API / local weights / agent

## 0. How to think about it

    - Two axes organise everything below:
        axis 1  hardness of the gate (hard / firm / soft): pick by what must not change
        axis 2  surface (who drives: you clicking, you coding, or an LLM operating tools)
    - Every real pipeline is the same stack, whatever the tool:
        1  define the gate as a file (a matte or mask plus the verbatim layer)
        2  generate at the chosen hardness
        3  re-gate: composite the verbatim layer back on top
        4  verify: pixel diff inside the gate should be ~0
    - 2026 centre of gravity: "unified" instruction editors (soft gate, many reference images)
      for anything casual; masks and layers for anything that must stay verbatim.
    - Failure mode to design around: soft tools redraw the sketch (cleaner lines, changed
      proportions) even when told not to. Treat their output as background and re-gate.

## 1. HARD gate (pixel level: the gate is never touched)

    1.1 Layer compositing (what Path B does today)
        - multiply the pencil layer over any generated background; works in Photoshop, Krita,
          Affinity, GIMP, or 20 lines of numpy/PIL/OpenCV/ImageMagick
        - LLM-written procedural graphics: SVG, Canvas/p5.js, PIL, matplotlib, TikZ. The LLM
          writes deterministic code; the sketch is just a layer. Hardest gate there is.
    1.2 Mask inpainting / outpainting (generate only inside or outside a mask)
        - Photoshop Generative Fill / Expand: now defaults to the "Firefly Fill & Expand" model,
          partner models selectable (Gemini 2.5 Flash Image, FLUX.1 Kontext Pro)
          https://community.adobe.com/product-updates/1546650  [agent-confirmed]
        - OpenAI Images API edits: transparent pixels mark the editable region (gpt-image-2)
          https://developers.openai.com/docs/guides/image-generation  [agent-confirmed]
        - FLUX.1 Fill (BFL), Stable Image inpaint/outpaint (Stability v2beta), Midjourney Editor,
          Ideogram Canvas  [unconfirmed this round; known mid-2026]
        - InvokeAI canvas (strongest open-source inpaint/compositing UI, v6.14, Sep 2026)
          https://github.com/invoke-ai/InvokeAI  [agent-confirmed]
        - Krita AI Diffusion plugin v1.53 (selection-based inpaint on a ComfyUI backend)
          https://github.com/Acly/krita-ai-diffusion  [agent-confirmed]
        caveat: most inpainters re-encode the whole image through a VAE, so "outside the mask"
        is near-verbatim, not bit-exact. Re-composite the original if it matters.
    1.3 Defining the gate (segmentation and mattes: the tools that make masks)
        - SAM 3 / 3.1 (text-promptable segmentation, Mar 2026 checkpoints)
          https://github.com/facebookresearch/sam3  [agent-confirmed]
        - BiRefNet / rembg (background removal) https://github.com/ZhengPeng7/BiRefNet
        - Depth Anything 3 (depth maps, Nov 2025, Apache-2.0)  [agent-confirmed]
        - ControlNet preprocessors (lineart / HED / PiDiNet: turn any image into a sketch)
          https://github.com/huggingface/controlnet_aux
        - OpenCV / ImageMagick / numpy thresholds and morphology (what today's gate used)

## 2. FIRM gate (structure level: geometry kept, pixels re-rendered)

    2.1 Structure conditioning
        - ControlNet family (scribble / lineart / canny / depth / pose) for SD1.5 and SDXL
          https://github.com/lllyasviel/ControlNet ; newer DiT models ship native controls instead
        - FLUX.1 Tools: Canny, Depth, Fill, Redux (still the FLUX.1 family; FLUX.2-native
          controls not seen)  https://help.bfl.ai/articles/9364115800-flux-models-overview
        - Stability Stable Image API, Control endpoints: Sketch (control_strength 0..1 is
          literally a dial on the gate), Structure, Style  https://platform.stability.ai/docs/api-reference
        - SD3.5 ControlNets (Blur / Canny / Depth)  [legacy]
    2.2 Sketch-to-render products (the closest commercial fit for a fashion sketch)
        - Vizcom (designers' sketch rendering)  https://www.vizcom.ai  [agent-confirmed]
        - Krea Realtime Canvas (live sketch-to-image)  https://www.krea.ai  [agent-confirmed]
        - Leonardo (Canva-owned; canvas, Phoenix / Lucid Origin models)  https://leonardo.ai
        - InvokeAI Control Layers + Regional Guidance (the most "managed" UI in open source)
        - Scenario, Google Vertex Imagen 4 controls, AWS Nova Canvas conditioning  [not searched]
    2.3 Low-strength img2img (denoise 0.2 to 0.4): the oldest trick, in every SD interface
    2.4 Reference / identity / style adapters (a gate on what it looks like, not where)
        - IP-Adapter, InstantID, PuLID, FLUX.1 Redux  [not searched; stable]
        - Midjourney --sref / --oref (carried into V8.x), Firefly style and structure reference
        - trend: native multi-reference inputs are replacing bolt-on adapters
          (Nano Banana Pro up to 14 refs, gpt-image-2 up to 16, Seedream 5 up to 10,
          Qwen-Image-2.1 up to 10)  [agent-confirmed]

## 3. SOFT gate (semantic: "keep the sketch, add a runway" as an instruction)

    3.1 Unified instruction editors (generation and editing in one model): the 2026 mainstream
        - Google "Nano Banana" line: Pro = Gemini 3 Pro Image; 2 = Gemini 3.1 Flash Image;
          2.1 listed as newest on the Gemini API docs
          https://ai.google.dev/gemini-api/docs/models/gemini-nano-banana-2.1  [agent-confirmed]
        - OpenAI gpt-image-2 ("ChatGPT Images 2.0", alias chatgpt-image-latest); "2.5" unconfirmed
          https://developers.openai.com/docs/guides/image-generation  [agent-confirmed]
        - Black Forest Labs FLUX.2 Pro / Flex / Dev (32B) / Klein 4B & 9B; FLUX.1 Kontext still sold
          https://help.bfl.ai/articles/9364115800-flux-models-overview  [agent-confirmed]
        - Alibaba Qwen-Image-2.1 (open weights 7B, gen + edit, RGBA layer output, Sep 2026);
          Qwen-Image 3.0 closed preview  [secondary sources only]
        - ByteDance Seedream 5.0 Pro Edit (1 to 10 refs)  [agent-confirmed]
        - Midjourney V8.x (V8.1 default from Jun 2026)  https://docs.midjourney.com/docs/models
        - Adobe Firefly Image 5 (native 4MP, layered editing)  [agent-confirmed]
        - Ideogram 4 (text, transparent backgrounds), Recraft V4.1 (native SVG), Krea 2,
          Runway Gen-4.5, Reve 2.1 (sunsetting Sep 2026), Luma Uni-1, HiDream-O1,
          Meta Muse Image  [last four unconfirmed]
        caveat for your spec: these redraw the sketch unless you re-composite the original.
        Use them for the background and re-gate.
    3.2 Vector and layered outputs (soft generation, but editable output lets you re-impose the gate)
        - Recraft SVG; Adobe Illustrator generative vector; Figma Weave (ex-Weavy node canvas,
          acquired late 2025); Canva Magic Studio; Vectorizer.ai
        - layered raster: Firefly 5 layers, Qwen-Image-2.1 RGBA, Ideogram 4 transparent
    3.3 Image-to-video (the first frame is the gate; time is what gets generated)
        - Runway Gen-4.5, Kling 3.0 / Omni, Google Veo 3.1, Alibaba Wan 3.0 (open: 2.x),
          Luma Ray3.2, MiniMax Hailuo 2.3  [agent-confirmed via roundups]
        - OpenAI Sora discontinued (API shut Sep 2026, two secondary sources; verify)
        - this is "the sketch walking in Manhattan" taken literally
    3.4 Image-to-3D (gate the silhouette, generate a mannequin): Tripo, Meshy, Hunyuan3D,
        TRELLIS  [not searched]

## 4. SURFACES (where you run any of the above)

    4.1 Chat apps: ChatGPT, Gemini, Grok, Meta AI. Claude has no native image generation.
    4.2 Pro apps with AI inside: Photoshop / Illustrator / Firefly app (partner-model hub),
        Krita + AI Diffusion, Affinity, Clip Studio, Figma (Weave, Make), Canva, Blender add-ons.
        Procreate publicly declines generative AI.
    4.3 Node graphs and power UIs: ComfyUI (lingua franca; Comfy Cloud; official Comfy MCP
        since Jun 2026  https://docs.comfy.org/development/cloud/mcp-server), InvokeAI,
        Krita AI Diffusion, SD WebUI Forge (your repo's namesake; maintenance status unclear),
        Fooocus (maintenance mode), Draw Things (Mac/iOS), Figma Weave, Krea, Leonardo, Freepik,
        Playground
    4.4 APIs and hosted inference ("let me plug in and program")
        - first-party: OpenAI Images API, Gemini API, BFL API, Stability v2beta, Ideogram,
          Recraft, Runway, Adobe Firefly Services, AWS Bedrock Nova Canvas, Vertex Imagen
        - aggregators: fal.ai (https://fal.ai), Replicate, Together, Fireworks, Hugging Face
          Inference, OpenRouter (now routes image models), Civitai orchestration, Atlas Cloud
        - ComfyUI hosting: Comfy Cloud, RunComfy, RunDiffusion, ComfyDeploy, Modal
    4.5 Local open weights and libraries
        - libraries: Hugging Face diffusers, stable-diffusion.cpp, MLX (mflux)
        - laptop-class: FLUX.2 Klein 4B (Apache-2.0), Z-Image Turbo 6B, Qwen-Image-2.1 7B
          quantised, FLUX.2 dev GGUF
        - bigger: FLUX.2 dev 32B, HunyuanImage 3.0 80B; legacy: SDXL, SD3.5, FLUX.1 dev
    4.6 Agentic layer (an LLM operates the graphics tools)
        - official Comfy MCP + community ComfyUI MCP servers (target Claude Code / Desktop)
          https://docs.comfy.org/agent-tools
        - Stability MCP server (control-sketch / structure tools), Figma MCP, Blender MCP
        - gpt-image-2 inside Codex; Claude Code driving scripts and MCP generically (this session)

## 5. Decision procedure for a managed-generativity job

    1  name the gate precisely: pixels? geometry? identity or style? meaning only?
    2  make the gate a file: matte + verbatim layer (SAM, threshold, morphology)
    3  generate at the softest hardness that still satisfies step 1 (softer = richer output)
    4  re-gate: composite the verbatim layer on top (multiply for pencil and ink; alpha for colour)
    5  verify: pixel diff inside the gate ~0; eyeball the seam (halo width, paper-tone match)

    For this sketch today: (1) the pencil pixels; (2) built: P = pencil darkness, the figure
    silhouette, dress and skin masks; (3) hard: a procedural pencil scene; (4) multiply;
    (5) the gate layer is identical by construction. Next step up the ladder: feed the same
    files to a soft tool (Nano Banana / gpt-image-2 / FLUX.2) for the background only, then
    re-gate with compose.py unchanged.

## 6. New since mid-2026 (from the agent's search; dates are from third-party roundups)

    - Nano Banana 2.1 on the Gemini API docs; Nano Banana 2 Lite (Jun 30 2026)
    - official Comfy MCP (Jun 30 2026), cloud MCP in public beta
    - Qwen-Image-2.1 open weights with RGBA layers (Sep 20 2026); Qwen-Image 3.0 closed preview
    - Recraft V4.1 Pro (Aug 2026); Krita AI Diffusion 1.53 (Aug 2026); InvokeAI 6.14.2 (Sep 2026)
    - Reve sunsetting image generation (Sep 2026); Sora API shutdown (Sep 24 2026)
    - unconfirmed, single-source: ChatGPT Images 2.5, FLUX.2 Max, Midjourney V8.2 default,
      Meta Muse Image, Kling 4.0, Hailuo H3, Google "Omni Flash"

## 7. Provenance

    - A research agent ran 19 web searches on 2026-10-18 (snippets only, no pages read).
      Items marked [agent-confirmed] appeared in those results; [unconfirmed] means it looked
      for them and found nothing solid; [not searched] means the item is from my own knowledge,
      which ends mid-2026, and may be stale.
    - Nothing here is in depth by design. Each line is a hook to pull on, not a verdict.
