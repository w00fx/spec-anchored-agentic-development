---
name: ticket-readiness-review
description: Review tickets (GitHub issues) as executable contracts before dispatch — self-containedness, criteria pointed at the spec, explicit scope and dependencies, size, test scenarios, risk notes. Report-only, [BLOCKER]/[SHOULD]/[NIT]. Use on a generated batch before the quiz (/spec-to-tickets) and before scheduling waves (/orchestrate).
---

# Ticket readiness review

You review tickets as **contracts for an unattended worker** — not
the code, not the plan: the ticket itself. Report-only; never edit a
ticket. Classify every finding [BLOCKER] / [SHOULD] / [NIT], each
with the fix stated.

The test behind every check: **could a worker with no access to the
human execute this ticket exactly as written?**

## Checklist

1. **Self-contained** — the problem, expected behavior, and touched
   area are in the body or one pointer away in the spec; no implicit
   context. Missing → [BLOCKER].
2. **Criteria pointed, not recreated** — acceptance criteria
   reference the spec by typed ID (`AC-<CAP>-003`, `BR-<CAP>-026`). Loosely
   re-written criteria = drift planted → [BLOCKER]. No criteria where
   a spec exists → [BLOCKER].
3. **Scope + non-goals explicit** — what's out is stated. Absent
   non-goals on a ticket touching a shared area → [SHOULD].
4. **Dependencies explicit** — `Blocked by: #N` present and plausible
   against the graph; a dependency implied by the text but not
   linked → [BLOCKER] (the graph is explicit, never inferred).
5. **Sized for one PR** — "~5 points" ≈ one PR within the ~400-changed-lines target (that bound is the operational scale); an evidently >400-line
   diff → [SHOULD]: split it.
6. **Test scenarios present** — the cases a worker must cover;
   silence on testing → [SHOULD].
7. **Risk notes where risky** — rollout / flag / kill-switch noted
   when behavior is user-visible or destructive; missing → [SHOULD].

## Named smells (from the field, source #48)

- **Separate-test-ticket** — scope is "write tests for #N" →
  [BLOCKER]: tests belong to the implementing ticket.
- **Foundation ticket** — helpers "for future use", no behavior of
  its own → [BLOCKER]: re-slice by capability.
- **Migration split from schema** — schema change and its migration
  in different tickets → [BLOCKER]: same ticket, always.

## Output

Per ticket: `#N — READY` or the classified findings with fixes. End
with the batch table `| # | Ready? | Blockers |` — the caller folds
it into the quiz (`/spec-to-tickets`) or the wave table
(`/orchestrate`).
