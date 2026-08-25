# Run log template — orchestrated-worker adapter

`.claude/logs/implement-orchestrated-<timestamp>.md`. One log per
ticket; the orchestrator owns the wave-level event log separately.

- run_id · issue # · typed branch · mode (assisted|autonomous) · claim
- Phase 0 preflight: spec status; pinned-commit relevance verdict
  (CURRENT / REBASED_NO_RELEVANT_CHANGE / STALE)
- Phase 1: proven delta — or NO_CHANGE_CANDIDATE (evidence target
  posted; corroboration verdict recorded)
- Phase 3: APPROVAL-FINGERPRINT (bundle: plan + scope manifest +
  pins); approving reply's fingerprint (assisted)
- Phase 4–5: chunks; per-criterion evidence (ID → test → output ref);
  browser evidence refs for UI criteria
- Phase 6–7: durable sync; seal SHAs (re-seals listed)
- Phase 8: self-checks run (no authority); re-engagements handled
- Phase 9 terminal: PR_READY_AWAITING_HUMAN | NAMED_BLOCKER |
  NO_CHANGE_REQUIRED (corroborated) — parked or released
- Cost where visible
