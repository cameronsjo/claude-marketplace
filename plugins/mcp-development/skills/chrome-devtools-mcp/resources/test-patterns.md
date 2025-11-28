# Chrome DevTools MCP Test Patterns

Reusable test patterns for common browser testing scenarios.

## Performance Testing Patterns

### Basic Performance Test
```
1. Navigate to https://example.com
2. Start performance trace
3. Wait for network idle
4. Stop performance trace
5. Analyze performance insights
```

**What to check:**
- First Contentful Paint (FCP) < 1.8s
- Largest Contentful Paint (LCP) < 2.5s
- Time to Interactive (TTI) < 3.8s
- Total Blocking Time (TBT) < 200ms
- Cumulative Layout Shift (CLS) < 0.1

### Performance with User Interaction
```
1. Navigate to page
2. Start performance trace
3. Click "Products" tab
4. Wait for 2 seconds
5. Scroll to bottom of page
6. Wait for network idle
7. Stop performance trace
8. Analyze performance insights
```

### Performance Comparison (Before/After)
```
# Baseline
1. Navigate to https://example.com
2. Start performance trace
3. Wait for network idle
4. Stop performance trace
5. Analyze insights (save metrics)

# After changes
6. Navigate to https://example.com?optimized=true
7. Start performance trace
8. Wait for network idle
9. Stop performance trace
10. Analyze insights (compare to baseline)
```

## Form Testing Patterns

### Simple Form Submission
```
1. Navigate to /contact-form
2. Fill the form with:
   - name: Test User
   - email: test@example.com
   - message: This is a test message
3. Click the "Submit" button
4. Wait for navigation to complete
5. Check if URL contains "success"
6. Take screenshot
```

### Form Validation Testing
```
1. Navigate to /registration
2. Fill email with "invalid-email"
3. Click "Submit"
4. List console messages
5. Verify error message appears
6. Take screenshot of error state
7. Fill email with "valid@example.com"
8. Fill password with "Test123!"
9. Click "Submit"
10. Verify success
```

### Multi-Step Form
```
1. Navigate to /checkout
2. Fill shipping form (step 1)
3. Click "Next"
4. Wait for step 2 to load
5. Fill payment form (step 2)
6. Click "Next"
7. Wait for step 3
8. Review and confirm
9. Click "Place Order"
10. Wait for confirmation
11. Take screenshot
```

## Navigation Patterns

### Multi-Page Flow
```
1. Navigate to /home
2. Click "Products"
3. Wait for navigation
4. Click first product
5. Wait for product page
6. Click "Add to Cart"
7. Wait for cart update
8. Navigate to /cart
9. Verify item in cart
10. Take screenshot
```

### Back/Forward Navigation
```
1. Navigate to /page1
2. Click link to /page2
3. Wait for load
4. Take screenshot of page2
5. Press key "Backspace" (go back)
6. Wait for page1 to load
7. Verify we're on page1
8. Take screenshot
```

### Tab Management
```
1. Create new page
2. Navigate to /login (in new page)
3. Fill login form
4. Click login
5. Select page 1 (original)
6. Navigate to /dashboard
7. List all pages
8. Close page 2 (login page)
```

## Network Testing Patterns

### API Request Monitoring
```
1. Navigate to /dashboard
2. Wait for network idle
3. List all network requests
4. Filter requests by /api/
5. Get details for /api/users request
6. Verify status code is 200
7. Verify response contains expected data
```

### Failed Request Debugging
```
1. Navigate to page
2. Wait for network idle
3. List all network requests with status 4xx or 5xx
4. For each failed request:
   - Get request details
   - Check request headers
   - Check response body
   - List console errors
5. Take screenshot
```

### Network Throttling Test
```
# Configure with --chromeArg=--force-slow-network
1. Navigate to page
2. Start performance trace
3. Wait for network idle (with timeout)
4. Stop performance trace
5. Analyze insights
6. Check if load time is acceptable on slow network
```

## Device Emulation Patterns

### Mobile Testing
```
1. Emulate iPhone 14 Pro
2. Navigate to /home
3. Verify mobile menu appears
4. Click hamburger menu
5. Verify menu opens
6. Take screenshot
7. Click menu item
8. Verify navigation works
```

### Responsive Design Testing
```
# Desktop
1. Resize page to 1920x1080
2. Navigate to page
3. Take screenshot (save as desktop.png)

# Tablet
4. Resize page to 768x1024
5. Take screenshot (save as tablet.png)

# Mobile
6. Resize page to 375x812
7. Take screenshot (save as mobile.png)

# Compare screenshots externally
```

### Orientation Testing
```
1. Emulate iPhone 14 Pro (portrait)
2. Navigate to page
3. Take screenshot
4. Emulate iPhone 14 Pro in landscape
5. Take screenshot
6. Compare layouts
```

## Debugging Patterns

### Console Error Investigation
```
1. Navigate to page
2. Trigger error (click broken feature)
3. List all console errors
4. Get first error message
5. Evaluate script: console.trace()
6. Take DOM snapshot
7. Take screenshot for evidence
```

### JavaScript Debugging
```
1. Navigate to page
2. Evaluate script: window.appState
3. Take note of current state
4. Perform action (click button)
5. Evaluate script: window.appState
6. Compare states
7. If issue found, evaluate debug script
```

### DOM Inspection
```
1. Navigate to page
2. Evaluate script: document.querySelectorAll('.product-card').length
3. Verify expected number of elements
4. Evaluate script: Array.from(document.querySelectorAll('.product-card')).map(el => el.textContent)
5. Verify content
6. Take DOM snapshot for detailed analysis
```

## Visual Regression Patterns

### Screenshot Comparison
```
# Baseline
1. Navigate to page
2. Wait for network idle
3. Resize to 1920x1080
4. Take screenshot (save as baseline.png)

# After changes
5. Navigate to page (new version)
6. Wait for network idle
7. Resize to 1920x1080
8. Take screenshot (save as current.png)

# Compare externally with image diff tools
```

### Component-Level Screenshots
```
1. Navigate to page
2. Evaluate script to scroll to component:
   document.querySelector('.hero-section').scrollIntoView()
3. Wait 1 second
4. Take screenshot
5. Repeat for other components
```

### Animation Testing
```
1. Navigate to page
2. Trigger animation (hover or click)
3. Wait 500ms (mid-animation)
4. Take screenshot
5. Wait 1000ms (animation complete)
6. Take screenshot
7. Compare frames
```

## Authentication Patterns

### Login Flow
```
1. Navigate to /login
2. Fill username with "testuser"
3. Fill password with "TestPass123!"
4. Click "Login"
5. Wait for navigation to /dashboard
6. Verify URL is /dashboard
7. Evaluate script: localStorage.getItem('authToken')
8. Verify token exists
9. Take screenshot
```

### Session Persistence (Using Persistent Profile)
```
# First run - login
1. Navigate to /login
2. Fill and submit credentials
3. Wait for dashboard

# Second run - check persistence
4. Navigate to /dashboard
5. Verify still logged in (no redirect to login)
6. Evaluate script: document.cookie
7. Verify auth cookies present
```

### Logout Flow
```
1. Navigate to /dashboard (while logged in)
2. Click "Logout"
3. Wait for navigation
4. Verify redirected to /login
5. Evaluate script: localStorage.getItem('authToken')
6. Verify token is null
7. Attempt to navigate to /dashboard
8. Verify redirected back to /login
```

## E2E Test Patterns

### Complete User Journey
```
1. Navigate to /home
2. Click "Sign Up"
3. Fill registration form
4. Click "Create Account"
5. Wait for confirmation
6. Navigate to /products
7. Click first product
8. Click "Add to Cart"
9. Navigate to /cart
10. Click "Checkout"
11. Fill shipping info
12. Fill payment info
13. Click "Place Order"
14. Wait for confirmation
15. Take screenshot of confirmation page
16. Verify order confirmation email (check console logs)
```

### Error Recovery Flow
```
1. Navigate to /checkout
2. Fill form with invalid credit card
3. Click "Submit"
4. Verify error message appears
5. List console errors
6. Fill with valid credit card
7. Click "Submit"
8. Verify success
9. Take screenshot
```

## Accessibility Testing Patterns

### Keyboard Navigation
```
1. Navigate to /form
2. Press key "Tab" (focus first input)
3. Fill current field
4. Press key "Tab" (move to next)
5. Fill current field
6. Press key "Enter" (submit)
7. Verify form submitted
```

### Screen Reader Testing
```
1. Navigate to page
2. Evaluate script:
   Array.from(document.querySelectorAll('*'))
     .filter(el => !el.getAttribute('aria-label') && !el.getAttribute('alt'))
     .filter(el => el.tagName === 'IMG' || el.tagName === 'BUTTON')
3. List elements missing accessibility attributes
4. Take screenshot
```

### Color Contrast Check
```
1. Navigate to page
2. Evaluate script to check contrast ratios:
   // Load contrast checking library first
3. List console warnings for contrast violations
4. Take screenshots of problem areas
```

## Data-Driven Testing Patterns

### Parameterized Form Tests
```
# Test data: multiple user scenarios
For each user in [admin, regular_user, guest]:
  1. Navigate to /login
  2. Fill username with user.username
  3. Fill password with user.password
  4. Click "Login"
  5. Verify correct dashboard loads for user role
  6. Take screenshot named "{user.role}-dashboard.png"
  7. Click "Logout"
```

### Cross-Browser Data Validation
```
# Test same data across different viewport sizes
For each viewport in [desktop, tablet, mobile]:
  1. Resize to viewport dimensions
  2. Navigate to /data-table
  3. Evaluate script: document.querySelectorAll('table tr').length
  4. Verify row count matches expected
  5. Take screenshot
```

## Integration Testing Patterns

### API + UI Integration
```
1. Navigate to page
2. List network requests
3. Verify API called correctly
4. Get API response details
5. Evaluate script to check UI state matches API data:
   JSON.parse(apiResponse.body).items.length ===
   document.querySelectorAll('.item').length
6. Take screenshot
```

### Third-Party Service Integration
```
1. Navigate to page with external service (e.g., maps)
2. Wait for 3 seconds (service load time)
3. Evaluate script: typeof google !== 'undefined'
4. Verify service loaded
5. List console errors (check for API key issues)
6. Take screenshot of working service
```

## Tips for Pattern Usage

1. **Combine patterns** - Mix and match for complex scenarios
2. **Add assertions** - Use evaluate_script to verify conditions
3. **Take screenshots** - Capture evidence at key points
4. **Check console** - Always verify no unexpected errors
5. **Wait appropriately** - Use wait_for to ensure stability
6. **Clean up** - Close pages and clear state between tests
7. **Document expectations** - Note what should/shouldn't happen
8. **Handle failures** - Plan for error scenarios and recovery

## Pattern Categories Quick Reference

| Category | Use When | Key Tools |
|----------|----------|-----------|
| Performance | Measuring speed/efficiency | performance_*, wait_for |
| Form Testing | Validating input handling | fill_form, click, wait_for |
| Navigation | Testing page flows | navigate_page, click, wait_for |
| Network | Debugging API calls | list_network_requests, get_network_request |
| Device Emulation | Testing responsive design | emulate, resize_page |
| Debugging | Investigating issues | evaluate_script, list_console_messages |
| Visual Regression | Detecting UI changes | take_screenshot, resize_page |
| Authentication | Testing login/logout | fill_form, evaluate_script |
| E2E | Full user journeys | All tools combined |
| Accessibility | A11y compliance | evaluate_script, press_key |
