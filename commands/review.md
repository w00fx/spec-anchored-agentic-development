---
description: Run the fresh-context reviewer on a diff, branch, PR, or path (report-only; context separation, not independent proof)
argument-hint: "[diff | branch | PR | path]"
---

Dispatch the `reviewer` agent via the Agent tool, in isolated context, on the
target in the argument — the working-tree diff by default, or a branch, PR
number, or path if given. Before dispatching, confirm the target resolves
and the diff is non-empty — a bad ref or an empty diff should fail here,
not inside parallel sub-agents. Do NOT review it yourself in this session: the
the fresh context that did not write the work is the point — context separation and decorrelation, not independent proof.

Default — one reviewer: instruct it to load the applicable lenses per its
own routing table (the reviewer agent carries it; do not restate the
conditions here — an inlined copy silently drifts). If an approved plan
exists for this change, paste it into the prompt for conformance's
Dimension 2; otherwise conformance covers Dimension 1 only and will say so.

**Risk and oracle strength decide which lenses are mandatory; size
only decides chunking/fan-out** (a two-line change in money or
authorization outranks 800 generated lines). When the diff exceeds
the context budget (~400 changed lines or 10 files as a local
default), dispatch three parallel single-lens reviewers — general /
constitution-compliance
(against architecture/constitution.md) / conformance (against the spec, and
the approved plan pasted into its prompt when one exists) — in ONE message,
then merge the reports: de-duplicate overlapping findings, keep the highest
severity for duplicates.

Present the findings as [BLOCKER]/[SHOULD]/[NIT] with locations and concrete
fixes. Report only — make no edits in this session unless I explicitly ask
afterwards.

Portability: this command's body works as a standalone prompt in any
harness — the semantic procedure is portable; invocation, permissions, and context loading need the harness adapter.

## No-change evidence targets

When the target is a no-change claim rather than a diff
(`kind: no-change`), the empty-diff guard does not apply — the review
corroborates the evidence target instead: expected vs observed,
authority IDs, commands + outputs, searched seams, environmental
limits, classification. Corroborate, or break the claim with the
counterexample or the seam the worker missed. Report-only, as always.
