#!/usr/bin/env python3
"""Portable per-step runner with process-GROUP containment.

`timeout(1)` is not present everywhere, and the shell fallback ran a hung
step to completion, so the budget was real only on some machines. This
runner also owns the group's lifecycle on BOTH paths: the previous version
cleaned up only on timeout, so a leader that exited 0 after spawning a
background child left that child writing into a tree the gate had already
judged (closure v5, P0-02).

    python3 scripts/run-step.py <seconds> <command> [args...]

Exit 124 on timeout, mirroring timeout(1); otherwise the leader's code.

BOUNDARY, stated honestly: this is **process-group containment**. A
descendant that calls setsid() leaves the group and is NOT contained here
— containing it requires an outer authority (cgroup, job object, or a
disposable CI container), which is where that guarantee belongs. The
runner does not pretend to own an arbitrary process tree.
"""
import sys, os, signal, subprocess, time
sys.dont_write_bytecode = True

if len(sys.argv) < 3:
    sys.exit("usage: run-step.py <seconds> <command> [args...]")

budget = int(sys.argv[1])
_posix = hasattr(os, "killpg") and hasattr(os, "setsid")
proc = subprocess.Popen(sys.argv[2:], start_new_session=_posix)
pgid = None
if _posix:
    try:
        pgid = os.getpgid(proc.pid)
    except ProcessLookupError:
        pgid = None

timed_out = False
try:
    rc = proc.wait(timeout=budget)
except subprocess.TimeoutExpired:
    timed_out = True
    rc = 124
finally:
    # Always reclaim the group — after a normal exit too. A gate command
    # never intentionally leaves a background member behind.
    if pgid is not None:
        for sig in (signal.SIGTERM, signal.SIGKILL):
            try:
                os.killpg(pgid, sig)
            except (ProcessLookupError, PermissionError):
                break
            time.sleep(0.2)
    elif timed_out:
        proc.kill()
        print("   ^ note: descendants are not contained on this platform",
              file=sys.stderr)
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        pass

if timed_out:
    print("   ^ killed after %ds (process-group containment)" % budget, file=sys.stderr)
sys.exit(rc)
