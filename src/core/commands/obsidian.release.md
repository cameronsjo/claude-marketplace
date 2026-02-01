---
description: Trigger Obsidian plugin release (beta, RC, or stable)
category: version-control-git
argument-hint: "[beta|rc|stable]"
allowed-tools: Bash, Read, Edit, Glob, Grep
---

# Claude Command: Obsidian Release

## Usage

```bash
/obsidian.release beta     # Create beta release for BRAT
/obsidian.release rc       # Create release candidate
/obsidian.release stable   # Prepare stable release (via Release Please)
/obsidian.release          # Interactive - ask which type
```

## Release Types

### Beta Release (`[beta]`)

For BRAT users to test in-progress changes:

- Triggered by `[beta]` keyword in commit message
- Creates prerelease like `1.2.0-beta.5+abc1234`
- Available immediately via BRAT
- Can push multiple betas without version bump

### Release Candidate (`[rc]`)

For final testing before stable:

- Triggered by `[rc]` keyword in commit message
- Creates prerelease like `1.2.0-rc.1`
- Cleans up previous beta releases
- Signals "ready for stable" to testers

### Stable Release

For production/community plugin listing:

- Managed by Release Please PR
- Merge the "chore(main): release X.Y.Z" PR
- Automatically builds and uploads assets
- Cleans up all prereleases for this version

## Step-by-Step Process

### 1. Pre-flight Checks

Before any release:

```bash
# Verify clean working directory
git status

# Ensure tests pass
npm test

# Ensure build succeeds
npm run build

# Check current version
cat manifest.json | jq '.version'

# Check for open Release Please PR
gh pr list --state open --search "chore(main): release"
```

### 2. Beta Release

```bash
# Option A: Add [beta] to new commit
git add .
git commit -m "feat: add new feature [beta]"
git push

# Option B: Amend last commit with [beta]
git commit --amend -m "$(git log -1 --format=%B) [beta]"
git push --force-with-lease
```

The beta-release.yml workflow will:

1. Detect `[beta]` keyword
2. Generate version: `{next-version}-beta.{commit-count}+{short-sha}`
3. Update manifest.json temporarily
4. Build plugin
5. Create GitHub prerelease
6. Upload main.js, manifest.json, styles.css

### 3. Release Candidate

```bash
# Add [rc] to commit message
git commit -m "chore: prepare release candidate [rc]"
git push
```

The rc-release.yml workflow will:

1. Detect `[rc]` keyword
2. Generate version: `{next-version}-rc.{count}`
3. Delete all beta releases for this version
4. Create RC prerelease

### 4. Stable Release

```bash
# Check for Release Please PR
gh pr list --state open --search "chore(main): release"

# Review the PR changes
gh pr view {pr-number}

# Merge when ready
gh pr merge {pr-number} --merge
```

Release Please will:

1. Update CHANGELOG.md
2. Bump version in package.json and manifest.json
3. Update versions.json
4. Create GitHub release
5. Upload assets
6. Delete all prereleases for this version

## Checking Release Status

```bash
# List recent releases
gh release list --limit 10

# View specific release
gh release view v1.2.0

# Check GitHub Actions status
gh run list --limit 5
```

## Fixing Release Issues

### Beta didn't trigger

Check commit message includes `[beta]`:

```bash
git log -1 --format=%B
# If missing, amend:
git commit --amend -m "$(git log -1 --format=%B) [beta]"
git push --force-with-lease
```

### Version mismatch in BRAT

BRAT requires manifest.json version to match release tag:

```bash
# Check release assets
gh release view v1.2.0-beta.1 --json assets

# Re-upload fixed manifest if needed
gh release upload v1.2.0-beta.1 manifest.json --clobber
```

### Delete bad release

```bash
# Delete release and tag
gh release delete v1.2.0-beta.1 --yes --cleanup-tag
```

### Force versions.json update

If versions.json is out of sync:

```bash
# Get current version
VERSION=$(jq -r '.version' manifest.json)
MIN_VERSION=$(jq -r '.minAppVersion' manifest.json)

# Update versions.json
jq --arg v "$VERSION" --arg m "$MIN_VERSION" '. + {($v): $m}' versions.json > tmp.json
mv tmp.json versions.json

git add versions.json
git commit -m "chore: update versions.json for $VERSION"
git push
```

## BRAT Installation Instructions

For testers installing via BRAT:

1. Install BRAT from Community Plugins
2. Open BRAT settings
3. Click "Add Beta Plugin"
4. Enter: `{github-username}/{repo-name}`
5. Enable the plugin

## Version Numbering Guide

| Change Type | Version Bump | Example |
|-------------|--------------|---------|
| Breaking change | Major | 1.0.0 → 2.0.0 |
| New feature | Minor | 1.0.0 → 1.1.0 |
| Bug fix | Patch | 1.0.0 → 1.0.1 |
| Beta | Prerelease | 1.1.0-beta.1 |
| RC | Prerelease | 1.1.0-rc.1 |

Use conventional commits:

- `feat:` → minor bump
- `fix:` → patch bump
- `feat!:` or `BREAKING CHANGE:` → major bump

## Output Summary

After triggering release:

```
🚀 Release triggered!

Type: Beta
Version: 1.2.0-beta.5+abc1234
Commit: feat: add new feature [beta]

📋 Next steps:
   - Monitor: gh run watch
   - Verify: gh release view 1.2.0-beta.5+abc1234
   - Test: Install via BRAT

🔗 BRAT install: username/repo-name
```
