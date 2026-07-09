---
description: Shape work through a relentless interview — create a capability spec from an idea, transcript, or existing code; refine an existing spec; or sharpen a task until it's implementable. One question at a time with a recommended answer, the codebase consulted before the human, and the paper trail written the moment things resolve.
argument-hint: [idea | task/issue | spec path | transcript | code area]
---

Identify the target from the argument and pick the mode:

- **An idea or ongoing discussion** → create a capability spec.
- **A transcript** (meeting, chat, voice note) → extract what was
  decided, interrogate the gaps, create the spec.
- **Existing code with no spec** (brownfield) → archaeology: read the
  code, draft what it *does*, interrogate what it *should* do.
- **An existing spec** → grill-back: interrogate the document for
  ambiguity and holes, refine it.
- **A task / issue** → sharpen it until an agent could implement it
  without guessing.

All modes are one machine: interview relentlessly **until we reach a
shared understanding** — that is the termination condition, not a
checklist filled. Never write implementation code.

## Interview mechanics

- **One question at a time, then wait for feedback before continuing.**
  Asking multiple questions at once is bewildering. Walk down each
  branch of the design tree, resolving dependencies between decisions
  one by one — the answer to question 3 changes what question 7 should
  be. Exception: **task mode** may ask small thematic batches (3-5
  related questions); tasks have shallow decision trees and the human
  answers between meetings.
- **For each question, provide your recommended answer.** The human
  confirms or corrects; composing from scratch is friction. The
  recommendation is a proposal — the human's answer is the truth.
- **If a question can be answered by exploring the codebase, explore
  the codebase instead.** One law bounds this (our addition, for
  domains where truth is external): code settles **facts** ("the
  parser already returns a validated Decimal"); code does not settle
  **intent** — behavior found in code enters as a *question*, never as
  a rule, until the human confirms. Code can contain bugs that became
  structural.
- **Numbers before prose.** For any calculation or threshold rule:
  collect the input → expected-output pairs with the human FIRST, then
  draft the EARS rule as the generalization of agreed examples. In the
  reverse order, examples get invented to fit your wording — you end
  up validating your prose, not their truth.
- **Stay inside one capability.** If the work crosses capability
  boundaries, stop and say so — that is architecture (new contracts,
  the human-led route), not a spec interview.

## During the session — the active discipline

Interviewing is not just asking; it is actively sharpening the model
while you go:

- **Challenge against the capability language.** When the human uses a
  term that conflicts with the spec's existing glossary, call it out
  immediately: "The spec defines 'cancellation' as X, but you seem to
  mean Y — which is it?"
- **Sharpen fuzzy language.** When a term is vague or overloaded,
  propose a precise canonical term: "You're saying 'account' — do you
  mean the Customer or the User? Those are different things."
- **Discuss concrete scenarios.** When relationships between concepts
  come up, stress-test them: invent scenarios that probe edge cases
  and force precision about the boundaries between concepts. Don't
  save this for the end — do it as the concepts appear.
- **Cross-reference with code.** When the human *states* how something
  works, check whether the code agrees, and surface contradictions:
  "The code cancels entire Orders, but you just said partial
  cancellation is possible — which is right?" (This is the reverse
  direction of exploring-instead-of-asking: there, code answers your
  questions; here, code challenges their claims.)

## What the questions walk (the completeness model)

The question generator is not vibes — it is the spec template plus the
ambiguity classes the implement skills abort on. This interview is
Phase 1.5 run *before* the work instead of during it:

- **Purpose and capability language** — what this does for the
  business; the terms with specific meaning inside it.
- **Business rules in EARS** — one at a time; every externally-sourced
  rule gets its citation (identifier + version + scope).
- **Acceptance criteria** — concrete Given/When/Then; reference values
  for every calculation. Each criterion asserts the **journey's true
  end state, never the intermediate event**: "an email sends" is not a
  criterion — "the click-through lands on the right thread" is.
- **Edge cases** — missing input, invalid source, out-of-range,
  duplicates, retries, concurrency, ordering. Don't ask the obvious;
  ask what could go wrong.
- **Non-goals** — with teeth: each one something an agent or a junior
  would plausibly build (conformance review blocks behavior they
  exclude, so make them real).
- **Contracts and dependencies** — what it consumes and produces, from
  and to which capabilities.

## The paper trail — write it the moment it resolves, never batched

- **Terms → the spec's Capability language section**, as an
  *opinionated glossary*: when multiple words exist for one concept,
  pick the best and ban the rest —

  ```
  **Invoice**: A request for payment sent after delivery.
  _Avoid_: Bill, payment request
  ```

  Definitions tight (one-two sentences; what it IS, not what it does).
  Only terms specific to this capability — general programming
  concepts don't belong. The glossary stays devoid of implementation
  details: it is a glossary and nothing else (rules go to EARS,
  values to the reference table, decisions to ADRs).
- **Rules → Business rules (EARS)**, drafted as agreed.
- **Values → reference-table rows**, as collected.
- **Decisions → an ADR at
  `architecture/decisions/YYYY-MM-DD-slug.md`** (the system's declared
  ADR home; date-prefixed like the walkthroughs, so the folder
  self-sorts), only when ALL three are true: hard to reverse,
  surprising without context, the result of a real trade-off. If any
  is missing, skip it. The format is minimal — a title plus 1-3
  sentences (context, decision, why); an ADR can be a single paragraph
  — the value is recording *that* a decision was made and *why*, not
  filling out sections. Create the directory lazily, on the first ADR. What qualifies: architectural shape,
  integration patterns, technology with real lock-in, boundary and
  scope decisions (the explicit no-s are as valuable as the yes-s),
  deliberate deviations from the obvious path (they stop the next
  engineer from "fixing" something deliberate), constraints invisible
  in the code, and non-obvious rejections (record why you didn't pick
  GraphQL, or someone suggests it again in six months).

## The grill-back (final phase of spec modes; the whole session in
refine mode)

Before writing the final document, interrogate the draft:

- **Divergence probe:** could two materially different implementations
  both be defended under this text? Wherever yes, the spec is ambiguous
  *there* — tighten it.
- **Boundary probe:** zero, negative, enormous, duplicate, concurrent,
  out-of-order — does a rule answer each, or is it deliberately out of
  scope?
- **Oracle coverage:** every rule either has an executable expression
  (reference values → golden tests; GWT → tests) or is explicitly
  marked human-judgment territory.
- **Change test:** if the external source versions tomorrow, can every
  impacted rule be located in minutes?

## Output

- **Spec modes:** write `specs/<capability>/<capability>.md` from the
  template, report the path, and list 3-5 open questions if ambiguity
  remains — unresolved ambiguity belongs in open questions, never
  silently filled with a default. The spec is committed before any
  implementation issue references it: the spec is the first commit.
- **Task mode:** the refined task text (title, context, binary
  acceptance criteria pointing at the spec where one exists, edge
  cases, out-of-scope), paste-ready for the issue.

Spec creation is always human-validated: this command structures the
interview; the human is the source of business truth.

Portability: this command's body works as a standalone prompt — paste
it into any chat, point it at the target, same interview.

---

Interview mechanics (one question at a time, recommended answers,
explore-the-codebase-instead, "shared understanding" as the stop) and
the paper-trail discipline (opinionated glossary, minimal ADRs)
adapted from Matt Pocock's `grilling` and `domain-modeling` skills.
The input modes, the fact-vs-intent law, numbers-before-prose, the
completeness model, and the grill-back are this system's.
