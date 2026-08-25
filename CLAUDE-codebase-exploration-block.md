# Block for root CLAUDE.md — Codebase exploration

Operational version. Add as a subsection in your root CLAUDE.md.

> The tool names below (grepika, tilth, cachebro) are an **example
> stack** — swap in your project's equivalents. The discipline (outline
> before content, structural query before whole-file reads, native Read
> before edits) is what matters, not these specific tools.

---

## Codebase exploration

**Principle:** minimize context consumption. Read outlines before specific
sections; open a full file only when you need literal content (usually
because you're going to edit it).

### Tool hierarchy

| Question                       | Primary tool                      | Method                                                                |
| ------------------------------ | --------------------------------- | --------------------------------------------------------------------- |
| Directory overview             | `grepika`                         | `toc`                                                                 |
| Search code (NL or regex)      | `grepika`                         | `search`                                                              |
| File structure                 | `grepika`                         | `outline` → `get` with line range                                     |
| Where is X defined?            | `tilth`                           | `search` — definition-first                                           |
| What calls X?                  | `tilth`                           | `search kind:callers`                                                 |
| Config, JSON, markdown, docs   | `cachebro`                        | `cachebro_read_file` (hash-based caching)                             |
| Before editing a file          | Native `Read`                     | required precondition for `Edit`/`Write`/`str_replace`; see note below |

### Edit precondition

`Edit`/`Write`/`str_replace` require a native `Read` of the target path in
the current session. **Only native `Read` satisfies this** — `cachebro`,
`grepika`, `tilth`, `Grep`, and even `Bash` that wrote the file do NOT
count.

Practical guidance:

- **Large files:** use `Read` with `view_range` to load only the region
  you'll edit. Saves tokens; the precondition is still satisfied.
- **Multiple edits in same file:** prefer `MultiEdit` — a single `Read`
  enables several atomic substitutions in one call.
- **New file:** `Write` does NOT require prior `Read` if the file doesn't
  exist yet. Use `Write` directly.

**Anti-pattern:** reading 5+ files to understand a flow — almost always a
structural query in `grepika`/`tilth` resolves it in one call.

Repos: [grepika](https://github.com/agentika-labs/grepika),
[tilth](https://github.com/jahala/tilth),
[cachebro](https://github.com/glommer/cachebro).
