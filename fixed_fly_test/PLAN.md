# Fixed-fly decomposition test: plan sketch, v1 (5 Nov 2026)

Seat: Claude Code (cloud). Lead: Chris. Everything below that is not quoted is the seat's articulation; Chris's ruling is still owed.

This builds on three files already in Dropbox:
- `context-parameters-rudin-test.md` (2 Oct): the Rudin test, conditions A–D, and a perturbed control.
- `kuhn-logic-versus-examples.md` (7 Oct): thin logic plus many examples, and the split between "derivable" and "fitted" examples.
- `step7__fix_and_fly_test__v1__20260923.md`, definition `[D 1.1e]`: *flying is operating with the basis held fixed; fixing is changing the presumptions.*

---

## 1. The idea in one paragraph

Take a book. **Fix** a small kernel from it: the nouns (objects and definitions), the verbs (the moves the subject allows: inference rules and named theorems used as tools), and a few canonical examples. Then **fly**: a fresh model sees only that kernel and must regenerate what the book does, meaning its exercises, its results and its arguments. Compare the result to the book.

Two numbers come out:
- **compression:** how many tokens the kernel is, divided by how many tokens the book is;
- **regeneration:** how much of the book flying from that kernel recovers.

## 2. Your question: "flying is a logic, and the subject is just a subject?"

Close, with one shift. Under `[D 1.1e]`, the **logic is part of what is held fixed**. The verbs (the allowed moves) sit in the kernel next to the nouns. **Flying is the act of running those verbs** on the nouns to produce new statements. So the split is:

| | what it is | in Rudin | in Kuhn |
|---|---|---|---|
| fixed: nouns | the subject's objects | ordered field, supremum, metric space, open set | paradigm, normal science, anomaly, crisis |
| fixed: verbs | the moves allowed on them | least-upper-bound property, ε–δ, Archimedean step, compactness arguments | puzzle-solving, anomaly accumulates, crisis loosens rules, gestalt switch, incommensurability |
| fly | running the verbs on the nouns | solving the exercises, re-deriving the theorems | re-deriving each chapter's claims |
| not fixed: examples | what the book illustrates with | worked examples, counterexamples | Lavoisier, Copernicus, the Leyden jar |

The Kuhn note from 7 Oct already names the key residual: some examples are **derivable** (flying regenerates them) and some are **fitted** (the logic was read off them, and they carry grain the logic does not). The test measures that ratio.

## 3. The density hypothesis, stated as a prediction

Abstract math may be a tiny share of the training distribution, but inside that share it is dense, and the subject is close to fully determined by its axioms. Prediction: **the denser and more derivable the subject, the smaller the kernel it needs and the more of the book flying recovers.**

Ordering we expect (pre-registered, not yet tested):
1. Real analysis (Rudin): the smallest kernel relative to the book, and the highest regeneration.
2. Machine-learning theory (Shalev-Shwartz & Ben-David, *Understanding Machine Learning*): a small kernel and high regeneration on the theorems, lower on the algorithm chapters.
3. Kuhn: the smallest kernel in absolute terms, but loose regeneration. You get "a lot of action," because the claims come back while the examples (which are fitted) do not.

The kernel can't be the only source of what the flyer knows: the flyer has training. So **condition A (no kernel at all) is the baseline every number is read against**, and the out-of-sample arms below are where the claim earns or loses its keep.

## 4. Not faking the out-of-sample part

Contamination is real. Rudin's exercises and their solutions are all over the training data, so a high score on unperturbed exercises shows almost nothing. Three arms make the test bite:

1. **Perturbed axiom (the 2 Oct control).** Hand the flyer the Rudin kernel **without the least-upper-bound property** (work over ℚ). For each chapter-1 and chapter-2 result, ask whether it still holds, and why or why not. The sharpest items are the ones where *the statement survives but the book's proof dies*. Example: the Archimedean property is true in ℚ, but Rudin proves it with the least-upper-bound property. A flyer that is only retrieving gets these wrong. A flyer actually running the kernel's verbs gets them right. **This is the out-of-sample number that matters.**
2. **Renamed vocabulary.** The same kernel and exercises with every technical term swapped for a nonsense word ("supremum" becomes "plinth," "compact" becomes "sorrel"). Retrieval by surface wording breaks. The logic survives.
3. **Kernel-derivable new items.** A separate agent writes exercises that follow from the kernel but are not in the book, and a checker verifies them. These are weaker evidence, since generated items can still sit near training, but they are cheap.

## 5. Conditions per book (from the 2 Oct Rudin note, widened)

| code | the flyer sees | reads as |
|---|---|---|
| A | the item only | training alone |
| B | kernel (nouns + verbs) + item | the operator |
| C | B + canonical examples and proofs | the operator plus fitted examples |
| D | C + the flyer's own earlier outputs ("experiences") | the operator plus experiences |
| P | B with one axiom removed or altered | out of sample: perturbed |
| N | B with the vocabulary renamed | out of sample: surface wording broken |

Readouts: **B−A** (what the kernel adds over training), **C−B** (what the examples add), **D−C** (hoped to be near zero), and **P and N accuracy** (whether the flying actually runs the logic).

One more readout earns its place: **the kernel citation rate**. The flyer tags each step of its solution with the kernel item it uses (`K-12`) or with `OUT` (pulled from outside the kernel). The share of `OUT` steps measures how much of the flight came from training rather than from what was fixed.

## 6. Scope for one run (the one-shot)

Small enough to finish unattended, large enough to show a pattern:
- **Rudin**, chapters 1–2 (real and complex number systems; basic topology). All exercises, conditions A–D, P and N. This is the core.
- **Understanding Machine Learning**, chapters 2–6 (PAC learning through VC dimension). Exercises, conditions A, B, C and N.
- **Kuhn**, the whole book, regeneration only. There are no exercises, so the flyer re-derives each chapter's central claims from the kernel and a checker scores them against the text, with a separate score for the examples.

Grading: the flyer never grades itself. A separate checker agent sees the book's relevant section, the item and the answer, and scores 0, 1 or 2 with one line of reason. Where public reference solutions exist, the checker uses them.

## 7. One-shot mechanics

- **Everything is decided before the run.** The brief (`ONE_SHOT_BRIEF.md`) is the whole instruction, the run asks no questions, and every choice it might face has a stated default.
- **Roles are kept apart.** The *fixer* reads the book and writes the kernel. The *flyer* gets the kernel text inline in its prompt, never the book, and is told not to open files. The *checker* sees the book and the answer. These are three separate subagents with separate contexts, which is the per-step fix/fly exclusivity from 23 Sep put into practice.
- **Checkpoints.** Each finished arm is committed to the branch, so a crash loses at most one arm.
- **A stop rule.** If a book can't be obtained (the network blocks it, or the PDF is unreadable), that arm is recorded as skipped and the run continues.
- **One output.** A results file (tables plus residuals) and a short PDF or HTML summary.

## 8. What is still yours to rule on

1. Which machine-learning book. The default is *Understanding Machine Learning*: free, built from theorems and proofs, and with a clear kernel. The alternative is Bishop's *Pattern Recognition and Machine Learning*, which is more example-heavy and would sit between Rudin and Kuhn.
2. Whether the Kuhn arm stays in today's run or waits.
3. When to launch: today in a fresh cloud session, or later.

## 9. Residuals already visible

- The flyer's training includes all three books. Condition A measures that, P and N route around it, and nothing removes it.
- "Do not open files" is an instruction to the flyer, not a hard wall. The checker audits flyer transcripts for tool use.
- Order matters in context but not in training. The kernel's item order is held fixed across conditions, so it doesn't vary between arms.
- The density claim (math as roughly 0.01% of training but internally dense) can't be measured from here. Condition A's score stands in for coverage.
