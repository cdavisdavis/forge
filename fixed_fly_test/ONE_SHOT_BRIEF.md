# One-shot brief — fixed-fly decomposition test, v1

Date written: 5 Nov 2026. Lead: Chris (cdavisdavis). Written by the seat (Claude Code cloud); his ruling owed.
**This file is the entire instruction for an unattended run. Do not ask questions. Every decision below has a default; take it and record that you took it.**

Companion: `PLAN.md` (the why). Repo branch: `claude/fixed-fly-decomposition-test-d3fuhu`. Work under `fixed_fly_test/run_<YYYYMMDD>/`.

---

## 0. What is being tested

`[D 1.1e]` (23 Sep 2026): *flying is operating with the basis held fixed; fixing is changing the presumptions.*

Claim under test: a book in a dense, derivable subject can be decomposed into a small **fixed kernel** (nouns + verbs) from which a model, **flying**, regenerates most of the book's work — and this holds **out of sample** (perturbed axioms, renamed vocabulary), not just where training already holds the answers.

Pre-registered predictions (write them into the results file BEFORE running any flyer; do not edit them afterwards):
- P1. **Regeneration per kernel token** (mean condition-B score ÷ kernel tokens, scaled per 1,000) orders Rudin > UML > Kuhn.
- P2. Rudin condition A (no kernel) already scores high (contamination). B−A small and positive.
- P3. D−C ≈ 0 (prior outputs add nothing once the operator and canonical examples are loaded).
- P4. Condition P (perturbed axiom) is where B beats A clearly — a kernel-running flyer tracks which results survive the perturbation; a retrieving flyer does not.
- P5. Condition N (renamed vocabulary) costs B little and costs A a lot.
- P6. Kuhn: central claims regenerate well; examples (Lavoisier, Copernicus, Leyden jar, etc.) do not — they are fitted, not derivable.

## 1. Sources (obtain in this order; on failure record and use the fallback)

| arm | book | scope | primary source | fallback |
|---|---|---|---|---|
| R | Rudin, *Principles of Mathematical Analysis*, 3rd ed. | Ch. 1 (Real and Complex Number Systems), Ch. 2 (Basic Topology), all end-of-chapter exercises | Dropbox `/a_ClaudeMain_DropBox/c_ all_refs_via_OneDrive_0808/a          Primary Refs 1     LargeSized_Books/Principles_of_Mathematical_Analysis-Rudin.pdf` (12.9 MB: use Dropbox `download_link`, then `curl` into `sources/`) | Fixer writes kernel from its own knowledge; mark arm `SOURCE=memory` — results reported but flagged degraded |
| U | Shalev-Shwartz & Ben-David, *Understanding Machine Learning* (2014) | Ch. 2–6 (gentle start → VC dimension), end-of-chapter exercises | Author's free PDF: `https://www.cs.huji.ac.il/~shais/UnderstandingMachineLearning/understanding-machine-learning-theory-algorithms.pdf` | Same `SOURCE=memory` rule |
| K | Kuhn, *The Structure of Scientific Revolutions*, 2nd ed. | Whole book incl. Postscript | Dropbox `/a_ClaudeMain_DropBox/a_ canonical_entities__warehouse/a_ method/a_ method_history_/a_ kuhn/Kuhn-SSR-2ndEd.pdf` (fetch) | Skip arm; record `SKIPPED: source` |

Extract text with `pdftotext -layout` (install `poppler-utils` if missing). Store under `run_*/sources/` but **add `sources/` to `.gitignore`** — copyrighted text is not committed. Commit only kernels, items, answers, scores, and summaries.

Reference solutions for checking Rudin: if reachable, a public solution set (e.g. Roger Cooke's solutions to Rudin ch. 1–2); otherwise the checker grades from the book's text and its own derivation, and the score row carries `ref=none`.

## 2. Roles (three separate subagents; never merged)

- **FIXER** — reads the source. Writes the kernel. Never answers items.
- **FLYER** — receives *only* the text pasted into its prompt (kernel + item). Instruction in every flyer prompt: *"Do not use any tools. Do not open files. Answer from what is in this prompt and what you already know."* Each item is a fresh flyer call (no shared context across items), except condition D.
- **CHECKER** — receives the source section, the item, the reference solution if any, and the flyer's answer. Never sees which condition produced the answer (strip condition labels; shuffle order). Scores.

The orchestrating seat (you) runs no flights and grades nothing. If the Workflow tool is available, use it with one agent per role-call; otherwise use the Agent tool.

## 3. The kernel (FIXER output) — format

File: `run_*/<arm>/kernel.md`. Numbered items, stable ids, fixed order across all conditions.

```
## NOUNS
K-01 [def] Ordered set: ...
K-02 [def] Upper bound, supremum: ...
## VERBS
K-20 [axiom] Least-upper-bound property: every nonempty subset bounded above has a supremum.
K-21 [rule] Archimedean step: ...
K-22 [theorem-as-tool] (Rudin 1.20) ...  ← statement only, no proof
## EXAMPLES (condition C only — held in a separate file kernel_examples.md)
E-01 ...
```

Kernel rules:
- Nouns = definitions of objects. Verbs = axioms, inference moves, and theorems *stated* (no proofs) that the book uses as tools.
- Proofs and worked examples go ONLY in `kernel_examples.md` (condition C).
- Budget: the kernel should be as small as the fixer can make it while it still lets the book's own results be derived from it. Record token counts (`wc -w` × 1.33 is acceptable as the token estimate; say so) for kernel, kernel_examples, and the source scope.
- Kuhn kernel: nouns = Kuhn's concepts; verbs = the dynamics he asserts (how normal science runs, how anomaly becomes crisis, how crisis resolves, why choice between paradigms is not settled by logic alone). No historical cases in the kernel; they go in `kernel_examples.md`.

## 4. Items

- Rudin: every end-of-chapter exercise of Ch. 1 and Ch. 2, verbatim from the source, one per line in `items.jsonl` (`{"id":"R1.05","text":...}`).
- UML: every end-of-chapter exercise of Ch. 2–6.
- Kuhn: no exercises. FIXER writes, from the source (not the kernel), one central claim per chapter (13 chapters + Postscript) and one example per chapter that the chapter leans on. Items are posed as: *"From the kernel, derive what Kuhn argues about <chapter topic>."* and *"Name and describe a historical case that illustrates <chapter claim>."* The second type measures example regeneration (P6).

## 5. Conditions

| code | flyer prompt contains | arms |
|---|---|---|
| A | item only | R, U, K |
| B | kernel.md + item | R, U, K |
| C | kernel.md + kernel_examples.md + item | R, U, K |
| D | C + the flyer's own previous answers in this arm (run items sequentially in one context) | R only |
| P | kernel.md **with K-axiom "least-upper-bound property" deleted and the line "Work over the rationals ℚ; the least-upper-bound property does NOT hold." added** + perturbed item | R only |
| N | kernel.md and item with every technical term mapped through `rename_map.json` (FIXER writes the map: e.g. supremum→plinth, compact→sorrel, metric→tensa); answers are back-mapped before checking | R, U |

**Perturbed items (condition P).** FIXER lists every numbered theorem/proposition in Rudin Ch. 1–2 (statements only). For each, the P item is: *"Over ℚ with the kernel as given: does this statement still hold? Answer HOLDS or FAILS, then give a derivation or counterexample using only kernel items."* Ground truth for each is written by the CHECKER from first principles *before* any flyer runs, and stored in `p_truth.jsonl`. Flag `route_breaks=true` on items where the statement holds over ℚ but Rudin's own proof uses the least-upper-bound property (e.g. the Archimedean property, 1.20(a)). Report P accuracy overall and on `route_breaks=true` separately — that subset is the sharpest number in the run.

Run conditions A and P also with an empty kernel (A-P: item over ℚ, no kernel) so P's lift over training alone is measurable.

## 6. Flyer answer format

Every flyer answer ends with a step table:

```
STEPS
1. <step> — uses K-20
2. <step> — uses K-07, K-21
3. <step> — OUT (not from the kernel)
```

`kernel citation rate` = steps citing K-items ÷ all steps. Condition A has no kernel, so A's steps are all OUT by definition — skip the table for A.

## 7. Scoring (CHECKER)

Per answer, write one row to `scores.jsonl`:
`{"arm":"R","item":"R1.05","cond_hidden_id":"x7f2","score":0|1|2,"reason":"<one line>","ref":"cooke|book|none","p_correct_verdict":true|false|null}`
- 2 = correct and complete; 1 = right idea, a gap or error a grader would mark down; 0 = wrong or missing.
- For P items, `p_correct_verdict` = HOLDS/FAILS matches `p_truth`; score the derivation separately.
- Kuhn claim items: 2 = matches the chapter's central claim; 1 = adjacent; 0 = off. Kuhn example items: 2 = the case Kuhn actually uses for that point; 1 = a fitting case Kuhn does not use there; 0 = none or wrong.
- CHECKER audits each flyer transcript for tool calls; any flyer that used a tool has its answer scored but flagged `contaminated_tool=true` and excluded from headline means.

After scoring, un-blind (join hidden ids back to conditions) in a script, not by hand.

## 8. Readouts (`results.md`)

1. Pre-registered predictions P1–P6 (copied verbatim, unchanged).
2. Per arm: token counts (source scope, kernel, kernel_examples) and compression ratio.
3. Mean score per condition per arm, with n. Lifts: B−A, C−B, D−C, N-vs-B, and for P: B-P vs A-P overall and on `route_breaks=true`.
4. Kernel citation rate per condition.
5. Kuhn: claim regeneration vs example regeneration, side by side.
6. Each prediction marked: HELD / DID NOT HOLD / MIXED, with the number that decides it. No other verdict words.
7. Residuals (3–8 lines): what the run could not separate. At minimum — training contamination in A–D; flyer isolation is by instruction, not by wall; the checker is the same model family as the flyer.
8. Five worked examples, chosen by rule (not by taste): for Rudin, the two `route_breaks=true` P items with the largest B-P vs A-P difference, and the lowest-scoring B item; for Kuhn, the best and worst example item.

Also produce `summary.html` (single self-contained page: the readout tables and the five worked examples). No external scripts.

## 9. Order of work and checkpoints

1. Set up `run_*/`, `.gitignore` for `sources/`, write predictions into `results.md`. **Commit.**
2. Obtain sources (§1). Record outcome per arm.
3. FIXER: kernels, kernel_examples, items, rename maps, P list. **Commit** (kernels and items only).
4. CHECKER: `p_truth.jsonl`. **Commit.**
5. FLYERS: arm R (A, B, C, D, P, A-P, N), then U (A, B, C, N), then K (A, B, C). **Commit after each arm.**
6. CHECKER: score blind. **Commit.**
7. Un-blind, compute, write `results.md` and `summary.html`. **Commit and push** to `claude/fixed-fly-decomposition-test-d3fuhu` (`git push -u origin <branch>`; retry on network failure 4× with 2/4/8/16 s backoff).

Stop/skip rules: an arm whose source fails and whose fallback also fails is recorded `SKIPPED` and the run continues. If the run is about to exhaust its budget, finish scoring and readouts for completed arms before starting a new arm — a scored small run beats an unscored large one. Never fabricate a score, a count, or a source; a missing number is written `—` with the reason.

## 10. House rules for every written output

- Vocabulary: do not use *confirm, discover, novel*, or claim the test *proves* anything (the mathematical sense of "prove" inside an exercise answer is fine). Licensed: *held, did not hold, the residual, the frame*.
- Gloss any specialist term in parentheses on first use. No acronyms outside the arm/condition codes defined here.
- Attribution: framing is Chris's; construction is the seat's ("seat's articulation, his ruling owed"). Do not attribute the seat's choices to him.
- Residuals come after results, never before.
