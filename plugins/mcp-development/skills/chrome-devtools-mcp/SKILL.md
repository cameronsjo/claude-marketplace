# Chrome DevTools MCP Skill

Expert guidance for using Chrome DevTools MCP server to automate browser testing, performance analysis, and debugging through AI-powered interactions.

## Overview

Chrome DevTools MCP is a Model Context Protocol server that enables AI coding agents to control and inspect live Chrome browser instances. It provides 26 tools across performance analysis, browser automation, network inspection, and debugging capabilities.

**Key Capabilities:**
- Browser automation with reliable Puppeteer-based actions
- Performance tracing and analysis using Chrome DevTools
- Network request inspection and debugging
- Console monitoring and JavaScript execution
- Screenshot capture and DOM snapshots
- Device emulation and responsive testing

## When to Use This Skill

Use Chrome DevTools MCP for:
- **Performance Analysis**: Measure page load times, rendering efficiency, resource usage
- **Automated Testing**: E2E testing, form validation, user flow testing
- **Debugging**: Network issues, console errors, JavaScript problems
- **Visual Regression**: Screenshot comparisons, responsive design testing
- **Device Emulation**: Mobile testing, different viewport sizes
- **Accessibility Testing**: Check console for a11y warnings
- **Security Testing**: Inspect network traffic, check CSP headers

## Installation & Setup

### Basic Installation

**Claude Code:**
```bash
claude mcp add chrome-devtools npx chrome-devtools-mcp@latest
```

**Manual Configuration (any MCP client):**
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

### Advanced Configuration

**Headless Mode with Isolated Profile:**
```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "chrome-devtools-mcp@latest",
        "--headless=true",
        "--isolated=true",
        "--channel=stable"
      ]
    }
  }
}
```

**Connect to Running Chrome Instance:**
```json
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

**With Proxy and Custom Viewport:**
```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "chrome-devtools-mcp@latest",
        "--viewport=1920x1080",
        "--proxyServer=http://proxy.example.com:8080"
      ]
    }
  }
}
```

### Configuration Options Reference

| Option | Type | Default | Purpose |
|--------|------|---------|---------|
| `--browserUrl`, `-u` | string | — | Connect to running Chrome via port |
| `--wsEndpoint`, `-w` | string | — | WebSocket endpoint for Chrome |
| `--wsHeaders` | string | — | Custom WS headers (JSON format) |
| `--headless` | boolean | false | Run without UI |
| `--executablePath`, `-e` | string | — | Custom Chrome path |
| `--isolated` | boolean | false | Temporary profile (auto-cleanup) |
| `--channel` | string | stable | Chrome channel (stable/canary/beta/dev) |
| `--logFile` | string | — | Debug log path |
| `--viewport` | string | — | Initial size (e.g., `1280x720`) |
| `--proxyServer` | string | — | Proxy configuration |
| `--acceptInsecureCerts` | boolean | false | Ignore certificate errors |
| `--chromeArg` | array | — | Additional Chrome arguments |
| `--categoryEmulation` | boolean | true | Enable emulation tools |
| `--categoryPerformance` | boolean | true | Enable performance tools |
| `--categoryNetwork` | boolean | true | Enable network tools |

## Available Tools (26)

### Input Automation (8 tools)

**`click`** - Perform mouse clicks
- Click buttons, links, or any clickable elements
- Automatically waits for element to be clickable
- Example: "Click the 'Sign In' button"

**`drag`** - Drag and drop operations
- Drag elements from one location to another
- Useful for sortable lists, drag-to-upload
- Example: "Drag the file to the upload zone"

**`fill`** - Text input
- Fill single input fields
- Example: "Fill the email field with test@example.com"

**`fill_form`** - Multi-field form completion
- Fill multiple form fields at once
- More efficient than individual `fill` calls
- Example: "Fill the registration form with test data"

**`handle_dialog`** - Dialog management
- Accept or dismiss alerts, confirms, prompts
- Example: "Accept the confirmation dialog"

**`hover`** - Mouse hovering
- Trigger hover states and tooltips
- Example: "Hover over the help icon"

**`press_key`** - Keyboard input
- Send keyboard events (Enter, Escape, Tab, etc.)
- Example: "Press Enter to submit"

**`upload_file`** - File uploads
- Upload files through file input elements
- Example: "Upload test-data.csv to the import form"

### Navigation Automation (6 tools)

**`navigate_page`** - URL navigation
- Navigate to any URL
- Example: "Navigate to https://example.com"

**`new_page`** - Create new tabs/pages
- Open new browser pages
- Example: "Open a new page"

**`select_page`** - Switch between pages
- Switch to different open pages/tabs
- Example: "Switch to page 2"

**`list_pages`** - Enumerate open pages
- List all currently open pages
- Example: "List all open pages"

**`close_page`** - Close browser pages
- Close specific pages
- Example: "Close the current page"

**`wait_for`** - Wait for conditions
- Wait for navigation, network idle, selectors
- Example: "Wait for the page to finish loading"

### Emulation (2 tools)

**`emulate`** - Device/environment emulation
- Emulate mobile devices, tablets
- Set user agents, screen sizes, device metrics
- Example: "Emulate iPhone 14 Pro"

**`resize_page`** - Viewport modification
- Change viewport dimensions
- Example: "Resize page to 1024x768"

### Performance (3 tools)

**`performance_start_trace`** - Begin performance recording
- Start recording Chrome DevTools performance trace
- Example: "Start performance trace"

**`performance_stop_trace`** - End performance recording
- Stop trace and save data
- Example: "Stop performance trace"

**`performance_analyze_insight`** - Extract performance metrics
- Analyze traces for actionable insights
- Metrics: load times, rendering, resource usage
- Example: "Analyze performance insights from the trace"

### Network (2 tools)

**`list_network_requests`** - View network requests
- List all network requests made by page
- Filter by type, status, URL patterns
- Example: "List all failed network requests"

**`get_network_request`** - Request details
- Get detailed information about specific request
- Headers, body, timing, response
- Example: "Get details for the API request to /users"

### Debugging (5 tools)

**`evaluate_script`** - Execute JavaScript
- Run JavaScript in page context
- Access DOM, window, document
- Example: "Execute: document.querySelectorAll('img').length"

**`get_console_message`** - Retrieve console message
- Get specific console message
- Example: "Get the first error message"

**`list_console_messages`** - View all console messages
- List all console logs, warns, errors
- Example: "List all console errors"

**`take_screenshot`** - Capture current state
- Take full page or viewport screenshots
- Example: "Take a screenshot of the page"

**`take_snapshot`** - DOM snapshot
- Capture current DOM state
- Example: "Take a DOM snapshot"

## Common Usage Patterns

### Performance Testing Workflow

```
1. Navigate to the page: "Navigate to https://example.com"
2. Start tracing: "Start performance trace"
3. Perform user actions: "Click the 'Products' tab"
4. Stop tracing: "Stop performance trace"
5. Analyze: "Analyze performance insights"
```

**What to look for:**
- First Contentful Paint (FCP) < 1.8s (good)
- Largest Contentful Paint (LCP) < 2.5s (good)
- Time to Interactive (TTI) < 3.8s (good)
- Total Blocking Time (TBT) < 200ms (good)
- Cumulative Layout Shift (CLS) < 0.1 (good)

### Automated Form Testing

```
1. Navigate to form page
2. Fill form: "Fill the registration form with:
   - email: test@example.com
   - password: TestPass123!
   - confirm: TestPass123!"
3. Submit: "Click the 'Register' button"
4. Verify: "Wait for navigation to complete"
5. Check result: "Take a screenshot"
```

### Network Debugging

```
1. Clear cache and navigate
2. Wait for load: "Wait for network idle"
3. List requests: "List all network requests"
4. Filter failures: "List all requests with status 4xx or 5xx"
5. Inspect specific: "Get details for the failed API request"
6. Check console: "List all console errors"
```

### Visual Regression Testing

```
1. Set baseline viewport: "Resize page to 1920x1080"
2. Navigate: "Navigate to homepage"
3. Baseline screenshot: "Take screenshot of full page"
4. Test responsive: "Resize page to 375x812" (mobile)
5. Mobile screenshot: "Take screenshot"
6. Compare screenshots externally
```

### Device Emulation Testing

```
1. Emulate device: "Emulate iPhone 14 Pro"
2. Navigate to page
3. Test mobile interactions: "Click the hamburger menu"
4. Check touch targets: "Take screenshot"
5. Verify responsive layout
6. Test orientation: "Emulate iPhone 14 Pro in landscape"
```

### Console Error Debugging

```
1. Navigate to page
2. Trigger error condition: "Click the 'Submit' button"
3. Check console: "List all console errors"
4. Get error details: "Get the first error message"
5. Execute debug script: "Evaluate: console.trace()"
6. Take evidence: "Take screenshot"
```

## Best Practices

### Performance Analysis
- **Clear cache** between runs for consistent metrics
- **Run multiple iterations** (3-5) and average results
- **Test on realistic network** conditions (throttling)
- **Compare against baselines** from previous tests
- **Focus on user-centric metrics** (FCP, LCP, CLS)

### Browser Automation
- **Wait for conditions** explicitly (don't assume instant load)
- **Use `wait_for`** after navigation or actions
- **Handle timeouts** gracefully in test scripts
- **Take screenshots** at key points for debugging
- **Check console errors** after critical actions

### Network Testing
- **Monitor API calls** during user flows
- **Check status codes** and response times
- **Verify request headers** (auth, content-type)
- **Inspect response payloads** for data quality
- **Test error handling** (simulate failures)

### Security & Privacy
- **Use `--isolated` flag** for sensitive testing
- **Avoid real credentials** in automated tests
- **Clear cache/cookies** between test runs
- **Don't expose debugging port** to network
- **Review screenshots** before sharing (may contain PII)

### Debugging Tips
- **Start with `--logFile`** to capture debug output
- **Use console messages** to trace execution
- **Evaluate scripts** to inspect page state
- **Take DOM snapshots** for complex debugging
- **Check network tab** for API issues

## Configuration Patterns

### Local Development Setup
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
- Uses Chrome Canary for latest features
- Isolated profile for clean testing environment

### CI/CD Pipeline Setup
```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "chrome-devtools-mcp@latest",
        "--headless=true",
        "--isolated=true",
        "--acceptInsecureCerts=true",
        "--chromeArg=--disable-dev-shm-usage",
        "--chromeArg=--no-sandbox"
      ]
    }
  }
}
```
- Headless for CI environments
- Additional Chrome args for container compatibility

### Persistent Profile Setup
```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "chrome-devtools-mcp@latest",
        "--channel=stable"
      ]
    }
  }
}
```
- Uses default profile at `~/.cache/chrome-devtools-mcp/chrome-profile-stable`
- Maintains cookies, local storage between runs

### Remote Chrome Connection
```bash
# Start Chrome with debugging port
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir=/tmp/chrome-profile
```

```json
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

## Troubleshooting

### Chrome Won't Start

**Problem**: "Failed to launch Chrome"

**Solutions:**
1. Check Chrome is installed: `which google-chrome` or `which chrome`
2. Specify path: `--executablePath=/path/to/chrome`
3. Try different channel: `--channel=canary`
4. Check logs: `--logFile=/tmp/chrome-mcp.log`

### Sandbox Issues (macOS/Linux)

**Problem**: "Running as root without --no-sandbox is not supported"

**Solutions:**
1. Use `--browserUrl` with externally launched Chrome
2. Disable MCP client sandboxing (if applicable)
3. Add Chrome arg: `--chromeArg=--no-sandbox` (development only)

### Connection Timeouts

**Problem**: "Timeout waiting for browser"

**Solutions:**
1. Increase timeout: Check MCP client settings
2. Check system resources (RAM, CPU)
3. Try headless mode: `--headless=true`
4. Kill existing Chrome processes

### Network Issues

**Problem**: "Network requests not captured"

**Solutions:**
1. Ensure `--categoryNetwork=true` (default)
2. Wait for network idle: Use `wait_for` tool
3. Check if page uses WebSockets or other protocols
4. Review console for CSP violations

### Performance Data Missing

**Problem**: "No performance trace data"

**Solutions:**
1. Ensure `--categoryPerformance=true` (default)
2. Stop trace before analyzing: `performance_stop_trace`
3. Check trace duration (minimum ~100ms)
4. Verify page loaded completely

## Security Considerations

### Data Privacy
- **Browser content exposed** to MCP clients (inspection, modification)
- **Avoid sensitive data** while server is running
- **Use `--isolated` flag** for temporary profiles
- **Clear profiles** regularly if using persistent mode

### Remote Debugging
- **Port 9222 accessible** to any local application
- **No authentication** on debugging port by default
- **Only use locally** - never expose to network
- **Non-default user-data-dir** required for security

### Credentials & Secrets
- **Never hardcode credentials** in test scripts
- **Use environment variables** for API keys
- **Clear storage** after tests with sensitive data
- **Review screenshots** before sharing (may contain tokens)

## Integration Examples

### Playwright Alternative
Chrome DevTools MCP can replace Playwright for many use cases:

**Playwright:**
```javascript
await page.goto('https://example.com');
await page.click('button#submit');
await page.waitForNavigation();
```

**Chrome DevTools MCP:**
```
1. Navigate to https://example.com
2. Click the submit button
3. Wait for navigation to complete
```

### Cypress Alternative
Similar functionality with AI-driven interactions:

**Cypress:**
```javascript
cy.visit('https://example.com')
cy.get('input[name="email"]').type('test@example.com')
cy.get('button').contains('Submit').click()
```

**Chrome DevTools MCP:**
```
1. Navigate to https://example.com
2. Fill the email input with test@example.com
3. Click the Submit button
```

### Lighthouse Alternative
Performance analysis similar to Lighthouse:

```
1. Navigate to page
2. Start performance trace
3. Wait for page load
4. Stop performance trace
5. Analyze performance insights
```

Provides Core Web Vitals and actionable recommendations.

## Advanced Use Cases

### Multi-Page Testing
```
1. Create new page for login
2. Navigate to /login
3. Fill login form
4. Click login button
5. Create new page for dashboard
6. Verify dashboard loaded
7. List all pages to see session
```

### API Response Validation
```
1. Navigate to page
2. Wait for network idle
3. List network requests filtered by /api/
4. Get request details for /api/users
5. Evaluate script to verify: JSON.parse(response.body).length > 0
```

### Progressive Enhancement Testing
```
1. Navigate with JavaScript disabled: --chromeArg=--blink-settings=scriptEnabled=false
2. Verify content renders
3. Take screenshot
4. Re-enable JavaScript and compare
```

### Accessibility Auditing
```
1. Navigate to page
2. Evaluate script: axe.run() (requires axe-core loaded)
3. List console warnings for a11y violations
4. Take screenshot of problematic areas
```

## Tool Combinations

### Complete E2E Test Flow
```
navigate_page → fill_form → click → wait_for →
list_console_messages → take_screenshot →
list_network_requests → evaluate_script
```

### Performance Optimization Workflow
```
navigate_page → performance_start_trace →
[user actions] → performance_stop_trace →
performance_analyze_insight → take_screenshot
```

### Debugging Workflow
```
navigate_page → evaluate_script (inspect state) →
list_console_messages → get_console_message →
list_network_requests → get_network_request →
take_snapshot
```

## Resources

- **Official Docs**: https://github.com/ChromeDevTools/chrome-devtools-mcp
- **Tool Reference**: Check repo for detailed tool documentation
- **Troubleshooting Guide**: See repo docs/troubleshooting.md
- **Chrome DevTools Protocol**: https://chromedevtools.github.io/devtools-protocol/

## Quick Reference

### Essential Test Prompt
```
"Check the performance of https://developers.chrome.com"
```
Validates setup by opening browser and recording performance trace.

### Common Tool Sequences

**Performance Test:**
```
navigate_page → performance_start_trace → wait_for →
performance_stop_trace → performance_analyze_insight
```

**Form Test:**
```
navigate_page → fill_form → click → wait_for →
list_console_messages → take_screenshot
```

**Network Debug:**
```
navigate_page → wait_for → list_network_requests →
get_network_request → list_console_messages
```

**Visual Test:**
```
navigate_page → emulate → wait_for → take_screenshot →
resize_page → take_screenshot
```

## Limitations

- **OS sandboxing** conflicts with Chrome's sandbox (use `--browserUrl` workaround)
- **WebSocket-based protocols** may not be fully captured in network logs
- **Cross-origin iframes** have limited inspection due to browser security
- **Chrome extensions** not supported in isolated mode
- **Binary file downloads** require additional handling
- **File system access** limited by browser security policies

## Next Steps

1. **Install the server**: Use Claude Code or manual configuration
2. **Test basic functionality**: "Check the performance of https://example.com"
3. **Explore tools**: Try each category (input, navigation, performance, etc.)
4. **Build test suites**: Create reusable test patterns
5. **Integrate with CI/CD**: Add to automated pipelines
6. **Monitor performance**: Track metrics over time

Always prioritize security, use isolated profiles for testing, and clear sensitive data after test runs.
