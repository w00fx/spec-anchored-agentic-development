# Review target & seal — schemas (staged enforcement)

`review-target.json` (frozen at Phase 7):

```json
{"run_id":"RUN-…","base_sha":"…","head_sha":"…","diff_sha256":"…",
 "spec_corpus_sha256":"…","plan_sha256":"…","evidence_manifest_sha256":"…"}
```

`review-report.json` (Phase 8):

```json
{"review_target_sha256":"…","reviewed_head_sha":"…",
 "status":"pass|blockers","findings":[]}
```

Final check before PR/update: current head == target head; current
diff hash == target hash; evidence hash matches; report points at the
target. Any mismatch → `REVIEW_INVALIDATED` (back to Phase 7). CI
recomputes this regardless of which tool produced the state.
