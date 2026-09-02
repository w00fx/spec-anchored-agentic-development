# Testing and verification

1. Every material behavior, contract, invariant, or quality change must map to
   evidence capable of detecting a relevant regression.

2. Use the lowest test boundary that faithfully proves the property:
   - pure deterministic logic: unit or property test;
   - database, queue, filesystem, framework, process, or infrastructure
     semantics: integration test;
   - API, event, schema, or public interface: contract test;
   - a critical cross-system journey not provable below: end-to-end test.

3. Every reproducible bug fix requires permanent regression coverage at the
   boundary where the defect actually occurs. Regression is a purpose, not a
   separate test level.

4. Do not mock or replace the boundary whose real behavior must be proved.

5. Code selected by the approved mutation policy must reach 100% line and
   branch coverage on the eligible target, 100% mutant resolution, and zero
   actionable surviving mutants. Equivalent or tooling-limited mutants require
   owner review; the hardener cannot approve its own exclusion.

6. Parsers, decoders, validators, untrusted-input boundaries, serialization,
   protocol/state-machine transitions, and broad input spaces require fuzz or
   property-based testing when applicable.

7. Every fuzz failure must retain a reproducible seed or minimized input and be
   promoted to permanent regression coverage.

8. Never delete, weaken, skip, rewrite, or reconfigure tests, reference oracles,
   mutation exclusions, fuzz corpora, or thresholds merely to make a gate pass.

9. Record the exact commands, exit status, relevant output, artifacts,
   unexecuted checks, and remaining limitations.
