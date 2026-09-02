# PR description template — all adapters

**Approved plan:** the executed plan and its `APPROVAL-FINGERPRINT`; in
orchestrated-assisted mode, include the approving reply identity whose
fingerprint must match.

**What changed:** end-to-end behavior from the user/system perspective.

**Evidence per requirement:** one line per pointed stable ID:
`AC-<CAP>-### → <method/command/artifact> → <observed result>`.

**Internal hardening:**

- General Code Reviewer input/output SHA, report hash, changed paths, and Owner
  accept/reject disposition;
- Mutation Hardener input/output SHA, eligible target, coverage, mutant
  dispositions, report hash, and Owner accept/reject disposition;
- final `owner_disposition_sha256` binding the inspected handoffs.

**Scope check:** touched paths are within the approved scope; non-goals, truth,
oracles, thresholds, exclusions, policy, and CI/review criteria were not
weakened.

**Risk/rollout:** flag/kill-switch/recovery state when declared; otherwise
`n/a`.

**External reviews:** pending, completed, or not required according to repository
policy. Internal hardening is not independent approval.

**Terminal:** this worker ends at `PR_READY_AWAITING_HUMAN`; the external
pipeline/orchestrator and human own later review, CI monitoring, and merge. The
worker never claims `reviewed`, `approved`, `landed`, or `merged` unless those
separate events were actually observed by their owning system.
