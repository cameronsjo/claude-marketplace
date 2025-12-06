# Chrome DevTools MCP Skill

Expert guidance for browser automation, performance testing, and debugging using Chrome DevTools MCP server with AI-powered interactions.

## Overview

This skill provides comprehensive knowledge for using Chrome DevTools MCP - a Model Context Protocol server that enables AI coding agents to control and inspect live Chrome browser instances. Perfect for automated testing, performance analysis, visual regression testing, and browser debugging.

## What is Chrome DevTools MCP?

Chrome DevTools MCP bridges AI assistants (like Claude Code) with Chrome's debugging capabilities through a standardized protocol. It provides 26 tools across:

- **Performance Analysis**: Record and analyze Chrome DevTools traces
- **Browser Automation**: Puppeteer-based reliable browser control
- **Network Inspection**: Monitor and debug API requests
- **Visual Testing**: Screenshots, device emulation, responsive testing
- **Debugging**: Console monitoring, JavaScript execution, DOM inspection

**Key Benefits:**
- No test framework boilerplate - use natural language
- Automatic waits and stability handling
- Built on battle-tested Puppeteer
- Full Chrome DevTools Protocol access
- Works with any MCP-compatible AI assistant

## When to Use This Skill

Use Chrome DevTools MCP skill for:

✅ **Performance Testing**
- Measure page load times and Core Web Vitals
- Identify rendering bottlenecks
- Analyze resource usage
- Compare before/after optimizations

✅ **Automated E2E Testing**
- User flow validation
- Form submission testing
- Multi-page navigation
- Authentication flows

✅ **Visual Regression Testing**
- Screenshot comparisons
- Responsive design validation
- Cross-device testing
- Component-level visual checks

✅ **Network Debugging**
- API request/response inspection
- Failed request debugging
- Header and timing analysis
- Request payload validation

✅ **Browser Debugging**
- Console error investigation
- JavaScript execution and inspection
- DOM state verification
- Breakpoint-free debugging

## Quick Start

### 1. Install Chrome DevTools MCP

**Claude Code (easiest):**
```bash
claude mcp add chrome-devtools npx chrome-devtools-mcp@latest
```

**Manual configuration (any MCP client):**
Add to your MCP configuration file:
```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest"]
    }
  }
}
```

### 2. Verify Setup

Run the validation script:
```bash
~/.claude/skills/chrome-devtools-mcp/scripts/validate-setup.sh
```

Or test with Claude Code:
```
Check the performance of https://developers.chrome.com
```

### 3. Start Testing

Try these example prompts with Claude Code:

**Performance:**
```
Measure the performance of https://example.com and identify any issues
```

**Form Testing:**
```
Test the registration form at https://example.com/signup with sample data
```

**Visual Testing:**
```
Take screenshots of https://example.com at desktop, tablet, and mobile sizes
```

**Network Debugging:**
```
Navigate to https://example.com and show all failed network requests
```

## Skill Structure

```
chrome-devtools-mcp/
├── SKILL.md                          # Comprehensive guide (main skill content)
├── README.md                         # This file
├── resources/
│   ├── configuration-templates.md    # MCP config examples
│   └── test-patterns.md              # Reusable test patterns
└── scripts/
    ├── validate-setup.sh             # Setup verification
    └── generate-test-suite.py        # Test template generator
```

## Core Capabilities

### 26 Available Tools

**Input Automation (8):**
- `click`, `drag`, `fill`, `fill_form`
- `handle_dialog`, `hover`, `press_key`, `upload_file`

**Navigation (6):**
- `navigate_page`, `new_page`, `select_page`
- `list_pages`, `close_page`, `wait_for`

**Emulation (2):**
- `emulate` (devices), `resize_page` (viewports)

**Performance (3):**
- `performance_start_trace`, `performance_stop_trace`
- `performance_analyze_insight`

**Network (2):**
- `list_network_requests`, `get_network_request`

**Debugging (5):**
- `evaluate_script`, `take_screenshot`, `take_snapshot`
- `get_console_message`, `list_console_messages`

## Configuration Examples

### Local Development
```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "chrome-devtools-mcp@latest",
        "--channel=canary",
        "--isolated=true"
      ]
    }
  }
}
```

### CI/CD Pipeline
```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "chrome-devtools-mcp@latest",
        "--headless=true",
        "--isolated=true",
        "--chromeArg=--no-sandbox"
      ]
    }
  }
}
```

### Connect to Running Chrome
```bash
# Start Chrome with debugging port
chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome

# Configure MCP
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "chrome-devtools-mcp@latest",
        "--browserUrl=http://127.0.0.1:9222"
      ]
    }
  }
}
```

See `resources/configuration-templates.md` for more examples.

## Common Usage Patterns

### Performance Testing Workflow
```
1. Navigate to https://example.com
2. Start performance trace
3. Wait for network idle
4. Stop performance trace
5. Analyze performance insights
```

### Form Testing Workflow
```
1. Navigate to /registration
2. Fill the form with test data
3. Click Submit button
4. Wait for confirmation page
5. Take screenshot
6. Verify no console errors
```

### Visual Regression Workflow
```
1. Resize to 1920x1080 (desktop)
2. Navigate to page
3. Take screenshot (baseline)
4. Resize to 375x812 (mobile)
5. Take screenshot (mobile)
6. Compare screenshots
```

See `resources/test-patterns.md` for 20+ detailed patterns.

## Helper Scripts

### Setup Validation
```bash
./scripts/validate-setup.sh
```
Checks Node.js, Chrome, npm, and MCP configuration.

### Test Suite Generator
```bash
# Performance test
./scripts/generate-test-suite.py --url https://example.com --type performance

# E2E test
./scripts/generate-test-suite.py --url https://example.com --type e2e --flow login

# Visual regression test
./scripts/generate-test-suite.py --url https://example.com --type visual
```

Generates test templates and configuration files.

## Best Practices

### Security
- ✅ Use `--isolated` flag for clean testing environments
- ✅ Avoid real credentials in automated tests
- ✅ Clear sensitive data after test runs
- ❌ Never expose debugging port to network

### Performance Testing
- ✅ Run multiple iterations and average results
- ✅ Test on realistic network conditions
- ✅ Focus on user-centric metrics (FCP, LCP, CLS)
- ✅ Compare against baselines

### Browser Automation
- ✅ Wait for conditions explicitly with `wait_for`
- ✅ Take screenshots at key points for debugging
- ✅ Check console for errors after critical actions
- ✅ Handle timeouts gracefully

### CI/CD Integration
- ✅ Use headless mode to save resources
- ✅ Add `--no-sandbox` in containers
- ✅ Set appropriate timeouts
- ✅ Capture screenshots on failures

## Troubleshooting

### Chrome Won't Start
1. Check Chrome is installed: `which google-chrome` or `which chrome`
2. Specify path: `--executablePath=/path/to/chrome`
3. Try different channel: `--channel=canary`
4. Check logs: `--logFile=/tmp/chrome-mcp.log`

### Sandbox Issues (macOS/Linux)
- Use `--browserUrl` with externally launched Chrome
- Or add: `--chromeArg=--no-sandbox` (development only)

### Network Issues
- Ensure `--categoryNetwork=true` (default)
- Wait for network idle with `wait_for` tool
- Check console for CSP violations

### Performance Data Missing
- Ensure `--categoryPerformance=true` (default)
- Stop trace before analyzing
- Check trace duration (minimum ~100ms)

See SKILL.md for comprehensive troubleshooting guide.

## Integration with Existing Tools

Chrome DevTools MCP can replace or complement:

- **Playwright**: Similar API, but AI-driven with natural language
- **Cypress**: No test framework needed, use conversational commands
- **Lighthouse**: Performance analysis with actionable recommendations
- **Selenium**: More reliable waits and modern protocol

Advantages:
- No test boilerplate or framework setup
- Natural language interaction
- Automatic stability handling
- Built on battle-tested Puppeteer

## Resources

### In This Skill
- **SKILL.md** - Complete reference guide
- **configuration-templates.md** - 20+ configuration examples
- **test-patterns.md** - Reusable test patterns and workflows
- **validate-setup.sh** - Verify installation and configuration
- **generate-test-suite.py** - Create test templates

### External Resources
- **Official Repository**: https://github.com/ChromeDevTools/chrome-devtools-mcp
- **Chrome DevTools Protocol**: https://chromedevtools.github.io/devtools-protocol/
- **MCP Documentation**: https://modelcontextprotocol.io/
- **Puppeteer Docs**: https://pptr.dev/

## Examples

### Complete E2E Test
```
Test the complete checkout flow at https://example.com:
1. Add an item to cart
2. Proceed to checkout
3. Fill shipping information
4. Enter payment details
5. Complete order
6. Verify confirmation page
7. Take screenshots at each step
8. Check for console errors
```

### Performance Comparison
```
Compare performance of https://example.com homepage:
1. Test current version
2. Test optimized version at /optimized
3. Show differences in Core Web Vitals
4. Identify which version is faster and why
```

### Multi-Device Testing
```
Test https://example.com responsive design:
1. Test on iPhone 14 Pro
2. Test on iPad
3. Test on desktop (1920x1080)
4. Take screenshots of each
5. Verify layout adapts correctly
```

## Requirements

- **Node.js**: v20.19 or newer (LTS recommended)
- **Chrome**: Stable version or newer
- **npm**: Latest version
- **MCP Client**: Claude Code, Cursor, VS Code Copilot, or any MCP-compatible client

## Getting Help

1. **Check SKILL.md** - Comprehensive guide with all tools and patterns
2. **Run validation script** - `./scripts/validate-setup.sh`
3. **Review examples** - `resources/test-patterns.md`
4. **Check logs** - Use `--logFile` option for debugging
5. **GitHub Issues**: https://github.com/ChromeDevTools/chrome-devtools-mcp/issues

## License

This skill documentation is provided as-is for use with Chrome DevTools MCP.

Chrome DevTools MCP is licensed under Apache 2.0.

## Contributing

Found an issue or have a suggestion? This skill is part of your Claude Code configuration.

To improve:
1. Edit skill files in `~/.claude/skills/chrome-devtools-mcp/`
2. Test changes
3. Share improvements with team or community

---

**Quick Links:**
- [SKILL.md](SKILL.md) - Full skill documentation
- [Configuration Templates](resources/configuration-templates.md)
- [Test Patterns](resources/test-patterns.md)
- [Official MCP Server](https://github.com/ChromeDevTools/chrome-devtools-mcp)
