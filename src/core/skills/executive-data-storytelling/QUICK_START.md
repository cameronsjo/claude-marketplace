# Executive Data Storytelling - Quick Start Guide

## What This Skill Does

Transforms data and metrics into compelling executive narratives using proven Gartner research frameworks.

## When Claude Uses This Skill

Claude automatically activates this skill when you:

- Create executive presentations or board memos
- Draft quarterly business reviews
- Build business cases for executives
- Design executive dashboards
- Transform technical analysis into executive-ready insights

## The 30-Second Framework

### WHAT → WHY → NEXT

1. **WHAT**: Current state + CEO priority connection
2. **WHY**: Data-driven root cause (depersonalized)
3. **NEXT**: Clear recommendations + expected outcomes

## CEO Priorities (2024 Gartner Data)

Connect every metric to one of these:

- **Growth (59%)**: Revenue, market share, customers
- **Technology (29%)**: Digital transformation, AI/ML, innovation
- **Workforce (25%)**: Talent retention, skills, productivity
- **Financial (22%)**: Cost optimization, profitability, ROI

## The 5 Rules

1. **3-5 bullets per slide** (adults have 67-second attention span)
2. **One slide, one idea** (keep it focused)
3. **Lead with insight** (don't make executives wait)
4. **Depersonalize failures** (focus on problem, not "we")
5. **State decision required** (be explicit about the ask)

## Example: Before vs After

### Before (Weak)
>
> "We missed our revenue target because the market was tough and we had some challenges in the sales team."

### After (Strong - What/Why/Next)
>
> **WHAT**: Q2 revenue reached $8.2M vs $10M target (82% attainment).
>
> **WHY**: Enterprise sales cycle extended from 90 to 120 days due to increased budget scrutiny (affecting 40% of pipeline). Product compliance gaps delayed 40% of enterprise deals pending features launched in early Q3.
>
> **NEXT**: Accelerate compliance roadmap (launched July 15) and introduce flexible payment terms to reduce upfront commitment 50%. Revise Q3 target to $9.2M reflecting current market reality. Decision required: Approve $85K investment in payment flexibility implementation.

## Key Resources

- **SKILL.md**: Full framework (58KB, comprehensive)
- **narrative-template.md**: Structure your story
- **pre-presentation-checklist.md**: 150+ quality checks
- **depersonalization-checklist.md**: Present failures analytically
- **chart-selection-guide.md**: Choose the right visuals
- **ceo-priorities-2024.md**: Align with executive priorities

## Quick Scripts

```bash
# Analyze your presentation
python scripts/analyze-presentation.py deck.pptx

# Validate your narrative
python scripts/narrative-validator.py narrative.md
```

## Common Mistakes to Avoid

1. **Jargon overload**: Define acronyms or eliminate them
2. **Burying the insight**: Lead with conclusion, not background
3. **Too many bullets**: More than 5 = slide overload
4. **Defensive language**: "We struggled" → Data-driven analysis
5. **Vague recommendations**: Be specific about action, investment, outcome

## Test Your Understanding

**Bad**: "We need to invest in infrastructure"
**Good**: "Recommendation: Invest $2M in cloud infrastructure to enable 4x traffic scale, supporting launch of enterprise tier targeting $8M annual revenue. ROI: 4x. Decision required by Aug 15 for Q3 launch."

**Why better?**

- Specific investment amount ($2M)
- Clear outcome (4x scale, enable enterprise)
- Business impact ($8M revenue)
- ROI quantified (4x)
- Timeline and decision deadline stated

## Get Started

Try these prompts:

- "Help me create an executive presentation for Q3 board meeting about [topic]"
- "Draft a board memo explaining why we [missed/exceeded] our [metric]"
- "Design an executive dashboard for [customer retention/sales/growth]"
- "Build a business case for [investment] to present to [CEO/CFO/Board]"

---

**Remember**: Executives want insights and decisions, not data dumps. Use this framework to make every presentation count.
