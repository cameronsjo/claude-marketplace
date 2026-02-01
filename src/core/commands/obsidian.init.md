---
description: Initialize or upgrade an Obsidian plugin project with modern 2025 tooling
category: project-setup
argument-hint: "[plugin-name]"
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# Claude Command: Obsidian Plugin Init

## Usage

```bash
/obsidian.init                    # Initialize in current directory
/obsidian.init my-cool-plugin     # Create new plugin directory
```

## What This Command Does

Sets up a complete Obsidian plugin project with:

1. **Project Structure**: Standard directory layout (src/, tests/, .github/)
2. **TypeScript Config**: Strict mode, ES2018 target, proper module resolution
3. **Build System**: esbuild with hot-reload development
4. **Release Automation**: Release Please + BRAT beta channel
5. **CI/CD**: GitHub Actions for testing and releases
6. **Linting**: ESLint + Prettier configuration

## Step-by-Step Process

### 1. Check Current State

First, determine if this is a new project or upgrade:

- Check for existing `manifest.json` (Obsidian plugin marker)
- Check for existing `package.json`
- Check for existing `src/main.ts` or `main.ts`

### 2. Gather Required Information

If creating new plugin, ask for:

- **Plugin ID**: kebab-case identifier (e.g., `my-cool-plugin`)
- **Plugin Name**: Human-readable name (e.g., `My Cool Plugin`)
- **Description**: One-line description
- **Author**: Author name or GitHub username
- **Min Obsidian Version**: Default to `1.5.0`

### 3. Create/Update Files

#### manifest.json

```json
{
  "id": "{{plugin-id}}",
  "name": "{{plugin-name}}",
  "version": "1.0.0",
  "minAppVersion": "1.5.0",
  "description": "{{description}}",
  "author": "{{author}}",
  "authorUrl": "https://github.com/{{author}}",
  "isDesktopOnly": false
}
```

#### package.json

```json
{
  "name": "{{plugin-id}}",
  "version": "1.0.0",
  "description": "{{description}}",
  "main": "main.js",
  "scripts": {
    "dev": "node esbuild.config.mjs",
    "build": "tsc -noEmit -skipLibCheck && node esbuild.config.mjs production",
    "test": "jest",
    "lint": "eslint src --ext .ts",
    "format": "prettier --write src/**/*.ts"
  },
  "keywords": ["obsidian-plugin"],
  "author": "{{author}}",
  "license": "MIT",
  "devDependencies": {
    "@types/node": "^20.0.0",
    "@typescript-eslint/eslint-plugin": "^7.0.0",
    "@typescript-eslint/parser": "^7.0.0",
    "builtin-modules": "^3.3.0",
    "esbuild": "^0.20.0",
    "eslint": "^8.57.0",
    "jest": "^29.0.0",
    "obsidian": "latest",
    "prettier": "^3.0.0",
    "ts-jest": "^29.0.0",
    "typescript": "^5.4.0"
  }
}
```

#### tsconfig.json

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "inlineSourceMap": true,
    "inlineSources": true,
    "module": "ESNext",
    "target": "ES6",
    "allowJs": true,
    "noImplicitAny": true,
    "moduleResolution": "node",
    "importHelpers": true,
    "isolatedModules": true,
    "strictNullChecks": true,
    "strict": true,
    "lib": ["DOM", "ES5", "ES6", "ES7"]
  },
  "include": ["src/**/*.ts"]
}
```

#### esbuild.config.mjs

Use the standard Obsidian esbuild configuration with:

- Entry: `src/main.ts`
- Output: `main.js` (CommonJS)
- Target: ES2018
- External: obsidian, electron, codemirror, lezer, node builtins
- Dev mode: inline sourcemaps, watch
- Prod mode: minified, no sourcemaps

#### versions.json

```json
{
  "1.0.0": "1.5.0"
}
```

#### .gitignore

```
node_modules/
main.js
*.js.map
.DS_Store
```

### 4. Create Source Files

#### src/main.ts

Create minimal plugin skeleton with:

- Settings interface and defaults
- `onload()` with settings loading
- `onunload()` stub
- Settings tab placeholder

#### src/types.ts

```typescript
export interface PluginSettings {
  // Add settings here
}

export const DEFAULT_SETTINGS: PluginSettings = {
  // Add defaults here
};
```

#### src/settings.ts

Basic SettingTab implementation.

### 5. Setup GitHub Actions

#### .github/workflows/ci.yml

```yaml
name: CI

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "20.x"
          cache: "npm"
      - run: npm ci
      - run: npm run lint
      - run: npm run build
      - run: npm test
```

#### .github/workflows/release-please.yml

Full Release Please configuration that:

- Creates release PRs from conventional commits
- Updates versions.json automatically
- Builds and uploads release assets
- Cleans up prereleases on stable release

#### .github/workflows/beta-release.yml

BRAT beta channel workflow that:

- Triggers on `[beta]` keyword in commit
- Creates prerelease with semantic version
- Updates manifest.json version
- Attaches main.js, manifest.json, styles.css

### 6. Setup Release Please

#### release-please-config.json

```json
{
  "$schema": "https://raw.githubusercontent.com/googleapis/release-please/main/schemas/config.json",
  "packages": {
    ".": {
      "release-type": "node",
      "bump-minor-pre-major": true,
      "bump-patch-for-minor-pre-major": true,
      "extra-files": ["manifest.json"]
    }
  },
  "separate-pull-requests": false
}
```

#### .release-please-manifest.json

```json
{
  ".": "1.0.0"
}
```

### 7. Final Steps

1. Run `npm install` to install dependencies
2. Create initial git commit if new repo
3. Display summary of created files
4. Remind user to:
   - Update plugin ID in manifest.json if needed
   - Add plugin features in src/main.ts
   - Run `npm run dev` for development
   - Use conventional commits for releases

## Upgrade Mode

If existing Obsidian plugin detected:

1. Preserve existing src/ code
2. Update package.json dependencies
3. Add missing GitHub Actions
4. Add Release Please if not present
5. Migrate from rollup to esbuild if needed
6. Add TypeScript strict mode if not enabled

## Output

After completion, display:

```
✅ Obsidian plugin initialized!

📁 Created files:
   - manifest.json
   - package.json
   - tsconfig.json
   - esbuild.config.mjs
   - src/main.ts
   - src/types.ts
   - src/settings.ts
   - .github/workflows/ci.yml
   - .github/workflows/release-please.yml
   - .github/workflows/beta-release.yml

📦 Next steps:
   1. npm install
   2. npm run dev (start development)
   3. Commit with conventional commits
   4. Push to GitHub for CI/CD
```
