---
description: Write or update the capability spec from an interview — turns a /shape session (or provided notes/transcript) into specs/<capability>/<capability>.md on the template. Does not interview back; gaps become open questions (OQ-<CAP>-###), never guesses. Every BR/AC carries a stable typed ID (BR-<CAP>-###, AC-<CAP>-###) issued in continuation; existing IDs never change, never renumber, retire instead of delete.
argument-hint: "[capability | spec path | default: this session's shaping]"
---

Turn the material in this conversation — a `/shape` session is the
common case — into the capability spec. If pointed at notes or a
transcript instead, work from those. **This command does not
interview:** the questions already happened. If material for a
template section is missing, list it under Open questions — ask
nothing, invent nothing, default nothing silently.

## Write

1. Identify the capability (the argument, or the session's subject).
   One spec per capability:
   `specs/<capability>/<capability>.md`, from
   `spec-templates/capability-spec.md`.
2. **Create mode** (no spec exists yet): fill every template section
   from the resolved material — Capability language as an opinionated
   glossary (canonical term; `_Avoid_:` synonyms; what it IS, not what
   it does); normative behavior in the representation its truth type
   demands (EARS as the default; decision tables, state models,
   formulas+oracles, schemas per the template's matrix), each
   externally-sourced rule with
   its citation (identifier + version + scope); Acceptance criteria in
   Given/When/Then, **each with its typed stable ID**; reference-value rows for every
   calculation; Non-goals with teeth; Contracts and dependencies.
3. **Update mode** (the spec exists): produce the delta — new rules,
   new items get **typed IDs issued in continuation** (the ID is the
   addressing scheme; tickets point at it), new or changed reference
   rows, non-goal updates. **Never renumber or rewrite existing
   criteria** unless the interview explicitly resolved a change to
   them.
4. Large reference tables (beyond a screen) go to
   `specs/<capability>/tables/` as data files the golden tests read;
   the rule cites the file.

## The completeness pass (writer-side — the interrogation was /shape's)

Before reporting done:

- Every template section is either filled or explicitly represented
  in Open questions.
- **Oracle coverage:** every rule has an executable expression
  (reference values → golden; GWT → tests) or is explicitly marked
  human-judgment territory.
- Every externally-sourced rule carries its citation.
- The spec stays **layer-agnostic**: no deployment targets, no
  framework names, no file paths — behavior and business truth only
  (the how lives in plans and ADRs).

## Output

Report the path, the IDs added (e.g. "BR-REG-013..015, AC-REG-016..017"),
and the Open questions list. The human validates as the owner of the
truth — the reference values are their signature — and commits: **the
spec is the first commit**, alone, before any implementation issue
references it. Then `/spec-to-tickets`.

Portability: this command's body works as a standalone prompt — paste
it after any interview, point it at the target, same result.

---

The spec is written with `status: draft` in its frontmatter.
Promotion to `ratified` happens **in the spec's own PR merged to the
protected branch by a human** — the merge is the approval record
(Option A); the status flip and the informative `approved_by/at`
mirrors travel in that same PR. Downstream (`/spec-to-tickets`,
workers) refuses drafts.

Adapted from Matt Pocock's `to-spec` skill (write from the
conversation; do not interview back). The anchored home
(`specs/<capability>/`, permanent), the template, the
typed-ID-in-continuation discipline, and the layer-agnostic rule are
this system's.
