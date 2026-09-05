"""Content for the results PDF. Design lives in make_results_pdf_lean.py.

Entries are dicts. A dict with "figure" renders an image with a numbered
caption; one with "header" renders a table. Every number is read from a
committed artifact in one of the two repositories.
"""

P1_TITLE = "CRPA: is behavioural contribution measurable at all?"
P1_APPROACH = ("Audited a partitioned-attention repository, then tested whether "
               "its own central claim survives a resolvability check.")

P1_SECTIONS = [
    dict(
        head="1.1&nbsp;&nbsp;The claim that was withdrawn",
        note="The branch reported that structural overlap does not predict "
             "behavioural contribution. Check 0 measures each edge's effect "
             "twice on disjoint halves of the evaluation split and correlates "
             "the two estimates. <b>Pooled verdict: UNRESOLVABLE.</b>",
        header=["seed", "r_delta", "r_stat", "ceiling", "observed rho",
                "delta size", "converges"],
        rows=[["42", "+0.088", "+0.119", "0.102", "+0.018", "6.0 ULP", "no"],
              ["1337", "-0.026", "+0.255", "0.000", "-0.017", "5.0 ULP", "no"],
              ["2024", "+0.012", "+0.250", "0.054", "+0.013", "4.0 ULP", "no"]],
        widths=[.12, .13, .13, .13, .17, .16, .16],
        aligns=["l", "r", "r", "r", "r", "r", "l"]),
    dict(
        figure="f1_check0.png", width=.80,
        caption="Figure 1. Observed correlation against the ceiling that "
                "measurement unreliability imposes on it, "
                "sqrt(r_delta &times; r_stat). Every observed value sits far "
                "inside its own ceiling, so a real decoupling and measured "
                "noise cannot be told apart. Seed 1337 has no bar: its "
                "split-half reliability is negative, so the ceiling "
                "degenerates to zero and that seed carries no information at "
                "all. n = 3 seeds, 1,044 to 1,152 scored edges each."),
    dict(
        head="1.2&nbsp;&nbsp;The floor holds across three orders of magnitude",
        note="The replacement claim is that single-edge contribution is not "
             "resolvable, not that overlap fails to predict it.",
        header=["scale", "precision", "single-edge delta"],
        rows=[["12.4M  (Tier 1)", "float32",
               "4 to 6 ULP, split-half reliability 0.088"],
              ["138M  (Tier 2)", "float32",
               "single-edge p90 0 ULP; group of 24 is 1 ULP"],
              ["<b>6.9B  (Tier 3)</b>", "<b>bfloat16</b>",
               "<b>exactly 0.000e+00 across 192 edges</b>"]],
        widths=[.26, .18, .56],
        aligns=["l", "l", "l"],
        band=(2,)),
    dict(
        figure="f2_floor.png", width=.74,
        caption="Figure 2. Typical single-edge intervention effect, expressed "
                "in units of the least representable step at the working "
                "precision. At 138M the single-edge p90 is zero; removing all "
                "24 candidates together moves the loss by one ULP. At 6.9B "
                "the single-edge effect is exactly zero: "
                "the edit shifts logits by 2.58, 3.05 and 0.127 at layers 0, "
                "16 and 31, and the loss is bit-identical to baseline for all "
                "192 edges. A criterion thresholding this quantity is "
                "unfalsifiable at every scale tested."),
    dict(
        head="1.3&nbsp;&nbsp;Reproduction of the published table",
        note="Re-run from the original commit. Four of five rows come back. "
             "The one that does not is the one the paper's claim rests on.",
        header=["Variant", "Published", "Reproduced", "Verdict"],
        rows=[["Dense Transformer", "50.9%", "55.6%", "reproduces"],
              ["Sliding Window", "51.9%", "52.5%", "reproduces"],
              ["CRPA no regularisation", "8.4%", "10.9%", "reproduces"],
              ["CRPA naive regularisation", "5.3%", "5.3%", "reproduces exactly"],
              ["<b>CRPA causal regularisation</b>", "<b>32.8%</b>",
               "<b>7.5%</b>", "<b>does not reproduce</b>"]],
        widths=[.40, .16, .16, .28],
        aligns=["l", "r", "r", "l"],
        band=(4,)),
    dict(
        head="1.4&nbsp;&nbsp;Three seeds against a measured chance floor",
        note="The floor is measured by simulating the task generator, not "
             "asserted from vocabulary size: 52.78% (sd 0.08, n = 25,000 x 5). "
             "<b>No variant clears it, dense included.</b> The retrieval task "
             "cannot discriminate between these variants.",
        header=["Variant", "Retrieval", "t vs floor", "Verdict", "Overlap"],
        rows=[["dense", "53.6%", "+0.8", "indistinguishable", "0.403"],
              ["sliding window", "47.2%", "-1.4", "indistinguishable", "0.322"],
              ["crpa_noreg", "4.4%", "-66", "below", "0.244"],
              ["crpa_naive", "4.6%", "-100", "below", "0.264"],
              ["crpa_contribution", "4.3%", "-50", "below", "0.222"]],
        widths=[.26, .14, .14, .28, .18],
        aligns=["l", "r", "r", "l", "r"]),
    dict(
        head="1.5&nbsp;&nbsp;Long context: the wall was in the diagnostic",
        note="A fused dense kernel is faster than the sparse gather path at "
             "every length benchmarked, with the gap narrowing as context "
             "grows. The benchmark itself was not run beyond 16k.",
        header=["Context", "Dense", "Sliding", "CRPA", "CRPA vs dense",
                "Peak memory"],
        rows=[["4,096", "13.2 ms", "19.5 ms", "31.5 ms", "2.40x slower", "737 MB"],
              ["8,192", "30.0 ms", "62.4 ms", "60.1 ms", "2.00x slower", "1,181 MB"],
              ["16,384", "72.0 ms", "218.1 ms", "119.1 ms", "1.65x slower", "2,067 MB"]],
        widths=[.13, .13, .14, .13, .24, .23],
        aligns=["r", "r", "r", "r", "c", "r"]),
    dict(
        head="1.6&nbsp;&nbsp;32k and 64k, previously unreachable, now measured",
        note="Six attempts on 48GB and 80GB cards had all exhausted memory. "
             "The cost was never in the model: bounding the candidate-edge "
             "diagnostic closed both lengths on the same hardware.",
        header=["Context", "Peak before", "Peak after", "Retrieval",
                "Realized overlap", "Largest single-edge delta"],
        rows=[["4,096", "14.14 GB", "0.75 GB", "0.0%", "0.2265", "9.54e-07"],
              ["8,192", "27.74 GB", "1.15 GB", "0.0%", "0.2256", "9.54e-07"],
              ["16,384", "55.04 GB", "1.24 GB", "0.0%", "0.2297", "1.91e-06"],
              ["32,768", "<i>out of memory</i>", "1.93 GB", "0.0%", "0.2308",
               "9.54e-07"],
              ["65,536", "<i>out of memory</i>", "3.30 GB", "0.0%", "0.2302",
               "9.54e-07"]],
        widths=[.13, .17, .15, .13, .19, .23],
        aligns=["r", "r", "r", "r", "r", "r"],
        band=(3, 4),
        after="The measurement extends the central claim rather than "
              "complicating it. The largest single-edge delta is "
              "<b>9.5367e-07 at four of the five lengths, exactly one unit "
              "in the last place</b>, and two at 16,384, against a float32 "
              "resolution of 1.32e-06. Single-edge behavioural contribution "
              "sits at the measurability floor across a sixteenfold range of "
              "context, not only at the short lengths where it was first "
              "seen. All five rows come from one implementation at one chunk "
              "size, so the memory column compares like with like."),
    dict(
        figure="f9_bounded.png", width=.86,
        caption="Figure 3. Peak memory of the candidate-edge diagnostic "
                "before and after bounding it. The unbounded implementation "
                "grew at 3.45 GB per 1,000 tokens and a linear fit to its "
                "three measured points predicts 110 GB at 32k and 219 GB at "
                "64k, both beyond the 80GB card. Streaming the overlap "
                "measurement by layer, disabling autograd in the group "
                "diagnostic and scoring edges in small chunks flattens the "
                "profile to 0.75-3.30 GB across the whole range, a 44x "
                "reduction at 16k. n = 1 seed, "
                "138M parameters, bfloat16."),
    dict(
        figure="f8_cost.png", width=.90,
        caption="Figure 4. Measured forward latency and peak allocated "
                "memory at the three lengths the latency benchmark was run "
                "at. A fused dense kernel is faster than the sparse gather "
                "path at every one, and the gap narrows from 2.40x to 1.65x "
                "as context grows, so the sparse path is closing but has not "
                "overtaken it by 16k. The shaded region marks lengths not "
                "benchmarked for latency; the diagnostic does now run there, "
                "as section 1.6 reports. Batch size 1, bfloat16, 138M "
                "parameters, median of 10 iterations after 5 warmups."),
    dict(
        head="1.7&nbsp;&nbsp;Defects found and repaired",
        note="Each of these changed a reported number.",
        header=["Defect", "Consequence"],
        rows=[["Central claim unsupported by its own measurement",
               "A decoupling claim the data cannot support. Withdrawn"],
              ["Chance floor asserted, not measured",
               "Real floor 52.78%, not 5.0%. Every above-chance verdict inverted"],
              ["Intervention masked a query-row pair, not a query-to-key edge",
               "The measured object was not the object being reasoned about"],
              ["Roughly half of all interventions were causally inert",
               "Delta zero by construction, so the pair was filed redundant"],
              ["Short runs recordable as completed measurements",
               "Nine 3-iteration runs entered an aggregate and moved it by 26x"],
              ["Auxiliary routing entropy pinned at ln(4)",
               "A constant reported as a finding"]],
        widths=[.46, .54],
        aligns=["l", "l"]),
]

P2_TITLE = "xsa-controls: sanity checks for attention surgery"
P2_APPROACH = ("Three checks shipped as importable code: is the measurement "
               "resolvable, does the statistic beat an anisotropy null, and "
               "does a matched arbitrary intervention recover the gain?")

P2_SECTIONS = [
    dict(
        head="2.1&nbsp;&nbsp;Check 1 across a nine-model scale ladder",
        note="5,408 head-level rows, 32 real documents per model, eager "
             "attention, null partner drawn within the sequence from positions "
             "the query could causally attend.",
        header=["model", "params", "cos_self", "cos_null", "excess",
                "% self-specific"],
        rows=[["gpt2", "124M", "0.4828", "0.2987", "0.1840", "38.1"],
              ["pythia-160m", "160M", "0.4180", "0.2637", "0.1544", "36.9"],
              ["gpt2-medium", "355M", "0.4252", "0.2579", "0.1674", "39.4"],
              ["pythia-410m", "410M", "0.4022", "0.1937", "0.2086", "51.9"],
              ["gpt2-large", "774M", "0.4213", "0.2117", "0.2096", "49.7"],
              ["pythia-1.4b", "1.4B", "0.3862", "0.1900", "0.1963", "50.8"],
              ["gpt2-xl", "1.5B", "0.3861", "0.2069", "0.1792", "46.4"],
              ["pythia-2.8b", "2.8B", "0.3565", "0.1859", "0.1705", "47.8"],
              ["<b>pythia-6.9b</b>", "<b>6.9B</b>", "<b>0.3404</b>",
               "<b>0.1979</b>", "<b>0.1425</b>", "<b>41.9</b>"]],
        widths=[.26, .13, .15, .15, .14, .17],
        aligns=["l", "r", "r", "r", "r", "r"],
        band=(8,)),
    dict(
        figure="f3_ladder.png", width=.80,
        caption="Figure 5. The anisotropy null weakens with scale but does not "
                "vanish. cos_null falls from 0.2637 at 160M to 0.1979 at 6.9B, "
                "yet 58% of the raw statistic is still explained by the null "
                "at 6.9B, and about half across the shaded range where the "
                "method was actually trained. This answers the strongest "
                "objection to the framing, that large models are isotropic, "
                "with measurement rather than extrapolation. n = 9 models, "
                "5,408 heads."),
    dict(
        head="2.2&nbsp;&nbsp;The null depends on where it is measured",
        note="The same model and corpus, measured at five context lengths.",
        header=["Context length", "64", "128", "256", "512", "1024"],
        rows=[["cos(y, v) observed", "0.4900", "0.4846", "0.4812", "0.4772",
               "0.4743"],
              ["cos(y, v') null", "0.3747", "0.3361", "0.3096", "0.2904",
               "0.2788"],
              ["<b>self-specific share</b>", "<b>23.5%</b>", "30.7%", "35.7%",
               "39.2%", "<b>41.2%</b>"]],
        widths=[.30, .14, .14, .14, .14, .14],
        aligns=["l", "r", "r", "r", "r", "r"],
        bold=(2,)),
    dict(
        figure="f4_length.png", width=.88,
        caption="Figure 6. The observed statistic is nearly flat across a "
                "sixteenfold change in context length while the null moves by "
                "a third, so the self-specific share swings from 23.5% to "
                "41.2%. A claim of the form &ldquo;only N% of this statistic is "
                "self-specific&rdquo; is therefore a property of the measurement "
                "context as much as of the model, and Check 1 must always be "
                "reported with the length it was measured at. n = 24 documents "
                "per length, GPT-2."),
    dict(
        head="2.3&nbsp;&nbsp;Grouped-query attention, which nobody had checked",
        note="Under GQA several query heads share one KV head, so the token's "
             "own value vector is shared across a group. The source method's "
             "own table reports no KV-head count.",
        header=["model", "query / KV heads", "within-group excess",
                "across-group excess"],
        rows=[["Qwen2.5-0.5B", "14 / 2", "<b>+0.2415</b>", "<b>-0.1876</b>"],
              ["Qwen2.5-1.5B", "12 / 2", "<b>+0.2731</b>", "<b>-0.1922</b>"],
              ["TinyLlama-1.1B", "32 / 4", "<b>+0.2373</b>", "<b>-0.1126</b>"]],
        widths=[.26, .20, .27, .27],
        aligns=["l", "r", "r", "r"]),
    dict(
        figure="f5_gqa.png", width=.72,
        caption="Figure 7. Borrowing a neighbouring KV group's value at the "
                "same position does not merely lose the effect, it reverses "
                "it. The self-value direction is specific to the head's own "
                "group. GQA models also show a higher self-specific share, 56 "
                "to 68%, than any multi-head model on the ladder, 37 to 52%, "
                "so grouped-query attention is not a neutral change of "
                "variable for this family of methods. The sign replicates "
                "outside the Qwen family: TinyLlama-1.1B is a Llama "
                "architecture with a different group ratio and its "
                "across-group excess is also negative. The magnitude is about "
                "40% smaller, so the sign generalises and the size does not. "
                "n = 3 models across 2 families, 1,376 heads."),
    dict(
        head="2.4&nbsp;&nbsp;Does the statistic predict its own intervention?",
        note="Each head's self-value is removed in a frozen model and the "
             "change in loss measured twice, on disjoint halves of the "
             "evaluation documents. Nothing is reported until A &times; V "
             "rebuilds the model's own attention output.",
        header=["model", "statistic", "raw rho", "split-half r", "ceiling",
                "disattenuated", "verdict"],
        rows=[["gpt2", "cos(y, v)", "<b>+0.469</b>", "+0.799", "0.892",
               "<b>+0.526</b>", "reliable"],
              ["gpt2", "excess", "+0.236", "+0.799", "0.892", "+0.264",
               "reliable"],
              ["pythia-160m", "cos(y, v)", "<b>+0.014</b>", "+0.473", "0.686",
               "+0.020", "attenuated"],
              ["pythia-160m", "excess", "<b>+0.487</b>", "+0.473", "0.686",
               "<b>+0.710</b>", "attenuated"],
              ["pythia-410m", "cos(y, v)", "<b>+0.099</b>", "+0.435", "0.657",
               "+0.150", "attenuated"],
              ["pythia-410m", "excess", "<b>+0.216</b>", "+0.435", "0.657",
               "<b>+0.328</b>", "attenuated"]],
        widths=[.16, .13, .12, .14, .12, .16, .17],
        aligns=["l", "l", "r", "r", "r", "r", "l"],
        band=(2, 3),
        after="In both Pythia models the raw self-value cosine, the quantity "
              "the method is motivated by, carries <b>essentially no "
              "information</b> about the measured effect of removing it, "
              "while the null-corrected excess predicts it. <b>In GPT-2 the "
              "ordering reverses.</b> Two models agreeing and a third "
              "disagreeing is not a law, so the claim is the narrow one: "
              "whether a raw statistic predicts its own intervention is "
              "model-dependent."),
    dict(
        head="2.4.1&nbsp;&nbsp;The first version of that table did not reproduce",
        note="The same experiment was run three times: twice at 24 evaluation "
             "documents per half and once at 64, on two different GPUs under "
             "two different PyTorch and transformers versions.",
        header=["quantity", "run 1 (n=24)", "run 2 (n=24)", "run 3 (n=64)",
                "verdict moved?"],
        rows=[["gpt2 r_delta", "+0.752", "+0.629", "<b>+0.799</b>",
               "no, reliable throughout"],
              ["pythia-160m r_delta", "+0.304", "+0.194", "<b>+0.473</b>",
               "<b>yes</b>"],
              ["pythia-410m r_delta", "+0.446", "-0.007", "<b>+0.435</b>",
               "<b>yes</b>"],
              ["gpt2 cos(y,v) <i>disattenuated</i>", "+0.521", "+0.527",
               "<b>+0.526</b>", "no"]],
        widths=[.28, .16, .16, .16, .24],
        aligns=["l", "r", "r", "r", "l"],
        band=(3,),
        after="At 24 documents per half the reliability estimate for the two "
              "Pythia models is <b>not stable</b>. Repeating the run moved "
              "pythia-410m's from +0.446 to -0.007, taking the verdict from "
              "attenuated to unresolvable, and the correlations followed it "
              "down. Any statement built on the first run's Pythia numbers "
              "would not have survived a reviewer repeating the "
              "measurement.<br/><br/>"
              "At 64 documents per half both models are stable, +0.473 and "
              "+0.435, and the pattern the first run showed returns. That is "
              "the run reported above. Both smaller runs are kept in the "
              "repository rather than discarded, because the disagreement is "
              "more informative than either alone.<br/><br/>"
              "<b>The last row is the argument for disattenuation, and it "
              "makes that argument better than any reasoning could.</b> "
              "GPT-2's raw correlation moved across these runs, from +0.450 "
              "to +0.469. Its disattenuated value did not: +0.521, +0.527, "
              "+0.526. Disattenuation divides out precisely the reliability "
              "that moved, so what is left is stable across budgets, GPUs "
              "and library versions.<br/><br/>"
              "This is Check 0 catching a claim in our own work, for the "
              "second time in this project. An effect that is not reliably "
              "measurable produced a correlation that did not survive being "
              "measured again."),
    dict(
        head="2.4.2&nbsp;&nbsp;Why this disagrees with the prior figure by 10x",
        note="The specification quotes prior GPT-2 values for exactly this "
             "correlation. Our GPT-2 number is an order of magnitude larger, "
             "so the gap has to be explained rather than left for a reader "
             "to find.",
        header=["statistic", "prior value", "measured here", "ratio"],
        rows=[["cos(y, v)", "0.043", "<b>+0.469</b>", "10.9x"],
              ["excess", "0.017", "+0.236", "13.9x"],
              ["a_ii", "-0.021", "<i>not measured</i>", "&ndash;"]],
        widths=[.28, .24, .26, .22],
        aligns=["l", "r", "r", "r"],
        after="The prior values were measured on <b>one paragraph repeated "
              "two hundred times</b> &mdash; base loss 0.76 nats against 3.96 "
              "for real prose. The specification's own bug list flags that "
              "input as a defect to fix before porting anything.<br/><br/>"
              "The reason it matters here is specific rather than general. "
              "<b>A correlation across heads needs variation across heads.</b> "
              "One paragraph repeated gives a model very little to do "
              "differently in different heads, so the per-head effects it "
              "produces are small and largely undifferentiated, and "
              "correlating them against anything returns approximately zero. "
              "Near-zero on that input is a property of the input, not of the "
              "method.<br/><br/>"
              "Measured on 64 real wikitext-103 documents per half, with "
              "disjoint halves and the reliability of the effect established "
              "first, the same correlation is <b>+0.469 with a ceiling of "
              "0.892</b>. The prior figures are superseded rather than "
              "contradicted: they are not measurements of the quantity they "
              "appear to describe. Taken at face value they would have said "
              "the motivating statistic is unrelated to where the "
              "intervention helps, on every statistic and every model, which "
              "is the opposite of what GPT-2 shows and only half of what "
              "Pythia shows."),
    dict(
        figure="f10_a2.png", width=.86,
        caption="Figure 8. Correlation between each per-head statistic and "
                "the measured effect of removing that head's self-value. "
                "Dashed lines mark the ceiling that split-half unreliability "
                "places on any observable correlation, sqrt(r_delta &times; "
                "r_stat); every bar sits below its own ceiling, which is what "
                "makes the comparison legitimate. This is the check that "
                "returned UNRESOLVABLE on the sibling CRPA project: here the "
                "effect is resolvable, so the correlation can be read. "
                "n = 3 models, 144 to 384 heads each."),
    dict(
        head="2.5&nbsp;&nbsp;The matched intervention (underpowered pilot)",
        note="24 cells, 3 arms x 8 seeds, identical initialisation and data "
             "order per seed. Measured step-0 deviation across all five arms "
             "is 0.000e+00, so the arms start from a common point. This ran "
             "at 5e7 tokens per run, outside the pre-registered [3.5e8, 6e8] "
             "band, and is reported as the underpowered pilot; the primary "
             "endpoint is section 2.6.",
        header=["arm", "mean delta vs baseline", "95% CI", "t", "p", "n"],
        rows=[["<b>random</b>  (primary)", "<b>+0.001190</b>",
               "[+0.000351, +0.002040]", "+2.48", "<b>0.042</b>", "8"],
              ["xsa", "+0.001515", "[-0.001223, +0.004807]", "+0.92", "0.387",
               "8"]],
        widths=[.20, .24, .26, .10, .10, .10],
        aligns=["l", "r", "r", "r", "r", "r"]),
    dict(
        figure="f6_paired.png", width=.88,
        caption="Figure 9. Both arms fall inside the shaded band of effects "
                "the design cannot resolve. The minimum detectable effect is "
                "0.00518 nats against the 0.00076 the method's own independent "
                "replication reports, so the study is underpowered about "
                "sevenfold and cannot settle the question in either direction. "
                "The two arms are also indistinguishable from each other, "
                "which is what Check 2 asks. Reported as a power failure, not "
                "as a null result. n = 8 seeds per arm."),
    dict(
        head="2.6&nbsp;&nbsp;The primary endpoint, registered and running",
        note="The pilot above was void as a primary endpoint because it ran "
             "outside the pre-registered band. Re-running it properly was "
             "blocked by a cost projection that turned out to be measuring "
             "the wrong thing.",
        header=["arm", "measured throughput", "hours for 8 runs", "at $0.74/hr"],
        rows=[["baseline", "176,467 tok/s", "5.04", "$3.73"],
              ["xsa", "159,358 tok/s", "5.58", "$4.13"],
              ["random", "166,267 tok/s", "5.35", "$3.96"],
              ["<b>total, 24 cells</b>", "&ndash;", "<b>15.96</b>",
               "<b>$11.81</b>"]],
        widths=[.26, .26, .24, .24],
        aligns=["l", "r", "r", "r"],
        band=(3,),
        after="The committed calibration projected <b>$24.01</b> for this "
              "design, which scaled to the registered budget is about $27 and "
              "breaches a $20 ceiling. That figure is solved from "
              "<b>diagmask's</b> throughput of 71,918 tok/s, because diagmask "
              "is the slowest of the five arms and the solver sizes the whole "
              "design against its worst case. Diagmask is not in this run. "
              "Measured on the card that would run them, the three arms "
              "present are between 159,000 and 176,000 tok/s, roughly "
              "2.3x faster, and the real projection is <b>$11.81</b>. "
              "Substituting the slowest arm's throughput for arms twice as "
              "fast would have blocked a run that fits with $8 to spare."),
    dict(
        head="2.7&nbsp;&nbsp;What was registered, and what was dropped",
        note="Registered in the budget ledger before the run started, not "
             "after it finished.",
        header=["item", "value"],
        rows=[["configuration", "CFG_S, arms baseline / xsa / random"],
              ["seeds", "42, 1337, 2024, 7, 99, 512, 8191, 31337"],
              ["tokens per run", "399,900,672"],
              ["inside pre-registered band", "yes, [3.5e8, 6e8]"],
              ["batch aligned", "yes, 131,072 x 3,051"],
              ["primary endpoint", "random vs baseline; Holm over "
                                   "secondaries only"],
              ["CFG_M scale check", "<i>dropped for budget</i>"]],
        widths=[.34, .66],
        aligns=["l", "l"],
        band=(6,),
        after="<b>CFG_M is dropped, with the arithmetic rather than a "
              "shrug.</b> At CFG_M the measured diagmask slowdown is 2.336 "
              "and the same calibration projects $51.57 for 24 runs at the "
              "lower budget, about $59 at the registered one. Even applying "
              "the same throughput correction as above, the floor sits well "
              "beyond $20. Dropping it follows the specification's own "
              "pre-registered priority order, which cuts the CFG_M scale "
              "check first and the secondary arms second. It is recorded as "
              "dropped for budget, which is its sanctioned status, not as an "
              "oversight."),
    dict(
        head="2.8&nbsp;&nbsp;The checklist discriminates between methods",
        note="Check 1 applied to two further methods on frozen GPT-2, each "
             "with a null matched to the structure the statistic inherits for "
             "free.",
        header=["method", "statistic", "null", "excess", "% self-specific",
                "survives"],
        rows=[["attention sinks", "0.4028", "0.0034", "0.3994", "99.2", "yes"],
              ["massive activations", "12.8719", "3.6452", "9.2266", "71.7",
               "yes"],
              ["self-value (this work, 6.9B)", "0.3404", "0.1979", "0.1425",
               "41.9", "no"]],
        widths=[.28, .16, .13, .14, .17, .12],
        aligns=["l", "r", "r", "r", "r", "l"],
        band=(2,)),
    dict(
        figure="f7_generality.png", width=.72,
        caption="Figure 10. Attention sinks retain 99.2% of their statistic "
                "after a null matched for recency, and massive activations "
                "71.7% against the maximum expected from a matched-variance "
                "Gaussian. The self-value statistic retains 41.9%. The "
                "checklist separates methods rather than debunking all of "
                "them, which is a stronger position than a blanket null."),
    dict(
        head="2.9&nbsp;&nbsp;A reproduction left failing on purpose",
        note="Published GPT-2 reference: cos_self 0.5406, cos_null 0.3798, "
             "excess 0.1608. Thirteen measurement conventions were tested and "
             "the full grid is reported unselected.",
        header=["convention varied", "range of cos_self observed",
                "reproduces reference"],
        rows=[["sequence length, 64 to 1024", "0.4827 to 0.4955", "no"],
              ["position 0 included", "0.4847", "no"],
              ["null partner definition, 3 variants", "0.4832", "no"],
              ["head pooling", "0.4832", "no"],
              ["layer subsets, 4 variants", "0.4405 to 0.6494", "no"]],
        widths=[.42, .32, .26],
        aligns=["l", "r", "l"],
        after="<b>No tested convention reproduces the reference.</b> Layer "
              "subsets move the statistic most, so a subset is the likeliest "
              "remaining explanation, but no tested subset lands on the reference triple. "
              "Reported as unexplained rather than resolved by further search: "
              "selecting the setting that hits a target and presenting it as "
              "the method is the practice this work argues against."),
    dict(
        head="2.10&nbsp;&nbsp;Defects found only by running it on GPU",
        note="These defects were not visible from CPU testing.",
        header=["Defect", "Consequence"],
        rows=[["diagmask crashed on every GPU run",
               "bf16 autocast dtype mismatch. One of five arms could never have run"],
              ["Calibration output was never consumed",
               "The factorial used a default budget, so the gate changed nothing"],
              ["Budget clamped up to an unaffordable floor",
               "Returned a plan that could not be paid for and called it fine"],
              ["The spend threshold was never enforced",
               "Defined in config, referenced nowhere"],
              ["Two runs mixed token budgets in one directory",
               "Caught by a guard ported from the sibling project; data discarded"]],
        widths=[.42, .58],
        aligns=["l", "l"]),
]

CLOSING = dict(
    head="Status, and what remains open",
    note="Both deliverables carry green CI. No compute is running.",
    header=["", "CRPA", "xsa-controls"],
    rows=[["Tests", "266 passing", "202 passing"],
          ["Coverage", "83%", "90%"],
          ["Figures from real data", "7 of 7", "5 of 5"],
          ["Compute used", "A6000, RTX 6000 Ada, A100 80GB",
           "RTX 6000 Ada, A100 80GB"],
          ["Open item", "long context at 32k and 64k",
           "GPT-2 reference reproduction"],
          ["Why it is open", "proven memory wall over five attempts",
           "thirteen conventions tested; no convention matches"]],
    widths=[.24, .38, .38],
    aligns=["l", "l", "l"])
