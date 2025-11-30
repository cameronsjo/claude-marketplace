# Plugin Builder TUI - Quick Start Guide

## Launching the TUI

```bash
cd /Users/cameron/Projects/claude-marketplace
python scripts/plugin-builder.py
```

Or run the TUI module directly:

```bash
python -m scripts.plugin_builder_tui
```

## Screen Overview

### Dashboard (press `d`)
- View marketplace statistics
- See health status and validation issues
- Check for orphaned assets
- Quick overview of plugin ecosystem

### Plugins (press `p`)
- Browse all plugins
- View plugin contents (commands, agents, skills)
- Add assets to plugins (press `a`)
- Remove assets from plugins (press `r`)
- Create new plugins (press `n` for CLI instructions)

### Assets (press `a`)
- Browse all registry assets by type (Commands, Agents, Skills)
- Filter assets (press `f` or `Ctrl+F`)
- Clear filter (press `Esc`)
- View which plugins use each asset
- Delete assets (press `Delete`, requires confirmation)

## Common Workflows

### Adding an Asset to a Plugin

1. Press `p` to go to Plugins screen
2. Select a plugin from the left pane (arrow keys + Enter)
3. Press `a` to open Add Asset modal
4. Switch between Commands/Agents/Skills tabs if needed (click or Tab)
5. Select an asset from the list (arrow keys)
6. Press `Enter` or click "Add" button
7. Asset is now in the plugin

### Removing an Asset from a Plugin

1. Press `p` to go to Plugins screen
2. Select a plugin from the left pane
3. Press `r` to open Remove Asset modal
4. Select the asset to remove (arrow keys)
5. Press `Enter` or click "Remove" button
6. Asset is removed from the plugin

### Finding Assets

**Option 1: Global Search**
1. Press `/` or `Ctrl+F` from any screen
2. Type your search query (minimum 2 characters)
3. Browse results (up to 20 shown)
4. Press `Enter` to select or `Esc` to close

**Option 2: Filter in Assets Screen**
1. Press `a` to go to Assets screen
2. Press `f` to focus filter input
3. Type to filter the current tab
4. Press `Esc` to clear filter
5. Switch tabs to filter different asset types

### Validating Plugins

1. Press `v` from any screen
2. System checks all symlinks
3. Notification shows results:
   - Success: All valid
   - Warning: Issues but not broken
   - Error: Broken symlinks found

## Keyboard Shortcuts

### Navigation
- `d` - Dashboard
- `p` - Plugins
- `a` - Assets
- `Esc` - Back / Close modal
- `Tab` - Navigate between panes
- `Arrow Keys` - Navigate lists/tables

### Actions
- `/` - Open search
- `?` - Show help
- `v` - Validate symlinks
- `q` - Quit

### In Plugins Screen
- `a` - Add asset to selected plugin
- `r` - Remove asset from selected plugin
- `n` - Show new plugin instructions

### In Assets Screen
- `f` - Focus filter input
- `Ctrl+F` - Focus filter input (alternative)
- `Esc` - Clear filter (if empty, focus table)
- `Delete` - Delete selected asset

### In Modals
- `Esc` - Cancel and close
- `Enter` - Confirm action
- `Arrow Keys` - Navigate options

## Tips and Tricks

### Modal Navigation
- Modals automatically focus on the primary interactive element
- Use Tab to move between buttons
- Press Esc anytime to cancel

### Plugin Selection
- Your selected plugin is preserved after add/remove operations
- Highlight stays on the same plugin for easy multiple operations

### Visual Feedback
- Focused elements have brighter borders in primary color (blue)
- Buttons show bold text when focused
- Disabled options are dimmed
- Counts shown in modal titles (e.g., "5 available")

### Asset Type Indicators
- Commands shown with `/` prefix in plugin tree
- Asset types shown as sections in Remove Asset modal
- Type shown in parentheses in search results

### Filtering
- Filter applies to name and description
- Filter is case-insensitive
- Each tab (Commands/Agents/Skills) maintains independent filter

### Notifications
- Blue: Information (success messages)
- Yellow: Warnings (already exists, etc.)
- Red: Errors (failures, broken symlinks)

## Common Issues

### "Select a plugin first"
- You need to select a plugin from the list before adding/removing assets
- Click or press Enter on a plugin in the left pane

### "No available assets"
- All assets of that type are already in the plugin
- Switch to a different asset type tab
- Or remove an asset first

### "Asset already exists"
- The asset is already in the plugin
- Check the plugin tree on the right

### Symlink Validation Failures
- Run `v` to validate and see specific issues
- Broken symlinks mean registry assets were deleted
- Warnings mean symlinks point outside registry

### Modal Won't Open
- Ensure a plugin is selected first
- Check notifications for error messages

## Best Practices

1. **Validate Regularly**: Press `v` after making changes to ensure symlinks are healthy

2. **Use Search for Discovery**: Use `/` to find assets across all types rather than browsing tabs

3. **Check Before Removing**: Look at the "Used By" column in Assets screen to see if removing will affect other plugins

4. **Organize by Plugin**: Group related commands, agents, and skills into logical plugins

5. **Keep Assets DRY**: If multiple plugins need the same asset, add it to both - registry maintains single source

6. **Review Orphans**: Check Dashboard for orphaned assets that could be deleted

7. **Use Keyboard**: Keyboard navigation is faster than mouse for repeated operations

## Getting Help

- Press `?` anytime for keyboard shortcuts
- Check `/Users/cameron/Projects/claude-marketplace/docs/tui-improvements.md` for technical details
- Run CLI with `--help` for command-line options

## Exiting

Press `q` to quit at any time. All changes are saved immediately (symlinks created/removed in real-time).
