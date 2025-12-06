# Obsidian MCP Server Setup

Claude Code can connect to Obsidian vaults via Model Context Protocol (MCP) for programmatic access to vault operations: searching, reading, writing, and link management.

## Prerequisites

**Required Obsidian Plugins:**

1. **Local REST API** (coddingtonbear/obsidian-local-rest-api)
   - Provides HTTP/HTTPS API access to vault
   - Generates API key and configures ports
   - Install from Community Plugins

2. **MCP Tools** (jacksteamdev/obsidian-mcp-tools)
   - Provides MCP server binary for Claude Code integration
   - Install from Community Plugins
   - Location: `.obsidian/plugins/mcp-tools/bin/mcp-server`

## Configuration Steps

### 1. Extract API Configuration

The Local REST API plugin stores credentials in `.obsidian/plugins/obsidian-local-rest-api/data.json`:

```json
{
  "port": 27124,
  "insecurePort": 27123,
  "apiKey": "b2b34e3288227948535f70a45fd4a33754d79bdf77e67a0c2be9e61b6e8455fb"
}
```

Extract these values:
- `apiKey` → OBSIDIAN_API_KEY
- `port` → OBSIDIAN_HTTPS_PORT
- `insecurePort` → OBSIDIAN_HTTP_PORT

### 2. Register MCP Server with Claude Code

Use the `claude mcp add` command (do NOT manually edit config files):

```bash
claude mcp add --transport stdio obsidian \
  --env OBSIDIAN_API_KEY=<your-api-key> \
  --env OBSIDIAN_HOST=127.0.0.1 \
  --env OBSIDIAN_HTTPS_PORT=27124 \
  --env OBSIDIAN_HTTP_PORT=27123 \
  -- .obsidian/plugins/mcp-tools/bin/mcp-server
```

**Important Notes:**
- Replace `<your-api-key>` with the actual key from REST API plugin
- Server binary path is relative to vault root
- This registers the server in `~/.claude.json` (user global config)
- Do NOT create `.claude/mcp.json` manually - Claude Code ignores project-level MCP configs

### 3. Verify Connection

```bash
# List all MCP servers
claude mcp list

# Should show:
# ✓ obsidian - Connected
```

In Claude Code session:

```markdown
Can you check the Obsidian server status?
```

Claude will use `mcp__obsidian__get_server_info` to verify connection.

## Available MCP Tools

Once connected, Claude Code can use these Obsidian operations:

### Search and Discovery

- `mcp__obsidian__search_vault_simple` - Text search across vault
- `mcp__obsidian__search_vault_smart` - Semantic search
- `mcp__obsidian__search_vault` - Dataview DQL or JsonLogic queries
- `mcp__obsidian__list_vault_files` - List files in directory

### File Operations

- `mcp__obsidian__get_vault_file` - Read file content (markdown or JSON)
- `mcp__obsidian__create_vault_file` - Create or update file
- `mcp__obsidian__append_to_vault_file` - Append content
- `mcp__obsidian__patch_vault_file` - Update specific sections (heading, block, frontmatter)
- `mcp__obsidian__delete_vault_file` - Delete file

### Active File Operations

Work with currently open file in Obsidian:

- `mcp__obsidian__get_active_file` - Read currently open file
- `mcp__obsidian__update_active_file` - Replace active file content
- `mcp__obsidian__append_to_active_file` - Append to active file
- `mcp__obsidian__patch_active_file` - Update section in active file
- `mcp__obsidian__delete_active_file` - Delete currently open file

### Other Operations

- `mcp__obsidian__show_file_in_obsidian` - Open file in Obsidian UI
- `mcp__obsidian__fetch` - Fetch web page content as markdown
- `mcp__obsidian__execute_template` - Run Templater templates with arguments

## Common Use Cases

### Find Broken Links

```markdown
Search the vault for broken wiki links like [[missing-file]]
```

Claude uses `search_vault_simple` to find all `[[` patterns and verify targets exist.

### Bulk Link Updates

```markdown
Rename all links from [[old-name]] to [[new-name]]
```

Claude reads files, updates links with regex, writes back with proper error handling.

### Create Requirements from Template

```markdown
Create 10 requirement notes from this CSV with proper frontmatter
```

Claude uses `create_vault_file` to generate structured notes programmatically.

### Validate Vault Consistency

```markdown
Check that all requirement files have valid frontmatter and tags
```

Claude reads all files, validates YAML, reports inconsistencies.

### Update Frontmatter Field

```markdown
Update the status field to "active" in all draft requirements
```

Claude uses `patch_vault_file` with targetType="frontmatter" to update specific fields.

### Append to Daily Note

```markdown
Add this meeting summary to today's daily note
```

Claude uses `append_to_vault_file` to add content without replacing existing notes.

## Troubleshooting

### Connection Fails

- Verify both plugins installed and enabled in Obsidian
- Check API key matches REST API plugin config
- Ensure ports match (HTTPS 27124, HTTP 27123 are defaults)
- Restart Obsidian after plugin installation
- Use `claude mcp remove obsidian` and re-add if stale

### Tools Not Available

- Verify connection: `claude mcp list` shows "✓ Connected"
- Restart Claude Code session
- Check Obsidian REST API plugin is running (status bar icon)

### Permission Errors

- API key must be valid and not expired
- REST API plugin may need re-enable in Obsidian settings
- Check `.obsidian/plugins/obsidian-local-rest-api/data.json` readable

### Wrong Plugin Path

- MCP Tools plugin location: `.obsidian/plugins/mcp-tools/` ✅
- NOT: `.obsidian/plugins/obsidian-mcp-tools/` ❌
- Server binary: `mcp-tools/bin/mcp-server` ✅

## Configuration Example

Complete working example:

```bash
# Extract API key from REST API plugin
API_KEY=$(cat .obsidian/plugins/obsidian-local-rest-api/data.json | jq -r '.apiKey')

# Add MCP server
claude mcp add --transport stdio obsidian \
  --env OBSIDIAN_API_KEY=$API_KEY \
  --env OBSIDIAN_HOST=127.0.0.1 \
  --env OBSIDIAN_HTTPS_PORT=27124 \
  --env OBSIDIAN_HTTP_PORT=27123 \
  -- .obsidian/plugins/mcp-tools/bin/mcp-server

# Verify
claude mcp list
```

## Security Notes

- API key provides full read/write access to vault
- Only configure MCP server for vaults you control
- API key is stored in `~/.claude.json` (user global config)
- REST API plugin binds to localhost only (not exposed to network)
- Both HTTP and HTTPS ports are required for full functionality
