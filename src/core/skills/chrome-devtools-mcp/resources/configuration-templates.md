# Chrome DevTools MCP Configuration Templates

Quick-start configurations for common scenarios.

## Basic Configurations

### Minimal Setup
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

### Headless Mode
```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "chrome-devtools-mcp@latest",
        "--headless=true"
      ]
    }
  }
}
```

### Isolated Profile (Clean State)
```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "chrome-devtools-mcp@latest",
        "--isolated=true"
      ]
    }
  }
}
```

## Development Configurations

### Local Development (Chrome Canary)
```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "chrome-devtools-mcp@latest",
        "--channel=canary",
        "--isolated=true",
        "--logFile=/tmp/chrome-mcp-debug.log"
      ]
    }
  }
}
```

### With Custom Viewport
```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "chrome-devtools-mcp@latest",
        "--viewport=1920x1080",
        "--isolated=true"
      ]
    }
  }
}
```

### Mobile Testing Setup
```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "chrome-devtools-mcp@latest",
        "--viewport=375x812",
        "--isolated=true"
      ]
    }
  }
}
```

## CI/CD Configurations

### GitHub Actions / GitLab CI
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
        "--chromeArg=--no-sandbox",
        "--chromeArg=--disable-gpu"
      ]
    }
  }
}
```

### Docker Container
```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "chrome-devtools-mcp@latest",
        "--headless=true",
        "--isolated=true",
        "--chromeArg=--no-sandbox",
        "--chromeArg=--disable-setuid-sandbox",
        "--chromeArg=--disable-dev-shm-usage",
        "--chromeArg=--disable-gpu"
      ]
    }
  }
}
```

### Jenkins
```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "chrome-devtools-mcp@latest",
        "--headless=true",
        "--isolated=true",
        "--chromeArg=--no-sandbox",
        "--chromeArg=--disable-dev-shm-usage"
      ],
      "env": {
        "DISPLAY": ":99"
      }
    }
  }
}
```

## Advanced Configurations

### Remote Chrome Connection
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

**Start Chrome manually:**
```bash
# macOS
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir=/tmp/chrome-profile-stable

# Linux
/usr/bin/google-chrome \
  --remote-debugging-port=9222 \
  --user-data-dir=/tmp/chrome-profile-stable

# Windows
"C:\Program Files\Google\Chrome\Application\chrome.exe" \
  --remote-debugging-port=9222 \
  --user-data-dir="%TEMP%\chrome-profile-stable"
```

### WebSocket with Authentication
```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "chrome-devtools-mcp@latest",
        "--wsEndpoint=ws://127.0.0.1:9222/devtools/browser/<id>",
        "--wsHeaders={\"Authorization\":\"Bearer YOUR_TOKEN\"}"
      ]
    }
  }
}
```

### Corporate Proxy
```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "chrome-devtools-mcp@latest",
        "--proxyServer=http://proxy.corp.com:8080",
        "--acceptInsecureCerts=true"
      ]
    }
  }
}
```

### Custom Chrome Installation
```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "chrome-devtools-mcp@latest",
        "--executablePath=/opt/google/chrome/chrome",
        "--isolated=true"
      ]
    }
  }
}
```

## Platform-Specific Configurations

### macOS
```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "chrome-devtools-mcp@latest",
        "--channel=stable",
        "--isolated=true"
      ]
    }
  }
}
```

### Windows (PowerShell)
```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "cmd",
      "args": [
        "/c",
        "npx",
        "-y",
        "chrome-devtools-mcp@latest",
        "--channel=stable"
      ]
    }
  }
}
```

### Windows 11 (Codex)
```toml
[mcp_servers.chrome-devtools]
command = "cmd"
args = ["/c", "npx", "-y", "chrome-devtools-mcp@latest"]
env = { SystemRoot="C:\\Windows", PROGRAMFILES="C:\\Program Files" }
startup_timeout_ms = 20_000
```

### Linux (Ubuntu/Debian)
```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "chrome-devtools-mcp@latest",
        "--executablePath=/usr/bin/google-chrome",
        "--isolated=true"
      ]
    }
  }
}
```

## Testing Scenarios

### Performance Testing
```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "chrome-devtools-mcp@latest",
        "--headless=true",
        "--isolated=true",
        "--categoryPerformance=true",
        "--categoryNetwork=true",
        "--categoryEmulation=false"
      ]
    }
  }
}
```

### Visual Regression Testing
```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "chrome-devtools-mcp@latest",
        "--viewport=1920x1080",
        "--isolated=true",
        "--categoryPerformance=false",
        "--categoryNetwork=false",
        "--categoryEmulation=true"
      ]
    }
  }
}
```

### Network Debugging
```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "chrome-devtools-mcp@latest",
        "--isolated=true",
        "--categoryNetwork=true",
        "--categoryPerformance=false",
        "--categoryEmulation=false"
      ]
    }
  }
}
```

### Accessibility Testing
```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "chrome-devtools-mcp@latest",
        "--isolated=true",
        "--chromeArg=--force-prefers-reduced-motion"
      ]
    }
  }
}
```

## Security Configurations

### Maximum Isolation
```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "chrome-devtools-mcp@latest",
        "--isolated=true",
        "--headless=true",
        "--chromeArg=--disable-extensions",
        "--chromeArg=--disable-plugins",
        "--chromeArg=--disable-images"
      ]
    }
  }
}
```

### Testing with User Credentials (Use Carefully)
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
**Note**: Uses persistent profile at `~/.cache/chrome-devtools-mcp/chrome-profile-stable` which maintains cookies/storage.

## Environment Variables

You can also use environment variables for sensitive configuration:

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "chrome-devtools-mcp@latest",
        "--proxyServer=$PROXY_URL"
      ],
      "env": {
        "PROXY_URL": "http://proxy.example.com:8080",
        "CHROME_PATH": "/opt/chrome/chrome"
      }
    }
  }
}
```

## Configuration Selection Guide

| Use Case | Configuration | Key Options |
|----------|---------------|-------------|
| Local Development | Canary + Isolated | `--channel=canary --isolated` |
| CI/CD Pipeline | Headless + Isolated | `--headless --isolated --no-sandbox` |
| Performance Testing | Headless + Performance | `--headless --categoryPerformance` |
| Visual Testing | Viewport + Emulation | `--viewport=... --categoryEmulation` |
| Network Debugging | Network Category | `--categoryNetwork=true` |
| Remote Chrome | Browser URL | `--browserUrl=http://...` |
| Corporate Network | Proxy + Certs | `--proxyServer=... --acceptInsecureCerts` |
| Maximum Security | Isolated + Disabled Features | `--isolated --disable-extensions` |

## Quick Start Commands

**Claude Code:**
```bash
# Basic
claude mcp add chrome-devtools npx chrome-devtools-mcp@latest

# Headless + Isolated
claude mcp add chrome-devtools npx chrome-devtools-mcp@latest -- --headless=true --isolated=true

# Custom viewport
claude mcp add chrome-devtools npx chrome-devtools-mcp@latest -- --viewport=1920x1080
```

**Help:**
```bash
npx chrome-devtools-mcp@latest --help
```

## Tips

1. **Start simple** - Use minimal config first, add options as needed
2. **Use `--isolated`** for testing to avoid profile pollution
3. **Enable `--logFile`** when debugging connection issues
4. **Set `--viewport`** explicitly for consistent screenshot sizes
5. **Use `--headless`** in CI/CD to save resources
6. **Keep profiles separate** with `--channel` for different Chrome versions
7. **Test locally first** before adding to CI/CD pipelines
8. **Check system requirements** - Node.js v20.19+, Chrome installed
