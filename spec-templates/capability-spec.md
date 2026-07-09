# Capability: <name>

<!-- One spec per capability. PERMANENT: it is the business source of truth for
     this capability and lives as long as the capability does. There is no
     "disposable" spec — what is disposable is the implementation plan, not this.

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

## Business rules (EARS)

<!-- One rule per line, in EARS form (Easy Approach to Requirements Syntax,
     Mavin et al., Rolls-Royce) — imperative and testable. When a rule
     derives from an external source, cite it: identifier + version + scope.
     For calculation rules, EARS states the policy and cites the source;
     the numbers live in the reference-value table under Acceptance
     criteria (they become the golden).
     EARS patterns:
       "The system SHALL <x>."
       "WHEN <trigger>, the system SHALL <x>."
       "IF <condition>, THEN the system SHALL <x>."
       "WHILE <state>, the system SHALL <x>." -->

- The system SHALL ...
- WHEN ..., the system SHALL ...
  > Source: <norm / regulation id + version + scope>   (when applicable)

## Acceptance criteria (Given / When / Then)

<!-- Binary pass/fail. Each criterion is a scenario a test can verify — this is
     what lets the model "cook" and what an autonomous /goal checks against.
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

## Dependencies

<!-- Other capabilities this one depends on, and the nature (upstream/downstream). -->

-
