---
description: After implementing, generate a complete reference walkthrough of the changes made — every dimension (what, how, why), anchored in the spec, plan, and diff — as a self-contained interactive HTML page in docs/walkthroughs/
argument-hint: [default: this session's work | diff | branch | PR]
---

Generate a complete reference walkthrough of the changes in the argument — the
work just completed in this session by default, or a diff/branch/PR if given.
The goal is a document the human can read end to end and come away knowing
exactly what was built and why, with nothing material left out.

## Gather the full context first

Do not walk the diff blind. Read, and use as the backbone of the explanation:

- The **diff** of all changes (the what).
- The **capability spec** and the **approved Phase 2 plan** (the intent —
  what was asked and which approach was committed).
- The **decisions** captured in Phases 1.5 and 2, including the tradeoffs (the
  *why*, which the code does not contain).
- The **lessons** and any low-confidence decisions from Phase 6.
- The **constitution** (for the domain rules the change touches).

The intent artifacts are what make this more than a code re-narration: explain
the change *against what it was supposed to do*, not in a vacuum.

When the target is work from another session (a diff, branch, or PR), the
intent artifacts aren't in this conversation: pull the plan from the **PR
description** (implement-backlog puts it there) or the **run log** under
`.claude/logs/`. If an intent artifact is genuinely unavailable, say which
dimensions lack it — do not reconstruct intent from the code and present it
as the plan.

## The bar: complete in coverage, not in granularity

Cover every dimension below — leave none out. But explain at the level of *why
and how it connects*, not line by line. If a paragraph could be replaced by
reading the code, cut it; spend the words on what the code does not say (the
reason, the constraint, the cross-file flow, the edge case). "Exhaustive" means
no dimension missing, not every line narrated. There is no length limit — let
completeness set the length.

## Structure of the document

Sections, in order (omit a section only if it genuinely does not apply, and say
so explicitly rather than skipping silently):

1. **Background** — the existing system around this change, explained from the
   code itself: broadly explore the surrounding code, don't rely only on the
   diff. Layer the depth — a skippable deeper primer for a reader new to this
   area, then the narrow background directly relevant to the change. Weigh this
   section heavier when the target is work from another session: that reader
   has none of the context this session had.
2. **What this change does** — in prose, what the feature does, stated against
   the spec. Two to four paragraphs.
3. **The core intuition** — the essence of the approach before the details,
   with a concrete example on **toy data** walked start to finish. If the
   reader gets only this section, they should still leave with the right
   mental model.
4. **Where it lives** — the map: which capabilities, modules, and files the
   change touches, and how it fits the system. Where the change begins and ends.
5. **Execution flow** — how it runs, start to finish. Entry points (request
   handler, lambda, job, event consumer — whichever applies), the call chain,
   what happens in order. This is the "how it actually runs" walk.
6. **External connections** — every integration the change uses or adds:
   - **Database:** how the connection is obtained (pool, session), the queries
     and writes, transactions and their boundaries, any migration.
   - **APIs / queues / external services:** what is called, what is consumed.
   - The guarantees assumed from each, and what happens when each is unavailable.
7. **Events** — events the change expects, emits, or consumes: who fires them,
   who listens, the ordering assumptions, and what an out-of-order or missing
   event does.
8. **Data** — the models, schemas, and transformations touched; the shape of
   what flows in and out; the contracts with other capabilities.
9. **Domain rules** — every business/normative rule implemented, with its source
   (normative id + version + scope where applicable). Decimal/rounding/audit
   handling where it appears. Tie each rule to where in the code it lives.
10. **Error handling** — every failure path: what can fail, how each failure is
    handled, recovery, rollback, idempotency, retries, what gets logged, and what
    surfaces to the caller. This section must be complete — list the paths, do
    not summarize them away.
11. **Edge cases** — the boundary and degenerate cases handled (empty, null,
    limit, large, concurrent, duplicate), and explicitly the ones treated as out
    of scope.
12. **What the tests verify** — the map from the spec's acceptance criteria to the
    tests: each test and what behavior it proves. State plainly where "tests
    pass" does and does not equal "it works".
13. **Decisions and why** — the load-bearing decisions, each with the option
    chosen, what was considered, and the tradeoff. This is the highest-value
    section: it is the reasoning that the diff threw away. Pull it from the
    Phase 1.5/2 record.
14. **Watch-outs** — debt knowingly taken, low-confidence decisions with their
    review trigger, and anything to watch as the system evolves.
15. **Quiz (do not skip)** — 5-8 multiple-choice questions of medium difficulty:
    hard enough that the reader must have understood the substance, but no
    gotchas — the goal is to help the reader confirm they actually understood.
    Each option is a click-to-reveal toggle with feedback explaining why it is
    right or wrong. Focus on the *why* and the *flow* (one or two questions per
    major section), not trivia. A walkthrough read passively builds the illusion
    of understanding, not understanding — the quiz is where that gets tested.
    Close with one line: the reader can also ask, in session, to be grilled on
    whatever they missed.

## Output format — self-contained interactive HTML

Produce a **single self-contained HTML file**: inline CSS and JS, no external
dependencies, so it opens anywhere from the repo clone.

- **Navigation:** a table of contents with anchor links; one long, responsive
  page.
- **Callouts:** styled boxes for key concepts, invariants, and edge cases.
- **Diagrams:** pick a **small number of diagram families and reuse them
  throughout** (e.g., one system-map style, one flow style, one data-shape
  style), always populated with **example data**, drawn as styled HTML/SVG —
  never ASCII art.
- **Quiz:** real toggles (click an option → reveal ✅/❌ with the explanation).
- **Self-check before finishing:** if any container uses
  `white-space: pre-wrap`, verify the generated source has no stray
  indentation rendering as accidental formatting — regenerate if it does.

Write the file to `docs/walkthroughs/YYYY-MM-DD-<feature-or-issue>.html` (the
date prefix keeps the folder time-sorted) and report the path. It is a durable
reference and, in a regulated domain, an audit artifact mapping code to spec —
keep it in the repo, not in chat. Note the chosen trade-off: GitHub's web UI
shows `.html` as source, so this artifact is read locally in a browser — the
reading experience is the point.
