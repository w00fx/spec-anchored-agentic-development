---
description: Interview to create a capability spec (permanent, from the template)
argument-hint: [capability name]
---

You'll create a **capability spec** — the permanent business source of
truth for the capability in the argument. Use the template in
`specs/_template/capability-spec.md`, and first read the root
AGENTS.md/CLAUDE.md and `architecture/pipeline.md` (or equivalent) so
you know the neighbors and the contracts.

Then interview me, section by section of the template:

- **Purpose and capability language** — what this capability does for
  the business, and the terms that mean something specific inside it.
- **Business rules** — one at a time, in EARS form. For every rule that
  derives from an external source (regulation, contract, technical
  spec), ask for the citation: identifier + version + scope.
- **Acceptance criteria** — concrete Given/When/Then scenarios. For
  calculation rules, collect **reference values** (input → expected
  output); they become the golden tests.
- **Edge cases** — missing input, invalid source, out-of-range values,
  retries, concurrency. Don't ask the obvious; focus on what could go
  wrong.
- **Non-goals** — what this capability explicitly does NOT do. These
  are enforced later (conformance review blocks behavior they exclude),
  so make them real.
- **Contracts and dependencies** — what it consumes and produces, from
  and to which capabilities.

Rules of the interview:
- Don't write code.
- One theme at a time; go deeper when an answer smells incomplete.
- At the end, write the spec at `specs/<capability>/<capability>.md`
  and report the path.
- List 3-5 open questions if ambiguity remains — unresolved ambiguity
  belongs in the open questions, never silently filled with a default.
