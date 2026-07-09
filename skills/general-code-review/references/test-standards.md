# Test standards — the shared bar (producer writes to it; reviewer holds to it)

The bar: tests verify **behavior through public interfaces**. The code
inside can change entirely; the tests shouldn't move. A good test reads
as a specification of what the system does — not as a mirror of how it
currently does it. Examples are TypeScript; the principles are
language-agnostic (in Go, table-driven tests carry the same bar).

## Worked pairs

**Implementation-testing (BAD) vs behavior (GOOD):**

```ts
// BAD — knows the internals; breaks on harmless refactor
it("adds items to internal array", () => {
  cart.addItem(item);
  expect(cart.items).toContain(item);
  expect(cart.itemCount).toBe(1);
});

// GOOD — asserts the observable outcome
it("calculates total for added items", () => {
  cart.addItem({ price: 10.99, quantity: 2 });
  expect(cart.getTotal()).toBe(21.98);
});
```

**Mock-heavy (BAD) vs real behavior (GOOD):**

```ts
// BAD — only proves the mocks were called
it("calls repository save method", async () => {
  await service.createUser(userData);
  expect(mockRepo.save).toHaveBeenCalledWith(user);
  expect(mockLogger.log).toHaveBeenCalledTimes(1);
});

// GOOD — proves the behavior end to end
it("persists user for later retrieval", async () => {
  await service.createUser(userData);
  const retrieved = await service.getUser(userData.id);
  expect(retrieved.email).toBe(userData.email);
});
```

**Bypassing the interface (BAD) vs through the interface (GOOD):**

```ts
// BAD — verifies through external means (raw DB read)
it("createUser saves to database", async () => {
  await service.createUser(userData);
  const row = await db.query("SELECT * FROM users WHERE id = ?", [id]);
  expect(row.email).toBe(userData.email);
});

// GOOD — the interface is the contract; verify through it
it("makes user retrievable", async () => {
  await service.createUser(userData);
  expect((await service.getUser(id)).email).toBe(userData.email);
});
```

## Structure

- **One logical assertion per test.** Several `expect`s are fine when
  they express one behavior; two behaviors means two tests.
- **The name states WHAT the system does, never HOW.** "persists user
  for later retrieval", not "calls repository save method".

## Red flags

- Mocking internal collaborators (classes you own).
- Asserting call counts on your own code.
- A test name that describes the mechanism instead of the behavior.
- A test that breaks when refactoring without a behavior change.
- Verifying through external means instead of the public interface.
- You can't tell from the test alone what behavior it guarantees.

## Mocking — the boundary rule

Mock **only at system boundaries**:

- External APIs and third-party services — yes.
- Time and randomness — yes (inject a clock / a seed).
- The database — sometimes; prefer a real test database when practical.
- The filesystem — sometimes, for speed or isolation.

**Never mock your own classes, internal collaborators, or anything you
control.** If your own code is hard to test without mocks, that is a
design finding, not a mocking problem.

## Design for testability

- **Inject dependencies** — `new EmailService()` inside a class makes
  the boundary unmockable; a constructor-injected `EmailSender` makes
  the boundary explicit and the mock trivial.
- **SDK-style interfaces over generic fetchers** — mocking
  `apiClient.fetch(url, options)` forces the test to know URLs and HTTP
  details; mocking `githubClient.getUser(username)` is one line. Wrap
  external services behind interfaces shaped like what you consume.

---

Adapted from Matt Pocock's `tdd` skill (`tests.md` + `mocking.md`). The
severity mapping and the spec-anchoring context are this system's.
