# Chart Selection Guide for Executive Presentations

Choose the right chart type to tell your story effectively. Wrong chart type = confused executives.

## Quick Selection Matrix

| Your Data | Best Chart Type | Use When | Avoid When |
|-----------|----------------|----------|------------|
| **Trend over time** | Line chart | Showing changes, growth, patterns | Comparing categories |
| **Comparing categories** | Bar chart | Comparing values across groups | Showing trends over time |
| **Part of whole** | Pie chart (2-4 slices) | Simple proportions, percentages | Complex breakdowns (>5 slices) |
| **Relationship between two variables** | Scatter plot | Finding correlations, patterns | No clear relationship exists |
| **Geographic data** | Heat map / Choropleth | Regional comparisons, location-based | Data isn't location-specific |
| **Hierarchical data** | Tree map / Sunburst | Nested categories, drill-down | Flat data structures |
| **Comparing multiple metrics** | Table | Precise values matter | Simple comparisons |
| **Progress to goal** | Gauge / Progress bar | Single metric tracking | Multiple metrics |

---

## Line Charts (Trends Over Time)

### When to Use

- Showing trends, growth, or changes over time
- Comparing multiple time series (2-4 lines maximum)
- Identifying patterns, inflections, or seasonality
- Revenue, growth metrics, adoption rates over time

### Design Best Practices

✅ **Do:**

- Use contrasting colors for multiple lines
- Label axes clearly with units (%, $M, users, etc.)
- Annotate key events or inflection points
- Start Y-axis at zero (or clearly indicate if not)
- Limit to 3-4 lines maximum

❌ **Don't:**

- Use 3D effects (distorts perception)
- Start Y-axis at arbitrary number to exaggerate trends
- Show too many lines (becomes "spaghetti chart")
- Use similar colors for different lines
- Omit time period labels

### Example Use Cases

**Good:**

- "Monthly recurring revenue growth over last 12 months"
- "Customer churn rate trend (2022-2024)"
- "Feature adoption: Premium vs Standard users"

**Bad:**

- "Comparing 10 products' performance" (too many lines)
- "Single data point" (just use a number)

---

## Bar Charts (Category Comparisons)

### When to Use

- Comparing values across categories
- Ranking items (highest to lowest)
- Before/after comparisons
- Period-over-period comparisons (Q1 vs Q2)

### Horizontal vs Vertical

- **Horizontal bars**: Long category labels, easier to read names
- **Vertical bars**: Time periods or short labels, traditional feel

### Design Best Practices

✅ **Do:**

- Sort by value (descending) unless logical order exists
- Use consistent color (or color by meaningful groups)
- Show data labels if precise values matter
- Leave space between bars for readability
- Use horizontal bars for 5+ categories with long names

❌ **Don't:**

- Use 3D bars (distorts comparison)
- Show more than 10 categories (too cluttered)
- Use random colors for each bar
- Make bars too thin or too wide
- Omit axis labels and units

### Example Use Cases

**Good:**

- "Top 5 revenue-generating products"
- "Sales performance by region"
- "Q2 vs Q3 pipeline comparison"

**Bad:**

- "Monthly trend for 24 months" (use line chart)
- "Showing proportions of a whole" (use pie chart)

---

## Pie Charts (Parts of Whole)

### When to Use

- Showing simple proportions (2-4 segments only)
- Percentage breakdowns
- Market share, budget allocation
- **Only when parts sum to 100%**

### Design Best Practices

✅ **Do:**

- Limit to 2-4 segments (5 maximum)
- Start largest segment at 12 o'clock
- Proceed clockwise by size
- Show percentages on or near segments
- Use contrasting colors
- Consider donut chart for modern look

❌ **Don't:**

- Use for more than 5 segments
- Use 3D or exploded segments (distorts perception)
- Use when precise comparison matters (use bar chart)
- Show segments that don't sum to 100%
- Use similar shades for different segments

### Example Use Cases

**Good:**

- "Revenue by product line (3 products)"
- "Budget allocation: Engineering 60%, Sales 25%, Marketing 15%"
- "Market share: Us vs Top 2 competitors"

**Bad:**

- "Breakdown of 12 cost categories" (too many slices)
- "Comparison where exact values matter" (use bar chart)
- "Trend over time" (use line chart)

### When to Use Bar Chart Instead

If you have more than 5 categories, or if precise comparison matters, use a horizontal bar chart:

- Shows all categories clearly
- Easier to compare exact values
- Can display many more categories

---

## Scatter Plots (Relationships)

### When to Use

- Showing correlation between two variables
- Identifying outliers or clusters
- Demonstrating relationships (positive, negative, none)
- Segmentation analysis

### Design Best Practices

✅ **Do:**

- Label both axes with units
- Add trend line if relationship exists
- Use color to show categories/segments
- Annotate key outliers
- Include R² if showing statistical relationship

❌ **Don't:**

- Use if no relationship exists (just confuses)
- Overcrowd with too many points (>100)
- Forget to label axes
- Use 3D scatter plots (hard to read)

### Example Use Cases

**Good:**

- "Customer lifetime value vs acquisition cost by segment"
- "Feature usage vs customer satisfaction score"
- "Deal size vs sales cycle length"

**Bad:**

- "Showing categories without relationship" (use bar chart)
- "Trends over time" (use line chart)

---

## Tables (Detailed Comparison)

### When to Use

- Precise values are critical (financial data)
- Comparing multiple metrics across categories
- Executive needs to reference exact numbers
- Small datasets (5 rows × 4 columns maximum)

### Design Best Practices

✅ **Do:**

- Limit to 5 rows × 4 columns for executive slides
- Right-align numbers, left-align text
- Include units in column headers ($M, %, etc.)
- Highlight key cells with color or bold
- Use alternating row colors for readability
- Sort by most important column

❌ **Don't:**

- Show raw spreadsheet data (simplify first)
- Use for simple comparisons (use chart instead)
- Include too many decimals (round appropriately)
- Forget units
- Make it dense and hard to scan

### Example Use Cases

**Good:**

- "Quarterly financial summary: Revenue, Costs, Margin, Growth"
- "Feature comparison: Us vs Top 3 competitors"
- "Investment options: Cost, ROI, Timeline, Risk"

**Bad:**

- "Simple before/after comparison" (use bar chart)
- "Trend over 12 months" (use line chart)
- "20 rows of detailed data" (move to appendix)

---

## Heat Maps (Patterns and Intensity)

### When to Use

- Geographic comparisons (sales by region/state)
- Time-based patterns (activity by day/hour)
- Showing intensity or density
- Matrix comparisons (features × segments)

### Design Best Practices

✅ **Do:**

- Use intuitive color gradient (light to dark)
- Label all axes clearly
- Include legend with values
- Use colorblind-safe palette
- Annotate highest/lowest values

❌ **Don't:**

- Use random colors (stick to gradient)
- Use for simple comparisons (overkill)
- Make it too granular (hard to read)

### Example Use Cases

**Good:**

- "Sales performance by state"
- "Support ticket volume by time of day"
- "Feature adoption across customer segments"

**Bad:**

- "Simple A vs B comparison" (use bar chart)
- "Trend over time" (use line chart)

---

## Gauges and Progress Bars (Goal Tracking)

### When to Use

- Single metric progress to goal
- Simple status indicator
- KPI dashboards
- Performance scorecards

### Design Best Practices

✅ **Do:**

- Show current value and target clearly
- Use color to indicate status (green = good, red = concerning)
- Include percentage or absolute progress
- Keep it simple

❌ **Don't:**

- Use for multiple metrics (use table or bars)
- Make it overly decorative
- Use confusing color schemes

### Example Use Cases

**Good:**

- "Q3 revenue: $8.2M of $10M target (82%)"
- "Annual customer acquisition: 1,240 of 1,500 goal"

**Bad:**

- "Comparing 5 different goals" (use bar chart)
- "Complex multi-dimensional progress" (use table)

---

## Tree Maps and Sunburst Charts (Hierarchical Data)

### When to Use

- Nested categories (parent-child relationships)
- Proportional hierarchies
- Drill-down analysis
- Complex breakdowns (department → team → projects)

### Design Best Practices

✅ **Do:**

- Use size to show proportion
- Use color to show category or metric
- Label clearly (size permitting)
- Limit to 2-3 levels of hierarchy

❌ **Don't:**

- Use for simple data (overkill)
- Make it too complex (>20 boxes)
- Use similar colors for different categories

### Example Use Cases

**Good:**

- "Revenue by product line → product → SKU"
- "Cost breakdown: Department → Team → Category"
- "Feature usage by customer segment → company size → industry"

**Bad:**

- "Simple category comparison" (use bar chart)
- "Two-level hierarchy with 3 items" (use pie or bar)

---

## Combination Charts (Multiple Data Types)

### When to Use

- Showing two related metrics with different scales
- Combining trend (line) with comparison (bar)
- Revenue + growth rate, quantity + percentage

### Design Best Practices

✅ **Do:**

- Use two Y-axes (left and right) with clear labels
- Use different chart types (bar + line) for clarity
- Keep it simple (don't overload)
- Explain the dual axis clearly

❌ **Don't:**

- Use if relationship between metrics isn't clear
- Show more than 2 metrics
- Use similar colors for different metrics

### Example Use Cases

**Good:**

- "Revenue (bars) + growth rate (line)"
- "Number of deals (bars) + average deal size (line)"
- "Headcount (bars) + revenue per employee (line)"

**Bad:**

- "Two unrelated metrics" (use separate charts)
- "More than 2 metrics" (too complex)

---

## Chart Design Principles

### Color Psychology

- **Blue**: Trust, corporate, stable (financial data, baseline)
- **Green**: Positive, growth, success (increases, good outcomes)
- **Red**: Urgent, risk, negative (decreases, alerts, problems)
- **Orange**: Warning, caution (metrics to watch)
- **Purple**: Premium, innovation (new initiatives)
- **Gray**: Neutral, baseline (comparison points, historical)

**Colorblind-Safe Combinations:**

- Blue + Orange (not blue + purple)
- Green + Red + Blue (not just green + red)
- Use patterns or shapes in addition to color

### Typography

- **Title**: 24-28pt, bold, insight-driven
  - ✅ "Premium Leads Increase Pipeline 35%"
  - ❌ "Q2 Results"

- **Axis labels**: 16-18pt, clear units
- **Data labels**: 14-16pt (if shown)
- **Legend**: 14-16pt, clear and concise

### Simplicity Rules

1. **Remove chart junk**: Unnecessary gridlines, borders, shadows, 3D effects
2. **Highlight what matters**: Use color to draw attention to key data points
3. **Tell a story**: Chart title should state the insight, not just the topic
4. **Test at distance**: Can you read it from 10 feet away?

---

## Chart Selection Decision Tree

```
START: What do you want to show?

├─ Trend over time?
│  └─ Use LINE CHART
│
├─ Compare categories?
│  ├─ 2-7 categories?
│  │  └─ Use BAR CHART
│  ├─ 8+ categories?
│  │  └─ Use HORIZONTAL BAR CHART or simplify
│  └─ Need precise values?
│     └─ Use TABLE
│
├─ Show parts of a whole?
│  ├─ 2-4 parts?
│  │  └─ Use PIE CHART
│  └─ 5+ parts?
│     └─ Use HORIZONTAL BAR CHART instead
│
├─ Show relationship between two variables?
│  └─ Use SCATTER PLOT
│
├─ Show geographic patterns?
│  └─ Use HEAT MAP
│
├─ Show hierarchy or nested data?
│  └─ Use TREE MAP
│
└─ Show progress to goal?
   └─ Use PROGRESS BAR or GAUGE
```

---

## Common Mistakes to Avoid

### Mistake 1: Wrong Chart Type

**Problem**: Using pie chart for 10 categories
**Solution**: Use horizontal bar chart sorted by value

### Mistake 2: 3D Effects

**Problem**: 3D bars/pies distort perception
**Solution**: Always use 2D charts for accuracy

### Mistake 3: No Context

**Problem**: Showing numbers without comparison or baseline
**Solution**: Always include target, baseline, or prior period

### Mistake 4: Too Much Data

**Problem**: Trying to show everything on one chart
**Solution**: Simplify main chart, move details to appendix

### Mistake 5: Misleading Scales

**Problem**: Y-axis starts at 95 to exaggerate 5% change
**Solution**: Start at zero or clearly indicate truncated axis

### Mistake 6: Poor Color Choices

**Problem**: Using red/green only (colorblind issue)
**Solution**: Use blue/orange or add patterns

### Mistake 7: Unreadable Labels

**Problem**: Tiny fonts, overlapping text
**Solution**: Minimum 14pt fonts, rotate labels if needed

### Mistake 8: No Title or Insight

**Problem**: Chart titled "Revenue"
**Solution**: Title with insight: "Revenue Grew 34% YoY, Exceeding Target"

---

## Testing Your Chart

Before including in executive presentation:

- [ ] **Glance test**: Can you understand it in 5 seconds?
- [ ] **Distance test**: Can you read it from 10 feet away?
- [ ] **Insight test**: Does the title state the insight clearly?
- [ ] **Simplicity test**: Can you remove anything without losing the story?
- [ ] **Color test**: Works in black & white or for colorblind viewers?
- [ ] **Context test**: Are units, timeframes, and baselines clear?
- [ ] **Action test**: Does this chart support a decision or recommendation?

If your chart fails any of these tests, revise or remove it.

---

## Tools for Creating Charts

**PowerPoint/Keynote:**

- Built-in charts (adequate for most needs)
- Pros: Easy, integrated, familiar
- Cons: Limited customization

**Excel:**

- More chart types and customization
- Pros: Powerful, flexible, copy to PPT
- Cons: Can be complex, tempting to over-design

**Tableau/Power BI:**

- Advanced analytics and dashboards
- Pros: Interactive, powerful, handles big data
- Cons: Overkill for simple executive slides, requires training

**Python (Matplotlib/Seaborn/Plotly):**

- Programmatic chart generation
- Pros: Reproducible, customizable, version controlled
- Cons: Requires coding skills

**For executive presentations:** PowerPoint or Excel charts are usually sufficient. Focus on clarity and simplicity over complex tools.

---

## Examples: Good vs Bad

### Example 1: Revenue Growth

**Bad:**

- 3D pie chart with 8 slices
- No title or insight
- Colors are rainbow spectrum
- Labels overlap

**Good:**

- Line chart showing monthly trend
- Title: "Revenue Grew 34% YoY, Exceeding $10M Target in Q3"
- Clear axis labels: "$M" and "Month"
- Target line annotated
- Simple blue color with green for target achieved

### Example 2: Regional Performance

**Bad:**

- Table with 50 rows of state-by-state data
- No sorting or highlighting
- Tiny fonts (10pt)
- No context or comparison

**Good:**

- Heat map of US states colored by performance
- Title: "West Coast and Texas Drive 62% of Revenue Growth"
- Top 5 states labeled with values
- Color scale from light (low) to dark (high)
- Footnote: "Based on Q2 2024 data"

### Example 3: Feature Comparison

**Bad:**

- 8 columns × 20 rows of features
- All text, no visual hierarchy
- Equal weight to all features

**Good:**

- Simple table: 5 rows × 4 columns
- "Must-have features" only (20-row version in appendix)
- Title: "We Match or Exceed Competitors on Critical Features"
- Key differentiators highlighted in green
- Gaps highlighted in yellow with plan to address

---

*Choose charts that clarify, not decorate. Every chart should answer: "So what?" If it doesn't support your narrative or recommendation, remove it.*
