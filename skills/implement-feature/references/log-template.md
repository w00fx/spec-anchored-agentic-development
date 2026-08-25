# Run log template — supervised-local adapter

`.claude/logs/implement-feature-<timestamp>.md`. Fields follow the
shared protocol (Phase 0–9); one log per run.

- run_id · issue/target · typed branch · mode: supervised-local
- Phase 0 preflight: spec status + pinned commit check (SPEC_CURRENT/STALE)
- Phase 1 proven delta: expected / observed / evidence (command + exit) / gap
  — or NO_CHANGE_CANDIDATE (evidence target; classification) → Phase 8 review →
  NO_CHANGE_REQUIRED only if corroborated
- Phase 2 ambiguity: questions asked, answers (in-session)
- Phase 3 plan: APPROVAL-FINGERPRINT, human approval noted
- Phase 4 implement: chunks, declared-interface commands run
- Phase 5 verify: per-criterion (ID → test → runner output ref)
- Phase 6 durable sync: lessons/docs/proposals written
- Phase 7 seal: base/head SHAs; re-seals if edited after
- Phase 8 review: reviewer dispatched, findings, resolutions
- Phase 9 terminal: PR_READY_AWAITING_HUMAN | NAMED_BLOCKER | NO_CHANGE_REQUIRED
- Cost where visible
