---
paths: ["src/**", "app/**", "lib/**", "packages/**"]
---
# Package by feature

Place every new file inside the capability it belongs to. Do not create or
grow technical-layer folders (`controllers/`, `services/`, `repositories/`,
`utils/`) at the top level.

Before creating a NEW top-level folder, all three tests must pass:

- The name denotes a recognizable business responsibility or outcome; grammar
  class is irrelevant (`payments/`, `orders/`, and `onboarding/` can qualify).
  Do not organize around a shared data noun such as `customer/` or `invoice/`.
- It is a vertical slice: it will hold that capability's rules, use cases,
  and persistence — not one horizontal layer of an entity.
- Imports point inward: other capabilities must not need to reach into it
  to complete their flows.

If a file has no clear home and the tests fail, STOP and ask the human.
Creating a capability is a boundary decision, not a filing decision.
