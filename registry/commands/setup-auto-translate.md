---
description: Setup auto-translate GitHub Action workflow with customizable translation
---

You are setting up an auto-translate GitHub Action workflow. This workflow:
- Syncs from an upstream repository (optional)
- Translates documentation using OpenAI Codex
- Creates automated PRs with translated content

## Step 1: Gather Translation Configuration

Use the AskUserQuestion tool to collect:

1. **Translation Direction**: What languages are being translated?
   - Header: "Languages"
   - Question: "What translation are you setting up?"
   - Options:
     - label: "Chinese → English"
       description: "Translate Chinese documentation to English"
     - label: "Japanese → English"
       description: "Translate Japanese documentation to English"
     - label: "Custom languages"
       description: "I'll specify source and target languages in 'Other' field (format: 'SourceLang → TargetLang')"
   - multiSelect: false

2. **Target Branch Name**: Where translations will be committed
   - Header: "Branch"
   - Question: "What branch should translations be committed to?"
   - Options:
     - label: "language/english"
       description: "Default English translation branch"
     - label: "i18n/en"
       description: "Internationalization naming convention"
     - label: "Custom branch"
       description: "I'll specify branch name in 'Other' field"
   - multiSelect: false

3. **Files to Translate**: Which files should be processed?
   - Header: "File Scope"
   - Question: "Which files should be translated?"
   - Options:
     - label: "All markdown files"
       description: "Translate all .md files in the repository"
     - label: "Documentation only"
       description: "Translate README.md, docs/, and agent/command definitions"
     - label: "Custom pattern"
       description: "I'll specify file patterns in 'Other' field (e.g., '*.md, docs/, agents/')"
   - multiSelect: false

4. **Preservation Rules**: What should NOT be translated?
   - Header: "Preserve"
   - Question: "What content should be preserved (not translated)?"
   - Options:
     - label: "Code and metadata"
       description: "Preserve YAML frontmatter keys, JSON keys, code blocks, technical identifiers"
     - label: "Technical terms only"
       description: "Preserve code blocks and file paths, translate all prose"
     - label: "Custom rules"
       description: "I'll specify preservation rules in 'Other' field"
   - multiSelect: false

## Step 2: Gather API and Repository Configuration

Use the AskUserQuestion tool to collect:

1. **OpenAI API Key**: Required for Codex translation
   - Header: "API Key"
   - Question: "What is your OpenAI API key for Codex translation?"
   - Options:
     - label: "I have an API key"
       description: "I'll provide my OpenAI API key in the 'Other' field"
     - label: "Skip for now"
       description: "I'll set this up later manually"
   - multiSelect: false

2. **Upstream Repository**: Optional sync source
   - Header: "Upstream"
   - Question: "Do you want to sync from an upstream repository before translating?"
   - Options:
     - label: "Yes, sync from upstream"
       description: "Provide upstream repo in format: owner/repo (e.g., 'original/repo')"
     - label: "No upstream sync"
       description: "Just translate the current repository content"
   - multiSelect: false

3. **Personal Access Token**: Optional for PR creation
   - Header: "PAT Token"
   - Question: "Do you want to provide a Personal Access Token for creating PRs?"
   - Options:
     - label: "Use PAT"
       description: "I'll provide a PAT with repo permissions in the 'Other' field"
     - label: "Use default GITHUB_TOKEN"
       description: "Use the default GitHub Actions token (may have limited permissions)"
   - multiSelect: false

## Step 3: Build Custom Translation Prompt

Based on the user's answers in Step 1, construct a custom Codex prompt that includes:

1. **Mission statement** with source → target language
2. **Repository context** (ask user to describe their repo/project)
3. **Files to process** (based on File Scope answer)
4. **Preservation rules** (based on Preserve answer and any custom rules)
5. **Translation quality standards** (terminology consistency, technical accuracy)
6. **Execution steps** (scan, read, translate, preserve formatting, write, stage)

Example prompt structure:
```
# Mission: Translate [Project Name] from [Source] to [Target]

## Repository Context
[User-provided description of their project]

## Files to Process
[Based on user's file scope selection]

## Critical Preservation Rules
### DO NOT TRANSLATE:
[Based on user's preservation selection]

### DO TRANSLATE:
[Prose, documentation, comments, etc.]

## Translation Quality Standards
[Terminology mappings, technical accuracy, natural language]

## Execution Steps
1. Scan repository for files matching patterns
2. Read each file and identify source language text
3. Apply translation rules based on file type
4. Preserve all formatting
5. Write back to same file path
6. Stage changes with git add
```

## Step 4: Set GitHub Repository Secrets

After gathering the information, use the `gh` CLI to set secrets:

```bash
# Set OpenAI API Key (required)
gh secret set OPENAI_API_KEY --body "user-provided-key"

# Set upstream repo if provided (optional)
gh secret set UPSTREAM_REPO --body "owner/repo"

# Set upstream branch if different from main (optional)
gh secret set UPSTREAM_BRANCH --body "branch-name"

# Set PAT token if provided (optional)
gh secret set PAT_TOKEN --body "user-provided-pat"
```

## Step 5: Generate Custom Workflow File

Create `.github/workflows/auto-translate.yml` based on:
- User's target branch name (from Step 1)
- User's custom translation prompt (from Step 3)
- Upstream configuration (from Step 2)

Use the template from `/Users/cameron/Projects/ComplexMissionManager/.github/workflows/auto-translate.yml` but:
1. Replace `TARGET_BRANCH: language/english` with user's branch choice
2. Replace the hardcoded Codex prompt with the custom prompt built in Step 3
3. Update commit messages and PR titles to reflect the actual translation (not just "Chinese to English")

Example customizations:
```yaml
env:
  TARGET_BRANCH: [user-specified-branch]

# In the Codex step:
with:
  prompt: |
    [User's custom translation prompt from Step 3]

# In commit step:
git commit -m "feat(lang): translate to [target-language]"

# In PR creation:
--title "chore: translate documentation to [target-language]"
```

## Step 6: Confirm Setup

After setting secrets and creating the workflow:

1. List the configured secrets (names only, not values):
   ```bash
   gh secret list
   ```

2. Show the workflow file location and content summary:
   ```bash
   cat .github/workflows/auto-translate.yml | head -20
   ```

3. Inform the user:
   - **Secrets configured**: List which secrets were set
   - **Workflow location**: `.github/workflows/auto-translate.yml`
   - **Target branch**: Where translations will be committed
   - **Translation**: Source → Target languages
   - **How to trigger**:
     - Runs automatically nightly at 3:23 AM UTC
     - Manual trigger: `gh workflow run auto-translate.yml`
   - **Next steps**:
     - Commit the workflow file: `git add .github/workflows/auto-translate.yml`
     - Push to GitHub: `git push`
     - Test with manual trigger: `gh workflow run auto-translate.yml`
     - Monitor workflow runs: `gh run list --workflow=auto-translate.yml`
     - Review the generated PR when it completes

## Important Notes

- **OpenAI API key** is required for Codex translation to work
- **UPSTREAM_REPO** and **UPSTREAM_BRANCH** are optional - if not set, translates current branch
- **PAT_TOKEN** is optional - if not set, uses default GITHUB_TOKEN (may have limited PR permissions)
- Secrets are encrypted and only visible to GitHub Actions
- The workflow creates a new branch with translations and opens a PR
- Translation prompt is fully customizable based on your project needs
- You can edit the workflow file later to adjust the translation prompt or settings

## Error Handling

If `gh` CLI is not installed or not authenticated:
- Check: `gh auth status`
- Authenticate: `gh auth login`
- Install gh: `brew install gh` (macOS)

If workflow creation fails:
- Ensure you have write permissions to the repository
- Verify the workflow file syntax with: `gh workflow view auto-translate.yml`
- Check GitHub Actions is enabled in repository settings

## Customization Tips

After initial setup, you can customize:
- **Cron schedule**: Edit line 5 to change when the workflow runs
- **Translation prompt**: Edit the Codex step to refine translation rules
- **File patterns**: Add file filters in the prompt to target specific files
- **Branch strategy**: Change target branch name or base branch in the workflow
- **PR behavior**: Customize PR title, body, labels, reviewers in the workflow
