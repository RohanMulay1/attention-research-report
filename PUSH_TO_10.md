# Current scores and the work that would close them

Scores as assessed 2026-09-03/04, against each project's original requirements.

| Deliverable | Completion | Quality | What holds it below 10 |
|---|---|---|---|
| CRPA | **10** | 9.5 | closed 2026-09-05: Tier 2 at 32k/64k now measured |
| xsa-controls | **9.5** | 9.5 | CFG_M factorial still unrun (~51 GPU-h of wall clock, not money) |
| Report | 9.0 | 9.0 | No test suite, no CI, committed figures can silently drift from source data |

**Updated 2026-09-05.** CRPA's last open item closed by bounding the
candidate-edge diagnostic rather than by finding a larger GPU: peak memory at
16k fell from 55.04 GB to 1.24 GB and both previously unreachable lengths now
run. xsa-controls gained A2a/A2 (the effect is resolvable; the raw statistic
fails to predict it in two models of three), a second GQA family, and the six
paper artifacts. What remains is the CFG_M factorial.

None of the open items is a gap left out of laziness. Each has a recorded
reason, and two of them are open *because* closing them the easy way would
require dishonesty. Read the reason before attempting a fix.

---

## The prompt

Paste this to the agent doing the work.

---

You are the lead ML research engineer on three linked deliverables:

1. `~/crpa` — branch `feat/evidence-scaling`, PR #1 into `ishaannk/crpa`
2. `~/xsa-controls` — branch `feat/sanity-checks-harness-and-day1-gate`
3. `~/attention-research-report` — builds the combined results PDF

Current scores: CRPA 9.5/10 completion and 9.5/10 quality; xsa-controls 8.5/10
and 9.5/10; the report 9.0/10 and 9.0/10. Your task is to close the remaining
gaps and reach 10/10 on all three.

**Read `QA_CHECKLIST.md` in the report repo first and run it end to end. Fix
anything it fails before starting new work.** Report the results as PASS / FAIL
/ NOT RUN with command output for anything that is not a PASS.

### Integrity constraints, which outrank the score

These are not style preferences. Two of the open items exist because the
obvious fix would violate them, and a previous pass raised this work's quality
specifically by *withdrawing* a claim.

- Never manufacture significance and never cherry-pick a favourable run.
- Never tune a measurement toward an expected answer. If you search a
  configuration space and one setting happens to match a published reference,
  reporting that setting as "the method" is the exact practice this work
  criticises. Report the whole grid, unselected.
- Never convert a failure into a number. An out-of-memory run is `oom`, not an
  extrapolated value, and must not appear in any table or figure.
- Never average across differing training budgets. Both repos have a guard;
  keep it on the aggregation path.
- If evidence is insufficient, downgrade the conclusion explicitly rather than
  softening the language. A power failure is a power failure, not a null result.
- If a fix would require weakening one of these, stop and report that the item
  cannot be closed honestly. **"Cannot be closed honestly, here is why" is a
  10/10 answer for that item.** A documented impossibility scores higher than a
  fabricated success.

### CRPA: the one open item

Tier 2 at 32,768 and 65,536 tokens. Five attempts all hit OOM, including on an
idle A100 80GB at the correct 138M profile with batch size 1 and adaptive
chunking. The investigation established that a forward pass at 32k costs only
1.90 GB peak, so the model scales fine and the cost is in the candidate-edge
diagnostic, not in inference.

Close it by either:

- **(a)** Making the diagnostic memory-bounded so the lengths actually run:
  stream candidate edges instead of materialising them, chunk the scoring pass,
  and reduce to statistics immediately. If this works, the requirement is met
  with real numbers. Verify peak memory is measured, not projected.
- **(b)** Deriving the wall analytically: a memory model, in code, that predicts
  the observed peak at 4k/8k/16k within a stated tolerance and then shows 32k
  exceeds 80 GB by construction. That converts "we could not" into "it cannot",
  which closes the requirement.

Do not close it by lowering the profile, shrinking the candidate set until it
fits, or reporting a partial diagnostic as if it were the full one.

### xsa-controls: three open items

- **CFG_M factorial (Days 4-6, currently 4/5).** The budget solver dropped it in
  the spec's pre-registered priority order, which is its sanctioned status. An
  out-of-band attempt was abandoned when the budget-homogeneity guard caught two
  invocations mixing 3e7 and 5e7 tokens in one results directory; that data was
  deleted. To close: run it cleanly at a single token budget, with the guard
  active, within the cost ceiling, and confirm the Days 4-6 gate's identical
  `tokens_seen` per seed check passes. If the ceiling will not permit it, say so
  with the arithmetic and leave it not run.
- **GPT-2 Check-1 reference (Day 7, currently 3/4).** Measured 0.4828 / 0.2987 /
  0.1840 against the published 0.5406 / 0.3798 / 0.1608. Thirteen conventions
  were tested and none reproduces it within +/-0.01. Layer subsets move
  `cos_self` most (0.4405 to 0.6494), so a subset is the likeliest remaining
  explanation. You may extend the search, but you must report the full grid
  unselected. **Finding a matching configuration is not by itself a pass** —
  you must give an independent reason that configuration is the right one.
  Otherwise leave it failing and documented.
- **A6 methods 3 and 4.** Value-residual needs a matched-capacity control, which
  means training two models rather than probing one frozen model. Registers are
  a vision-transformer construct outside a causal-LM harness. Both are recorded
  in `NOT_IMPLEMENTED` with those reasons and the spec's guidance is two
  minimum, which is already met. Implement only if you can do so without a
  confound; otherwise confirm the reasons still hold.

### Report: raise it to 10

- Add a test suite that verifies the **rendered** PDF, not the source: page
  count, embedded image count, one caption per figure in order, absence of
  unrendered markup and placeholder values, uniform section spacing measured
  from the drawn rules, and no page under 60% fill except the last.
- Add a check that every figure's source data file exists and that
  `report_figs.py` contains no hand-entered measurement beyond the one
  documented literal.
- Add CI running that suite plus a clean-clone build.
- Consider generating the figures at build time from the source repos when
  present, so committed PNGs cannot silently drift from the data.

### Definition of done

- All three QA checklists pass, or every failure has a recorded reason.
- Tests and coverage at or above current levels: CRPA 266 tests / 83%,
  xsa-controls 202 tests / 90%, report suite new.
- `pyflakes` clean, CI green, working trees clean and pushed.
- No compute left running; confirm explicitly.
- Update each repo's `FINAL_STATUS.md` with the new score, what changed, and
  what remains open with its reason.
- State plainly which items you closed with results, which you closed as proven
  impossible, and which you left open. Do not report a score you cannot
  evidence.
