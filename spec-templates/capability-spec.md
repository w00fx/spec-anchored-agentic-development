---
# Authority & lifecycle (SA-001): human authority, not necessarily human authorship
schema_version: 1
capability_id: CAP-<NAME>
status: draft        # lifecycle metadata: draft → ratified → superseded
owner: <domain-owner>
# Authority (Option A): the protected-branch PR merge IS the approval
# record — Git carries author, reviewers, and revision. The fields
# below are informative mirrors, never a gate:
approved_by: <human>
approved_at: <date>
provenance: <shape-session / supersedes-revision>
---

# Capability: <name>

<!-- One durable logical contract per capability, with this file as the stable
     entrypoint and corpus map. It may remain one file or declare companion
     files under the same capability directory. There is no disposable semantic
     spec — what is disposable is the implementation plan, not this authority.

     Sections are ordered by CHANGE RATE: stable at the top constrains the
     volatile below. Each section must be DIAGNOSTIC — if the agent's output
     varies in a way a section was meant to pin down, that section is too vague.
     Document only what the agent CANNOT infer from the code; don't describe
     folder structure. A frontend area is just a capability whose I/O is flows
     and interaction states instead of data — same template. -->

## Purpose

<!-- 1-2 sentences: what this capability does for the business and the one thing
     it must get right. Not how it's built. -->

## Capability language

<!-- Opinionated glossary, nothing else. Pick the canonical term and ban
     the synonyms:
       **Term**: what it IS (one-two sentences, not what it does).
       _Avoid_: synonym1, synonym2
     Only terms specific to this capability; no implementation details
     (rules -> EARS, values -> reference table, decisions -> ADRs). -->

<!-- Glossary of the terms used HERE and what each means in THIS capability.
     Flag terms that mean something different elsewhere ("Order" here vs "Order"
     in shipping). This is usually the least-inferable thing in the spec. -->

| Term | Meaning here |
|------|--------------|
|      |              |

## Normative behavior (EARS as the default form)

Each rule is a heading with a stable typed ID — `### BR-<CAP>-001 —
<name>` — never renumbered; retired, not deleted. Tickets, tests, and
reviews point at these IDs.

### BR-<CAP>-001 — <name>

WHEN <trigger>, the system SHALL <observable behavior>. *(Source:
<identifier + version + scope> when derived from an external rule.)*

<!-- Representation by truth type — EARS is the default for event/state
     responses, not a universal container: combination of conditions →
     decision table; lifecycle → state model; calculation → formula +
     units + rounding + oracle (the numbers live in the reference-value
     table and become the golden); data shape → schema; invariant →
     property; measurable quality → QC-* with limit + method. Every
     item, whatever its representation, carries its typed ID as heading.
     EARS patterns:
       "The system SHALL <x>."
       "WHEN <trigger>, the system SHALL <x>."
       "IF <condition>, THEN the system SHALL <x>."
       "WHILE <state>, the system SHALL <x>." -->

- The system SHALL ...
- WHEN ..., the system SHALL ...
  > Source: <norm / regulation id + version + scope>   (when applicable)

## Acceptance criteria (Given / When / Then)

Each criterion is a heading with a stable typed ID — `### AC-<CAP>-001
— <name>` — same rules as BR IDs; `AC verifies BR-…` is stated where
the relation exists.

### AC-<CAP>-001 — <name> *(verifies BR-<CAP>-001)*

GIVEN <state> WHEN <action> THEN <observable outcome with values>.

<!-- Binary pass/fail. Each criterion is a scenario its declared verification
     method can check (test by default; static check, schema validation,
     benchmark, inspection, or runtime observation where the truth type
     demands it) — tool-neutral, and what lets the model "cook".
     For a calculation, anchor on reference values (input -> expected output),
     which become the golden the implementation is tested against. -->

- **Given** <state>, **When** <action>, **Then** <observable result>.

## Non-goals

<!-- What this capability explicitly does NOT do. Kills scope creep and tells the
     agent where the boundary is. -->

- This capability does NOT ...

## Contracts (inputs / outputs)

<!-- What this capability receives and produces, and from/to whom. Reference the
     contract files (schemas) rather than inlining large ones. This is the
     boundary other capabilities depend on. For a frontend area, the consumed
     API contract is the boundary to the owning backend capability.
     If this capability spans multiple deployables (services, functions), add a
     responsibility map here: which deployable owns which slice, and the
     contracts BETWEEN them. -->

- **Input:** <from which capability> — see `contracts/<x>`
- **Output:** <to which capability> — see `contracts/<y>`

<!-- Failure siblings: event/response contracts declare the failure case
     alongside success (Created => CreateRejected) — a contract that only
     describes success describes half a system, the half that doesn't
     ping you. (Source #37) -->

<!-- Access policies are contract material too: declare who may call what
     next to the endpoint it protects, generate the enforcement, and fail
     closed — an undeclared policy means denied. A security audit should be
     reading this file, not fifty resolvers. (Source #37) -->

## Observability

The events and metrics that prove this capability works in
production — named here because runtime truth deserves an address
too (a field promoted from the ticket checklist, source #48; the
runtime-only bug class, source #50):

- **Events:** what the capability emits when it succeeds and when it
  rejects (mirror the failure siblings above).
- **Metrics:** the one or two signals a human would check to answer
  "is this working for real users?"
- These land in tickets as instrumentation criteria. **The presence
  and correctness of instrumentation can be an acceptance criterion
  and a merge gate; the production outcome never is** — outcomes are
  rollout/promotion signals feeding lessons and spec deltas.

## Dependencies

<!-- Other capabilities this one depends on, and the nature (upstream/downstream). -->

-

## Open questions

Unresolved gaps live here — never invented defaults. Lifecycle:
`open → resolved-by BR/AC/CTR → retired` (an OQ never silently
disappears; its resolution names the ID that answered it).

- **OQ-<CAP>-001 — <question>**
  - Why unresolved: …
  - Decision needed from: …
  - Blocks: …
