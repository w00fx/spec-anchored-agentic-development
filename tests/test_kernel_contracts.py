#!/usr/bin/env python3
"""Kernel contract checks — fast, in-process, no repository copies.

The corpus/documentation fixtures live in tests/test_corpus.py: the
mutation runner re-runs THIS file per mutant, and re-copying the whole
bundle 16 times to re-check prose was the gate's cost problem
(eleventh audit, P0-01).
"""
import sys, os, json
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _harness import Suite, load_kernel

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sa = load_kernel(ROOT)
POL = sa.resolve_policy("supervised-local/v1")
S = Suite("contract checks")

# ---------- 1. canonical form ----------
S.section("1 canonical form")
S.holds("CRLF, trailing spaces and blank edges collapse to one hash",
        sa.hash_text("line one \r\nline two\r\n\r\n") == sa.hash_text("\n\nline one\nline two\n"))
S.holds("key order does not change the JSON hash",
        sa.hash_json({"b": 1, "a": [1, 2]}) == sa.hash_json({"a": [1, 2], "b": 1}))
S.holds("a real content change does change the hash",
        sa.hash_text("line one\n") != sa.hash_text("line onx\n"))
S.raises("a Markdown hard break is refused, not silently normalized",
         sa.canonical_text_bytes, "a line ending in a hard break  \nnext\n")
S.value("a plain body canonicalizes to bytes", sa.canonical_text_bytes, "ok\n",
        pred=lambda b: isinstance(b, bytes) and b.endswith(b"\n"))
S.raises("duplicate JSON keys are refused (ambiguous document)",
         sa.strict_json_loads, '{"a":1,"a":2}')
S.raises("non-finite JSON constants are refused", sa.strict_json_loads, '{"a": NaN}')
S.value("well-formed JSON parses", sa.strict_json_loads, '{"a":1}', expect={"a": 1})

# ---------- 2. approval identity ----------
S.section("2 approval identity")
BASE = {
    "schema_version": 1, "run_id": "RUN-001", "adapter": "implement-feature",
    "execution_mode": "supervised", "policy_profile": "supervised-local/v1",
    "policy_sha256": sa.hash_json(dict(sa.resolve_policy("supervised-local/v1"))), "ticket_ref": "org/repo#42",
    "ticket_body_sha256": sa.hash_text("implement AC-PAY-004"),
    "base_sha": "a" * 40, "spec_entrypoint": "specs/payments/payments.md",
    "spec_pinned_commit": "b" * 40, "spec_corpus_sha256": "2" * 64,
    "plan_artifact_id": "issue-comment:12345",
    "plan_sha256": sa.hash_text("1. add validator\n2. test"),
    "scope_manifest_sha256": sa.hash_json({"allowed_paths": ["src/pay/**"]}),
    "semantic_amendment_sha256": None,
}
S.value("a complete bundle builds", sa.build_approval, BASE, policy=POL,
        pred=lambda out: isinstance(out, tuple) and len(out[1]) == 64)
_, FP0 = sa.build_approval(BASE, policy=POL)
S.holds("same content → same fingerprint (order-independent)",
        sa.build_approval(dict(reversed(list(BASE.items()))), policy=POL)[1] == FP0)
MUTATIONS = {
    "plan edited": ("plan_sha256", sa.hash_text("1. add validator\n2. test\n3. extra")),
    "scope widened": ("scope_manifest_sha256", sa.hash_json({"allowed_paths": ["src/**"]})),
    "ticket body edited": ("ticket_body_sha256", sa.hash_text("implement AC-PAY-009")),
    "base moved": ("base_sha", "c" * 40),
    "spec pin moved": ("spec_pinned_commit", "d" * 40),
    "spec corpus changed": ("spec_corpus_sha256", "3" * 64),
    "spec entrypoint swapped": ("spec_entrypoint", "specs/orders/orders.md"),
    "ticket ref swapped": ("ticket_ref", "org/repo#43"),
    "amendment attached": ("semantic_amendment_sha256", sa.hash_text("BR-PAY-001 → new")),
    "plan re-posted elsewhere": ("plan_artifact_id", "issue-comment:99999"),
    "different run": ("run_id", "RUN-002"),
    "spec corpus swapped": ("spec_corpus_sha256", "7" * 64),
}
for label, (field, value) in MUTATIONS.items():
    S.holds(f"{label} → new fingerprint (a stale `approved` stops binding)",
            sa.build_approval({**BASE, field: value}, policy=POL)[1] != FP0)
S.holds("a coherent mode escalation → new fingerprint",
        sa.build_approval({**BASE, "adapter": "implement-backlog",
                           "execution_mode": "unattended",
                           "policy_profile": "unattended/v1",
                           "policy_sha256": sa.hash_json(dict(sa.resolve_policy("unattended/v1")))},
                          policy="unattended/v1")[1] != FP0)
S.raises("an adapter the profile forbids is refused at build time",
         sa.build_approval, {**BASE, "adapter": "implement-backlog"}, policy=POL)
S.raises("an execution_mode contradicting the profile is refused",
         sa.build_approval, {**BASE, "execution_mode": "unattended"}, policy=POL)
S.raises("a policy hash that is not the policy's hash is refused",
         sa.build_approval, {**BASE, "policy_sha256": "9" * 64}, policy=POL)
S.raises("an unknown policy profile is refused",
         sa.build_approval, {**BASE, "policy_profile": "yolo/v1"}, policy=POL)
S.raises("an incomplete bundle is refused",
         sa.build_approval, {k: v for k, v in BASE.items() if k != "plan_sha256"}, policy=POL)
S.raises("a bundle carrying its own fingerprint is refused (acyclic identity)",
         sa.build_approval, {**BASE, "approval_fingerprint": FP0}, policy=POL)
S.raises("placeholder values are refused",
         sa.build_approval, {**{k: "x" for k in BASE}, "schema_version": 1,
                             "semantic_amendment_sha256": None}, policy=POL)
S.raises("a boolean where an int is required is refused (True is not 1 here)",
         sa.build_approval, {**BASE, "schema_version": True}, policy=POL)

RECORD = {"schema_version": 1, "approval_fingerprint": FP0,
          "approval_artifact_id": "issue-comment:12346", "approver": "rapha",
          "approved_at": "2026-08-13T10:00:00Z", "provider": "github",
          "repository": "org/repo", "run_id": "RUN-001"}
S.clean("a matching approval record verifies", sa.verify_approval, RECORD, BASE, policy=POL)
S.violations("an approval of a different object is refused",
             sa.verify_approval, {**RECORD, "approval_fingerprint": sa.hash_text("other")}, BASE, policy=POL)
S.violations("an approval record without an approver is refused",
             sa.verify_approval, {**RECORD, "approver": ""}, BASE, policy=POL)
S.violations("a non-RFC3339 timestamp is refused",
             sa.verify_approval, {**RECORD, "approved_at": "yesterday"}, BASE, policy=POL)
S.violations("an unknown provider is refused",
             sa.verify_approval, {**RECORD, "provider": "carrier-pigeon"}, BASE, policy=POL)

# ---------- 3. scope ----------
S.section("3 mechanical scope, typed truth, policy floor")
MANIFEST = {
    "schema_version": 1, "run_id": "RUN-001", "capability": "CAP-PAY",
    "adapter": "implement-feature", "execution_mode": "supervised",
    "policy_profile": "supervised-local/v1",
    "semantic_scope": {"implements": ["BR-PAY-001"], "verifies": ["AC-PAY-004"],
                       "non_goals": []},
    "mechanical_scope": {
        "allowed_paths": ["src/pay/**", "tests/pay/**"],
        "denied_paths": ["src/pay/secrets/**"],
        "permissions": {"dependency_change": False, "schema_change": False,
                        "data_migration": False, "external_side_effect": False}},
    "truth_change": {"policy": "none", "allowed_spec_paths": []},
}
ns = sa.parse_name_status
sup = lambda m, ch: sa.validate_scope(m, ch, profile="supervised-local/v1")

S.clean("an authorized diff passes", sup, MANIFEST,
        ns("M\tsrc/pay/charge.py\nA\ttests/pay/test_charge.py"))
S.violations("a path outside allowed_paths is refused", sup, MANIFEST, ns("M\tsrc/orders/o.py"))
S.violations("a denied path wins over an allowed prefix", sup, MANIFEST,
             ns("M\tsrc/pay/secrets/key.py"))
S.violations("a spec write under policy 'none' is refused", sup, MANIFEST,
             ns("M\tspecs/payments/payments.md"))
S.violations("a rename with one end outside scope is refused (both ends checked)",
             sup, MANIFEST, ns("R100\tsrc/pay/a.py\tsrc/other/a.py"))
GATED = json.loads(json.dumps(MANIFEST))
GATED["truth_change"] = {"policy": "semantic-amendment",
                         "allowed_spec_paths": ["specs/payments/payments.md"]}
S.clean("a gated amendment on the exact authorized spec path passes", sup, GATED,
        ns("M\tspecs/payments/payments.md"))
S.violations("a gated amendment on a different spec is still refused", sup, GATED,
             ns("M\tspecs/orders/orders.md"))
S.violations("a spec amendment does not authorize the golden oracle", sup, GATED,
             ns("M\ttests/golden/values.py"))
S.violations("the governance floor protects the machine's own contracts", sup,
             {**MANIFEST, "mechanical_scope": {**MANIFEST["mechanical_scope"],
                                               "allowed_paths": ["**"]}},
             ns("M\tscripts/spec-anchored"))
S.value("NUL (-z) parsing understands renames", sa.parse_name_status,
        "R100\x00src/pay/a.py\x00src/pay/b.py\x00", nul=True,
        expect=[("R100", "src/pay/a.py"), ("R100", "src/pay/b.py")])

# ---------- 4. terminal contract ----------
S.section("4 terminal contract")
PR_OK = {"schema_version": 1, "run_id": "RUN-001", "issue_ref": "org/repo#42",
         "terminal": "PR_READY_AWAITING_HUMAN", "claim_state": "parked",
         "pr_url": "https://github.com/org/repo/pull/7", "head_sha": "e" * 40,
         "approval_fingerprint": FP0,
         "general_hardening_report_sha256": sa.hash_text("general-hardening"),
         "mutation_hardening_report_sha256": sa.hash_text("mutation-hardening"),
         "owner_disposition_sha256": sa.hash_text("owner-disposition")}
S.clean("a well-formed PR_READY result passes", sa.validate_result, PR_OK)
S.violations("an unknown terminal is refused", sa.validate_result, {**PR_OK, "terminal": "DONE"})
S.violations("PR_READY without the approval fingerprint is refused", sa.validate_result,
             {k: v for k, v in PR_OK.items() if k != "approval_fingerprint"})
S.violations("PR_READY without the general hardening report is refused", sa.validate_result,
             {k: v for k, v in PR_OK.items() if k != "general_hardening_report_sha256"})
S.violations("PR_READY without the mutation hardening report is refused", sa.validate_result,
             {k: v for k, v in PR_OK.items() if k != "mutation_hardening_report_sha256"})
S.violations("PR_READY without the Owner disposition is refused", sa.validate_result,
             {k: v for k, v in PR_OK.items() if k != "owner_disposition_sha256"})
S.violations("PR_READY with a released claim is refused (a claim outlives no terminal)",
             sa.validate_result, {**PR_OK, "claim_state": "released"})
S.violations("a PR from another repository is refused", sa.validate_result,
             {**PR_OK, "pr_url": "https://github.com/other/repo/pull/7"})
S.violations("a PR URL on an arbitrary host is refused", sa.validate_result,
             {**PR_OK, "pr_url": "https://evil.example/org/repo/pull/7"})
S.violations("a run claiming the merge is refused", sa.validate_result,
             {**PR_OK, "state": "merged"})
NC_OK = {"schema_version": 1, "run_id": "RUN-002", "issue_ref": "org/repo#43",
         "terminal": "NO_CHANGE_REQUIRED", "claim_state": "released",
         "evidence_target_sha256": sa.hash_text("target"),
         "no_change_corroboration_sha256": sa.hash_text("corroboration"),
         "classification": "ALREADY_SATISFIED", "corroborated": True}
S.clean("a corroborated no-change passes", sa.validate_result, NC_OK)
S.violations("NO_CHANGE without its corroboration artifact is refused", sa.validate_result,
             {k: v for k, v in NC_OK.items() if k != "no_change_corroboration_sha256"})
S.violations("an uncorroborated candidate is refused as a terminal", sa.validate_result,
             {**NC_OK, "corroborated": False})
S.violations("UNVERIFIABLE is never promoted to no-change", sa.validate_result,
             {**NC_OK, "classification": "UNVERIFIABLE"})
S.violations("WRONG_SYSTEM never resolves the graph either", sa.validate_result,
             {**NC_OK, "classification": "WRONG_SYSTEM"})
S.violations("a no-change carrying a PR is refused", sa.validate_result,
             {**NC_OK, "pr_url": "https://github.com/org/repo/pull/9"})
BL_OK = {"schema_version": 1, "run_id": "RUN-003", "issue_ref": "org/repo#44",
         "terminal": "NAMED_BLOCKER", "claim_state": "released",
         "blocker_kind": "AMBIGUITY",
         "issue_comment_url": "https://github.com/org/repo/issues/44#issuecomment-1"}
S.clean("a well-formed blocker passes", sa.validate_result, BL_OK)
S.violations("a blocker holding its claim is refused", sa.validate_result,
             {**BL_OK, "claim_state": "parked"})
S.violations("an invented blocker kind is refused", sa.validate_result,
             {**BL_OK, "blocker_kind": "VIBES"})

sys.exit(S.report())
