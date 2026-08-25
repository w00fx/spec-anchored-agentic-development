# Run log template — unattended adapter

`.claude/logs/implement-backlog-<timestamp>.md`. One log per loop run;
one section per issue. Fields follow the shared protocol (Phase 0–9).

Per issue:
- issue # · claim (applied/released) · typed branch
- Phase 0–1: preflight + proven delta — or NO_CHANGE_CANDIDATE (evidence
  target) → review → NO_CHANGE_REQUIRED only if corroborated
- Phase 2: ambiguity → NAMED_BLOCKER (question posted, label, released)
- Phase 3: APPROVAL-FINGERPRINT + plan-review lens verdict
- Phase 4–5: chunks; per-criterion evidence (ID → test → output ref)
- Phase 6–7: durable sync; seal SHAs
- Phase 8: reviewer findings + resolutions (or twice-failed → NAMED_BLOCKER)
- Phase 9 terminal: PR_READY_AWAITING_HUMAN | NAMED_BLOCKER | NO_CHANGE_REQUIRED
- Cost

Loop footer: issues attempted / terminals / halts (2-consecutive rule).
