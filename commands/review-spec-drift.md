---
description: Checks drift between specs and implementation
argument-hint: [capability name]
---

For the capability in the argument (or the current one if omitted):
1. Read the spec in specs/<capability>/.
2. Read the contracts in specs/<capability>/contracts/.
3. Read the corresponding implementation code.
4. Identify discrepancies:
   - Behaviors described in the spec not implemented
   - Behaviors in the code not anticipated in the spec
   - Schemas in contracts that don't match the code
5. Report in the format:
   - Critical drift (blocks production)
   - Relevant drift (fix next sprint)
   - Cosmetic drift (update spec)

Don't fix anything. Just report.
