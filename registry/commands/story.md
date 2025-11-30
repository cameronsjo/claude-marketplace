---
description: Transform data/metrics into executive narratives using What/Why/Next framework
category: business
argument-hint: "[topic or metric]"
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Claude Command: Executive Story

Transform data, metrics, and analysis into compelling executive narratives using the Gartner-backed What/Why/Next framework.

## Usage

Create executive narrative from data/analysis:
```
/exec-story Q3 revenue performance
```

Transform technical analysis to executive summary:
```
/exec-story security audit findings
```

Build business case:
```
/exec-story infrastructure investment
```

## What This Command Does

This command uses the executive-data-storytelling skill to transform your content into executive-ready narratives.

### Step 1: Understand the context

Ask clarifying questions to gather necessary information:

1. **What's the topic/metric?**
   - If provided as argument, use it
   - If not, ask: "What topic or metric should I focus on?"

2. **What's the audience?**
   - CEO/Board/C-suite/Department heads?
   - What's their primary priority? (Growth/Technology/Workforce/Financial)

3. **What's the format?**
   - Board memo, presentation slide, dashboard, business case, email?
   - Any page/slide limits?

4. **What data do you have?**
   - Where is the data? (file, inline, need to analyze)
   - Metrics, trends, comparisons available?

### Step 2: Activate the executive storytelling skill

Invoke the skill to get the full framework:
```
Use the executive-data-storytelling skill to help transform this into an executive narrative.
```

### Step 3: Gather and analyze data

If data is in files:
- Read the relevant files
- Extract key metrics
- Identify trends and patterns

If data needs analysis:
- Help user identify what metrics to include
- Suggest data visualizations
- Calculate key ratios/comparisons

### Step 4: Structure using What/Why/Next

Build the narrative following the framework:

**WHAT (Current State)**
- Key metric and context
- Performance vs target/expectation
- Connection to CEO priority (Growth/Technology/Workforce/Financial)
- Impact on business goals

**WHY (Root Cause)**
- Data-driven analysis of drivers
- Quantify contributing factors
- Depersonalize (focus on problem, not people)
- Show causal relationships with data

**NEXT (Recommendations)**
- Specific, actionable recommendations
- Expected outcomes with metrics
- Investment required (time/money/resources)
- Timeline and milestones
- ROI or business impact quantified
- **Decision required** (state explicitly)

### Step 5: Apply executive communication rules

Ensure the narrative follows these principles:

1. **3-5 bullets maximum per slide/section**
2. **One idea per slide/section**
3. **Lead with insight** (conclusion first, not background)
4. **Depersonalize failures** (data-driven, not defensive)
5. **State decision required** (be explicit about the ask)
6. **Define or eliminate jargon** (executives span domains)
7. **Quantify everything** (metrics, timelines, investments, outcomes)

### Step 6: Format for the medium

**For board memos:**
- Executive summary at top (What/Why/Next in 3-4 paragraphs)
- Supporting details below
- Appendix for detailed data

**For presentations:**
- One slide per major point
- Visual hierarchy (large numbers, small supporting text)
- Simple charts (bar, line, pie only)
- Minimal animation/effects

**For dashboards:**
- Critical metrics above the fold
- Traffic light indicators (red/yellow/green)
- Trend arrows (↑↓→)
- Context tooltips

**For business cases:**
- Problem statement (WHAT)
- Analysis (WHY)
- Recommendation with ROI (NEXT)
- Decision required section

### Step 7: Quality check

Run through the pre-presentation checklist:

**Content checks:**
- [ ] Metrics align with CEO priorities
- [ ] Conclusion stated upfront
- [ ] Root cause supported by data
- [ ] Recommendations specific and actionable
- [ ] ROI/business impact quantified
- [ ] Decision required explicitly stated
- [ ] Timeline and milestones clear

**Communication checks:**
- [ ] No more than 5 bullets per section
- [ ] One idea per slide/section
- [ ] Jargon defined or eliminated
- [ ] Failures depersonalized
- [ ] Numbers properly contextualized

**Visual checks:**
- [ ] Charts simple and clear
- [ ] Text large enough to read
- [ ] Color meaningful (not decorative)
- [ ] Consistent formatting

### Step 8: Deliver the output

Provide the narrative in requested format:
- Write to file if creating memo/document
- Display formatted text if for presentation
- Show structured outline if early draft

Include:
- **Main narrative** (What/Why/Next)
- **Supporting data points** (for Q&A preparation)
- **Suggested visuals** (chart types and data)
- **Key messages** (3-5 takeaways)

## CEO Priority Mapping

Always connect metrics to one of these (2024 Gartner data):

**Growth (59% of CEOs prioritize)**
- Revenue growth, market share expansion
- Customer acquisition, retention, lifetime value
- New market entry, product launches
- Sales velocity, conversion rates

**Technology (29%)**
- Digital transformation progress
- AI/ML adoption and outcomes
- Platform modernization
- Innovation metrics, patent pipeline

**Workforce (25%)**
- Talent retention, time-to-hire
- Skills development, training ROI
- Productivity metrics, efficiency gains
- Employee engagement, satisfaction

**Financial (22%)**
- Cost optimization, margin improvement
- Profitability, cash flow
- ROI on investments
- Budget variance, forecast accuracy

## Example Transformations

### Before (Technical/Weak)
> "We had some performance issues with the API that caused customer complaints. We're working on fixes and expect improvements soon."

### After (Executive-Ready)
> **WHAT**: API response time degraded to 3.2s (vs 500ms target), affecting 40% of enterprise customers and risking $2.4M in Q4 renewals (Growth priority).
>
> **WHY**: Traffic increased 180% following Q3 product launch, exceeding infrastructure capacity. Current architecture limits scale to 5K concurrent users vs 12K actual demand.
>
> **NEXT**: Recommendation: Invest $380K in infrastructure upgrade to support 20K concurrent users, ensuring sub-500ms response times and protecting enterprise renewals. ROI: 6.3x ($2.4M revenue protected). Implementation: 6 weeks. **Decision required: Approve $380K infrastructure investment by Nov 20 for Q4 completion.**

### What changed:
- Quantified problem (3.2s, 40%, $2.4M)
- Connected to CEO priority (Growth)
- Data-driven root cause (180% traffic, capacity limit)
- Specific recommendation ($380K, 20K users, 500ms)
- Clear outcome (protect $2.4M revenue)
- Quantified ROI (6.3x)
- Timeline (6 weeks)
- Explicit decision required

## Tips for Best Results

1. **Have your data ready**: Metrics, trends, comparisons
2. **Know your audience**: Which CEO priority matters most?
3. **Be specific**: Vague recommendations get ignored
4. **Quantify everything**: Investments, outcomes, timelines, ROI
5. **State the ask**: What decision do you need?

## Common Use Cases

**Quarterly business reviews:**
```
/exec-story Q3 performance review
```

**Board memos:**
```
/exec-story missed revenue target explanation
```

**Business cases:**
```
/exec-story cloud migration investment
```

**Executive dashboards:**
```
/exec-story customer retention dashboard
```

**Technical issues for executives:**
```
/exec-story production outage impact
```

---

**Framework Source:** Gartner Research "Use Data Storytelling to Engage the Executive Leadership Team" (G00818015)
**Last Updated:** 2025-11-13
