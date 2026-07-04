---
name: constitution-compliance-review
description: >
  Use when the reviewer subagent is reviewing a diff that touches a domain rule,
  a calculation, a sensitive numeric value, the audit trail, source-of-rule
  attribution, stage/responsibility boundaries, or past-period rules. Checks the
  diff against the system constitution (architecture/constitution.md). This is
  the regulated-domain reviewer dimension — apply it on top of
  general-code-review whenever the diff touches domain logic.
---

# Constitution Compliance Review

## Overview

**You are the machine that catches a regulatory or domain violation before it ships into a system where a mistake is expensive and auditable.** General code review checks whether the code works; you check whether it works *the way the domain requires*. A calculation that is correct but uses the wrong numeric type, or a decision the system can't trace back to its rule, is a violation even when every test is green.

Load `architecture/constitution.md` and review the diff against it. The checks below are the standard ones for a regulated/normative domain, and the file is authoritative **in both directions**: if the project's constitution adds or specializes a principle, hold the diff to that too; and a check whose subject the constitution does not define (stage separation in a project without stages, past-period rules where the concept doesn't exist) does not apply — don't manufacture findings against principles the project never adopted.

## When to Use

- A code-review subagent is reviewing a diff that touches a domain rule, a calculation, a sensitive numeric value, the audit trail, source attribution, a stage boundary, or a past-period rule.

**Not for:** general correctness/simplicity/tests (use `general-code-review`); whether the diff matches the spec or plan (use `conformance-review`); diffs that touch no domain logic at all (pure infra/tooling).

## The checks

Walk these against the constitution. Each violation is a **[BLOCKER]** unless the constitution explicitly allows the deviation with a documented reason.

1. **Sensitive numeric type.** Every high-sensitivity numeric value (monetary, percentage used in a calculation, quantity in a small unit) uses a fixed-precision type (Decimal/BigDecimal/equivalent), never float. Check especially the conversion path: string → precise type **directly**, never via an intermediate float (`Decimal(str)`, not `Decimal(float(str))`). A float anywhere on the path to a sensitive value is a [BLOCKER].

2. **Rounding policy.** Rounding is explicit and follows the single documented policy (e.g. ROUND_HALF_EVEN), unless a normative source specifies otherwise for this value. Implicit or default rounding on a sensitive value is a violation.

3. **Audit trail.** Every critical decision the diff introduces is traceable to (a) the rule applied — with source reference when external, (b) the input that triggered it, (c) the code version that produced it. A decision the system makes but can't explain afterward is a [BLOCKER]. "Logs later" is not an audit trail.

4. **Normative source citation.** Every coded domain rule that derives from an external source (regulation, contract, technical spec) cites the source: identifier + version/date + scope, inline or in a docstring reference. A rule from an external source with no citation is a [BLOCKER] — the next person can't verify it against the norm.

5. **Separation of responsibilities.** The change stays within its stage's responsibility as the constitution defines it (e.g. ingestion only captures; validation validates structure, applies no business rule; analysis classifies/decides, computes no final value; output computes/aggregates, makes no applicability decision). Applying a rule in the wrong stage is a [BLOCKER] — it breaks the boundary and usually needs an ADR, not an increment.

6. **Immutability of past-period rules.** A past-period rule is not modified retroactively in code. If the change alters how a past period is treated, it must create a new version keyed by validity period, not edit the existing rule. Retroactively mutating a past rule is a [BLOCKER].

## How to report findings

For each finding: the **constitution principle** it violates (by name/section), **severity** (**[BLOCKER]** violation of a non-negotiable principle · **[SHOULD]** a fragile pattern that risks a future violation · **[NIT]** a citation-format or documentation nicety), **location** (`file:line`), and the **concrete fix** ("convert with `Decimal(raw_string)`; the `float()` on line 42 loses precision before the Decimal ever sees it"). Cite the constitution section so the implementer can confirm. If the diff touches domain logic and you found no violation, say so explicitly with what you checked — a clean review with evidence is the goal, not manufactured findings.

If a finding is really about whether the rule matches the spec (not the constitution), route it to `conformance-review` instead of duplicating it here.

## Common rationalizations

| Rationalization | Reality |
|-----------------|---------|
| "It's a float but the test passes" | The test passed on the inputs you pictured. Float drift shows up on the one you didn't. A sensitive value on a float path is a violation regardless of green tests. |
| "The rule is obvious, it doesn't need a source citation" | Obvious to you today ≠ verifiable by the auditor next year. If it derives from an external source, cite it. |
| "I'll add the audit logging in a follow-up" | A decision that shipped without a trace can't be reconstructed after the fact. The trail is part of the change, not a follow-up. |
| "It's cleaner to apply the rule here even if it's the wrong stage" | Cleaner-but-misplaced breaks the separation the constitution draws and compounds. That's an ADR-level decision, not a shortcut. |
| "I just tweaked the past-period rule in place" | Retroactive mutation of a past rule changes history. Version it; don't edit it. |

## Red flags — STOP

- Approving a sensitive calculation that touches **float** anywhere on its path.
- Approving a decision with **no audit trail** to rule + input + version.
- Approving a rule from an **external source with no citation**.
- Approving a change that **applies a business rule in the wrong stage**.
- Approving a **retroactive edit to a past-period rule**.
- Approving because tests are green, **without checking the diff against the constitution at all**.
