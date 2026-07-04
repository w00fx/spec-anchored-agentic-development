---
description: Run the independent reviewer on a diff, branch, PR, or path (report-only)
argument-hint: [diff | branch | PR | path]
---

Dispatch the `reviewer` agent via the Task tool, in isolated context, on the
target in the argument — the working-tree diff by default, or a branch, PR
number, or path if given. Do NOT review it yourself in this session: the
independence of a fresh context that did not write the work is the point.

Default — one reviewer: instruct it to load the applicable lenses per its
own routing table (the reviewer agent carries it; do not restate the
conditions here — an inlined copy silently drifts). If an approved plan
exists for this change, paste it into the prompt for conformance's
Dimension 2; otherwise conformance covers Dimension 1 only and will say so.

If the diff exceeds roughly 400 changed lines or 10 files, dispatch three
parallel single-lens reviewers instead — general / constitution-compliance
(against architecture/constitution.md) / conformance (against the spec, and
the approved plan pasted into its prompt when one exists) — in ONE message,
then merge the reports: de-duplicate overlapping findings, keep the highest
severity for duplicates.

Present the findings as [BLOCKER]/[SHOULD]/[NIT] with locations and concrete
fixes. Report only — make no edits in this session unless I explicitly ask
afterwards.
