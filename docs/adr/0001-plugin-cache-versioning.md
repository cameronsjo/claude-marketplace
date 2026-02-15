# ADR-0001: Plugin Cache Versioning Strategy

- **Status:** Accepted
- **Date:** 2026-02-15
- **Author:** Cameron Sjo

## Context

The Claude Code plugin system caches installed plugins at
`~/.claude/plugins/cache/<marketplace>/<plugin>/<cache-key>/`. The cache key
determines identity -- if it matches an existing directory, old content is served.

Personal plugins use semver from `plugin.json` as the cache key. This requires
auto-bump GitHub Actions workflows on every push to avoid stale cache (same
version = old content). The workflows create merge conflicts, noisy commit
history, and CI complexity for what is fundamentally a cache-busting concern.

## Discovery: How Anthropic's Official Plugins Work

Reverse-engineering the official marketplace (`anthropics/claude-plugins-official`)
reveals three plugin archetypes:

| Archetype | plugin.json version | Cache key | Count | Examples |
|-----------|:-------------------:|-----------|:-----:|---------|
| Versioned | `"1.0.0"` | `1.0.0/` | 4 | claude-code-setup, code-simplifier |
| Versionless | **Field omitted** | `2cd88e7947b7/` (git SHA) | 10 | code-review, playwright, feature-dev |
| Minimal | **No plugin.json** | `1.0.0/` (fallback) | 5 | typescript-lsp, gopls-lsp |

**Cache key derivation chain (corrected):**

```
plugin.json.version ?? marketplace.json.version ?? gitCommitSha ?? "1.0.0"
```

All 10 SHA-keyed plugins share the same SHA (`2cd88e7947b7`) because they come
from one monorepo commit. Crucially, these are Anthropic's **newer** plugins.
The older ones have version fields. This indicates an intentional migration away
from semver-as-cache-key.

**Why the official marketplace hits SHA immediately:** Anthropic's marketplace is
a monorepo. The per-plugin entries in its `marketplace.json` do NOT carry version
fields -- only `name`, `description`, and `source`. So for versionless plugins
the chain falls straight through to git SHA. Hub registries (like our workbench)
with per-plugin version fields in `marketplace.json` create a second fallback
layer that must also be cleared.

**The implication:** for hub-style registries, removing `version` from BOTH
`plugin.json` (per-repo) AND `marketplace.json` (hub registry) is required.
The system then falls back to git SHA automatically.

## Decision

**Remove the `version` field from `plugin.json` in all personal plugins AND from
all plugin entries in `marketplace.json` (the hub registry).**

The system will use git commit SHAs as cache keys, matching what Anthropic does
for their newer plugins.

### What this solves

| Problem | Before (semver) | After (SHA) |
|---------|:---------------:|:-----------:|
| Stale cache | Same version = old content | Impossible -- every commit has unique SHA |
| Auto-bump workflows | Required on every push (8 plugins) | Unnecessary -- delete them |
| Merge conflicts | Local vs CI bump `plugin.json` | Gone -- no version field to conflict |
| Commit noise | "chore: auto-bump version [skip ci]" | Gone |

### What this doesn't solve

| Concern | Status | Mitigation |
|---------|--------|------------|
| Cache accumulation | Still happens (SHA dirs pile up) | Cleanup script in `setup-marketplaces.sh` (already added) |
| Human readability | `a3f8b2c/` vs `2.1.17/` | `installed_plugins.json` tracks install dates; `git log --oneline` for history |
| Display version | Lost from `plugin.json` and `marketplace.json` | Use `git log --oneline` or git tags for release tracking |
| Installed version in `installed_plugins.json` | Shows SHA instead of semver | Acceptable -- it's a machine file, not user-facing |

### What to keep

- **Cleanup script in `setup-marketplaces.sh`** -- SHA directories accumulate
  just like version directories
- **`name` and `description` in `plugin.json`** -- still required for plugin
  identity and registration
- **`name`, `description`, and `source` in `marketplace.json`** -- required for
  plugin discovery. Only `version` is removed

## Migration Plan

1. Remove `version` from `plugin.json` in all 10 personal plugins
2. Remove `version` from all plugin entries in `marketplace.json` (hub registry)
3. Push all repos + push workbench (must push workbench before marketplace update)
4. Run `claude plugin marketplace update workbench`
5. Reinstall all plugins: `claude plugin install <plugin>@workbench`
6. Verify cache directories use SHAs (12-character git SHA prefix)
7. Run stale cache cleanup (in `setup-marketplaces.sh` or manually)
8. Delete auto-bump GitHub Actions workflows from personal repos

### Migration gotchas discovered during execution

- **Marketplace.json is a fallback layer**: Initial migration only removed
  `plugin.json` versions. Cache keys fell back to `marketplace.json` versions,
  not git SHAs. Both layers must be cleared
- **Homelab was missed**: The 10th personal plugin (`homelab`) was not in the
  original list of 8 (it lives at `~/Projects/homelab/`, not under
  `claude-configurations/`)
- **Marketplace update re-fetches**: After removing marketplace.json versions
  and running `marketplace update`, the CLI re-clones repos and picks up the
  latest commit SHA. The `rules` plugin changed from `15d869a76c57` to
  `8fbec66c29cd` between reinstalls because the remote had newer commits

## Consequences

- Auto-bump workflows eliminated across 10 repos -- less CI, fewer conflicts
- Cache staleness becomes structurally impossible
- Version progression loses automatic tracking -- must check git log for history
- Existing semver cache directories become orphans -- cleanup script handles them
- No human-readable version displayed in plugin listings (acceptable tradeoff)
- Forked plugins (obra/superpowers) retain semver from upstream `plugin.json` --
  migration only applies to repos we control
