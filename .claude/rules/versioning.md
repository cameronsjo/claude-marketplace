# Versioning

Auto-versioning on push to main via conventional commits.

## Commit Prefixes

| Prefix | Bump | Example |
|--------|------|---------|
| `feat!:` or `BREAKING CHANGE` | MAJOR | 1.0.0 -> 2.0.0 |
| `feat:` | MINOR | 1.0.0 -> 1.1.0 |
| `fix:` | PATCH | 1.0.0 -> 1.0.1 |
| `chore:`, `docs:`, `refactor:` | none | no release |

## Release Workflow

The `.github/workflows/release.yml` workflow:

1. Parses commit messages since last tag
2. Determines version bump
3. Updates version in `marketplace.json`
4. Creates git tag
5. Publishes GitHub release

## Commit Message Format

```
type(scope): description

[optional body]

[optional footer]
```

Examples:

- `feat(core): add turbo mode command`
- `fix(security): correct OWASP check for XSS`
- `feat!: remove deprecated registry architecture`
