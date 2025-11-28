#!/usr/bin/env python3
"""
Generate browser test suites for Chrome DevTools MCP

Usage:
  python generate-test-suite.py --url https://example.com --type performance
  python generate-test-suite.py --url https://example.com --type e2e --flow login
"""

import argparse
import json
from pathlib import Path


PERFORMANCE_TEMPLATE = """# Performance Test: {url}

## Test Configuration
- URL: {url}
- Date: {{current_date}}
- Browser: Chrome (via DevTools MCP)

## Test Steps
1. Navigate to {url}
2. Start performance trace
3. Wait for network idle
4. Stop performance trace
5. Analyze performance insights

## Expected Results
- First Contentful Paint (FCP) < 1.8s
- Largest Contentful Paint (LCP) < 2.5s
- Time to Interactive (TTI) < 3.8s
- Total Blocking Time (TBT) < 200ms
- Cumulative Layout Shift (CLS) < 0.1

## Actual Results
_Fill in after test run_

## Screenshots
_Attach screenshots here_

## Notes
_Add any observations or issues_
"""

E2E_LOGIN_TEMPLATE = """# E2E Test: Login Flow - {url}

## Test Configuration
- URL: {url}
- Date: {{current_date}}
- Flow: Authentication

## Test Steps
1. Navigate to {url}/login
2. Fill username field with "testuser"
3. Fill password field with "TestPass123!"
4. Click "Login" button
5. Wait for navigation to complete
6. Verify URL contains "/dashboard" or "/home"
7. Take screenshot of logged-in state
8. Verify no console errors

## Expected Results
- Login successful
- Redirected to dashboard/home
- No JavaScript errors
- Auth token in localStorage or cookies

## Actual Results
_Fill in after test run_

## Screenshots
- Before login: _attach_
- After login: _attach_

## Notes
_Add any observations or issues_
"""

E2E_CHECKOUT_TEMPLATE = """# E2E Test: Checkout Flow - {url}

## Test Configuration
- URL: {url}
- Date: {{current_date}}
- Flow: Complete Purchase

## Test Steps
1. Navigate to {url}
2. Add item to cart
3. Navigate to /cart
4. Verify item in cart
5. Click "Checkout"
6. Fill shipping information
7. Click "Continue"
8. Fill payment information
9. Click "Place Order"
10. Wait for confirmation
11. Take screenshot of confirmation
12. Verify order confirmation message

## Expected Results
- Item added to cart successfully
- Checkout process completes
- Order confirmation displayed
- No console errors

## Actual Results
_Fill in after test run_

## Screenshots
- Cart page: _attach_
- Checkout form: _attach_
- Confirmation: _attach_

## Notes
_Add any observations or issues_
"""

VISUAL_REGRESSION_TEMPLATE = """# Visual Regression Test: {url}

## Test Configuration
- URL: {url}
- Date: {{current_date}}
- Viewports: Desktop, Tablet, Mobile

## Test Steps

### Desktop (1920x1080)
1. Resize page to 1920x1080
2. Navigate to {url}
3. Wait for load
4. Take screenshot (save as desktop-{timestamp}.png)

### Tablet (768x1024)
5. Resize page to 768x1024
6. Take screenshot (save as tablet-{timestamp}.png)

### Mobile (375x812)
7. Resize page to 375x812
8. Take screenshot (save as mobile-{timestamp}.png)

## Expected Results
- All viewports render correctly
- No layout shifts or overflow
- Responsive design working as expected
- Images and content properly sized

## Comparison
Compare screenshots with baseline:
- desktop-baseline.png vs desktop-{timestamp}.png
- tablet-baseline.png vs tablet-{timestamp}.png
- mobile-baseline.png vs mobile-{timestamp}.png

## Actual Results
_Fill in after test run_

## Differences Found
_Document any visual changes_

## Screenshots
_Attach current and baseline screenshots_
"""


def generate_performance_test(url: str) -> str:
    """Generate performance test template"""
    return PERFORMANCE_TEMPLATE.format(url=url)


def generate_e2e_test(url: str, flow: str) -> str:
    """Generate E2E test template"""
    if flow == "login":
        return E2E_LOGIN_TEMPLATE.format(url=url)
    elif flow == "checkout":
        return E2E_CHECKOUT_TEMPLATE.format(url=url)
    else:
        return f"# E2E Test: {flow.title()} - {url}\n\n_Custom test steps needed_"


def generate_visual_test(url: str) -> str:
    """Generate visual regression test template"""
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    return VISUAL_REGRESSION_TEMPLATE.format(url=url, timestamp=timestamp)


def generate_config(url: str, test_type: str) -> dict:
    """Generate MCP configuration snippet"""
    return {
        "test_info": {
            "url": url,
            "type": test_type,
            "mcp_server": "chrome-devtools"
        },
        "recommended_config": {
            "mcpServers": {
                "chrome-devtools": {
                    "command": "npx",
                    "args": [
                        "chrome-devtools-mcp@latest",
                        "--headless=true",
                        "--isolated=true"
                    ]
                }
            }
        }
    }


def main():
    parser = argparse.ArgumentParser(
        description="Generate browser test suites for Chrome DevTools MCP"
    )
    parser.add_argument("--url", required=True, help="URL to test")
    parser.add_argument(
        "--type",
        required=True,
        choices=["performance", "e2e", "visual"],
        help="Type of test to generate"
    )
    parser.add_argument(
        "--flow",
        default="login",
        help="E2E flow type (login, checkout, custom)"
    )
    parser.add_argument(
        "--output",
        default=".",
        help="Output directory"
    )

    args = parser.parse_args()

    # Generate test content
    if args.type == "performance":
        content = generate_performance_test(args.url)
        filename = "performance-test.md"
    elif args.type == "e2e":
        content = generate_e2e_test(args.url, args.flow)
        filename = f"e2e-{args.flow}-test.md"
    elif args.type == "visual":
        content = generate_visual_test(args.url)
        filename = "visual-regression-test.md"

    # Generate config
    config = generate_config(args.url, args.type)

    # Write files
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    test_file = output_dir / filename
    config_file = output_dir / "test-config.json"

    with open(test_file, "w") as f:
        f.write(content)

    with open(config_file, "w") as f:
        json.dump(config, f, indent=2)

    print(f"✅ Generated test suite:")
    print(f"   Test file: {test_file}")
    print(f"   Config: {config_file}")
    print()
    print("Next steps:")
    print("1. Review and customize the test file")
    print("2. Configure MCP server with settings from test-config.json")
    print('3. Run test with Claude Code: Ask to "Run the test in {filename}"')


if __name__ == "__main__":
    main()
