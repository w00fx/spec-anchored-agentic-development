# Smell baseline — a named vocabulary for structural findings

Twelve smells from Fowler's *Refactoring* (ch. 3), each with its fix.
Three binding rules govern their use:

- **The repo overrides.** If the repository documents a standard that
  contradicts a smell, the repo wins — suppress the smell.
- **Always a judgement call.** A smell is a labelled heuristic, never a
  hard violation: severity caps at **[SHOULD]** — a smell alone is
  never a [BLOCKER].
- **Skip anything tooling already enforces** (line length, formatting,
  complexity caps) — deterministic gates own those.

## The twelve

- **Mysterious Name** — a name that needs the body read to be
  understood → rename to what it does or is.
- **Duplicated Code** — same logic in multiple places → extract and
  reuse (respecting capability boundaries — cross-capability
  duplication may be the *cheaper* choice; see package-by-feature).
- **Long Function** — does several things → decompose by intent, one
  level of abstraction per function.
- **Long Parameter List** — a signature that reads like a form →
  introduce a parameter object that names the concept.
- **Global Data** — state reachable from anywhere → encapsulate behind
  an owner.
- **Mutable Shared Data** — widely-scoped mutation → narrow the scope;
  prefer values.
- **Divergent Change** — one module edited for many unrelated reasons →
  split by reason for change.
- **Shotgun Surgery** — one change forces edits across many modules →
  consolidate the responsibility (a capability-boundary signal).
- **Feature Envy** — a function more interested in another module's
  data than its own → move it to where the data lives.
- **Data Clumps** — the same fields travelling together → make them a
  type.
- **Primitive Obsession** — domain concepts as bare primitives → parse
  into domain types (Dimension 4's territory; in this domain, money as
  float is the constitution's, not this baseline's).
- **Speculative Generality** — abstraction for a future that isn't
  here → delete it (the review-side twin of the producer's Opus guard).

---

Curated in Matt Pocock's `code-review` skill from Fowler, *Refactoring*
ch. 3. The severity cap, boundary cross-references, and
tooling-deference rule are this system's.

**The paragraph-comment smell** (field-proven at 1M lines — source #36):
a workaround that needs a paragraph-long comment justifying why it is
OK is wrong code — fix the code, not the comment. Long explanatory
comments wrapped around workarounds are a reviewer trigger; capped at
[SHOULD] like the rest of this baseline.

**Three mechanized reward-hacking smells** (Cognition, production —
source #52; each is deterministically lintable, and the lint is the
better home where it exists):

- **getattr-so-it-never-errors** — defensive `getattr`/`hasattr` (or
  optional-chaining equivalents) on attributes the code *knows* exist,
  so the code cannot fail. Cognition's lint **fails the PR** on it.
- **Backwards-compatibility-at-all-costs** — import/export shims and
  re-exports added so nothing ever has to be renamed or moved; the
  diff avoids failure instead of finishing the change.
- **Untyped escape hatches** — untyped tuples, `dict[str, Any]`,
  `any` where a real type was one line away: the type system dodged
  so the code cannot be told it's wrong.
