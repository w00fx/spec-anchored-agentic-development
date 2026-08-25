"""Test harness with EXPLICIT outcome protocols.

The tenth audit killed the previous generic helper: it returned
`bool(result)`, so a parser that wrongly ACCEPTED bad input (returning
a non-empty object) was recorded as having REFUSED it. Four deliberate
regressions in the kernel left all 85 checks green.

The kernel has two refusal conventions, and a fixture must say which
one it expects:

    raises(...)      builders and parsers  — refusal is an exception
    violations(...)  validators            — refusal is a non-empty list
    clean(...)       validators            — acceptance is an empty list
    value(...)       builders and parsers  — acceptance is a value
    holds(...)       plain property assertions (hash equality, …)

Nothing here falls back on truthiness, and an unexpected exception is
always a failure rather than an accidental pass.
"""
import sys, traceback
sys.dont_write_bytecode = True   # suites must leave a consumer's tree clean

# Set by load_kernel(): the ONE exception type that counts as a
# contract refusal. Anything else (RuntimeError, TypeError, NameError)
# is a programming failure and must turn the suite red — the eleventh
# audit showed `exc=Exception` let a crashing parser pass as "refused".
DEFAULT_EXC = ValueError


class Suite:
    def __init__(self, title):
        self.title = title
        self.passed, self.failed = [], []

    # -- reporting -------------------------------------------------
    def section(self, name):
        print(f"\n[{name}]")

    def _ok(self, name):
        self.passed.append(name); print(f"  ok   {name}")

    def _no(self, name, why):
        self.failed.append((name, why)); print(f"  FAIL {name}\n         → {why}")

    def report(self):
        print(f"\n{len(self.passed)} passed, {len(self.failed)} failed")
        for name, why in self.failed:
            print(f"  FAILED: {name} — {why}")
        if self.failed:
            print(f"{self.title}: RED")
            return 1
        print(f"{self.title}: every fixture behaved as its declared protocol requires")
        return 0

    # -- protocols -------------------------------------------------
    def raises(self, name, fn, *args, exc=None, **kw):
        """Refusal MUST be the contract's own exception type.

        A crash of any other type is a programming failure, never a
        refusal, and fails the fixture.
        """
        exc = exc or DEFAULT_EXC
        try:
            out = fn(*args, **kw)
        except exc:
            return self._ok(name)
        except BaseException as e:
            return self._no(name, f"raised {type(e).__name__} (a programming failure, "
                                  f"not a contract refusal) instead of {exc.__name__}: {e}")
        return self._no(name, f"expected a refusal ({exc.__name__}), but the call "
                              f"returned {out!r:.120}")

    def violations(self, name, fn, *args, **kw):
        """Refusal MUST be a non-empty list of violation strings."""
        try:
            out = fn(*args, **kw)
        except Exception as e:
            return self._no(name, f"expected a violations list, got {type(e).__name__}: {e}")
        if isinstance(out, list) and out and all(isinstance(x, str) for x in out):
            return self._ok(name)
        return self._no(name, f"expected a non-empty list of violations, got {out!r:.120}")

    def clean(self, name, fn, *args, **kw):
        """Acceptance MUST be an empty violations list."""
        try:
            out = fn(*args, **kw)
        except Exception as e:
            return self._no(name, f"expected acceptance (empty list), got {type(e).__name__}: {e}")
        if out == []:
            return self._ok(name)
        return self._no(name, f"expected acceptance (empty list), got {out!r:.200}")

    def value(self, name, fn, *args, pred=None, expect=None, **kw):
        """Acceptance MUST be a value; an exception is a failure."""
        try:
            out = fn(*args, **kw)
        except Exception as e:
            return self._no(name, f"expected a value, got {type(e).__name__}: {e}")
        if expect is not None and out != expect:
            return self._no(name, f"expected {expect!r:.80}, got {out!r:.80}")
        if pred is not None and not pred(out):
            return self._no(name, f"value failed its predicate: {out!r:.120}")
        return self._ok(name)

    def holds(self, name, condition, why="property does not hold"):
        return self._ok(name) if condition else self._no(name, why)


def load_kernel(root):
    import importlib.util, importlib.machinery, os
    path = os.path.join(root, "scripts", "spec-anchored")
    spec = importlib.util.spec_from_loader(
        "sa", importlib.machinery.SourceFileLoader("sa", path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    globals()["DEFAULT_EXC"] = getattr(mod, "ContractViolation", ValueError)
    return mod
