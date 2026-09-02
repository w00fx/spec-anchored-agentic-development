# Run log template — supervised-local adapter

`.agent-runs/<run-id>/run-log.md`; one run directory per issue/task.
All machine-readable state and evidence for the same run lives beside this log.

- run id · task/issue · typed branch · mode
- Phase 0 — authority, policy, repository commands, baseline, isolation
- Phase 1 — expected / observed / evidence / gap, or no-change target + corroboration
- Phase 2 — facts, decisions, assumptions, questions, human answers
- Phase 3 — plan, scope, test strategy, mutation target, APPROVAL-FINGERPRINT
- Phase 4 — owner implementation chunks and focused checks
- Phase 5 — initial evidence commands and artifacts
- Phase 6 — durable sync and owner checkpoint SHA
- Phase 7 — General Code Reviewer input SHA, output commit, alteration report, owner inspection and acceptance/rejection, rerun checks
- Phase 8 — Mutation Hardener input SHA, output commit, coverage/mutant report, owner inspection and acceptance/rejection, rerun checks
- Phase 9 — Owner acceptance, final SHA/diff/evidence and hardening artifact identities
- Phase 10 — PR/no-change/blocker delivery; external reviews pending/listed; terminal
- Cost where visible
