# Executive Data Storytelling Skill

Transform data and metrics into compelling narratives that drive executive action using proven Gartner research frameworks.

## Overview

This skill teaches you to create data-driven narratives that engage executive leadership teams (ELTs) by:

- **Aligning metrics with CEO priorities** (Growth, Technology, Workforce, Financial)
- **Crafting compelling What/Why/Next narratives** adapted from storytelling frameworks
- **Designing concise, visually appealing presentations** that respect executive attention spans
- **Depersonalizing failures** to focus on problems and solutions, not blame
- **Driving executive action** through clear recommendations and decision frameworks

Based on Gartner's "Use Data Storytelling to Engage the Executive Leadership Team" research (G00818015, September 2024), which found that 84% of high-performing ELTs use data and analytics for decision-making.

## Quick Start

Claude automatically invokes this skill when you:

- Create executive presentations or board memos
- Draft quarterly business reviews or department updates
- Build business cases for investment decisions
- Prepare ELT updates or C-suite communications
- Design executive dashboards
- Transform technical analysis into executive-ready insights

**Example prompts:**

- "Help me create an executive presentation for our Q3 board meeting about AI investment"
- "Draft a board memo explaining why we missed our revenue target"
- "Design an executive dashboard that tells a story about customer retention"
- "Transform this technical analysis into an ELT-ready business case"

## What's Included

### SKILL.md (Comprehensive Guide)

The main skill document includes:

- **The Three-Step Framework**: Identify priorities, draft narrative, create presentation
- **What/Why/Next Structure**: Current state, root cause, recommendations
- **CEO Priority Alignment**: Growth (59%), Technology (29%), Workforce (25%), Financial (22%)
- **Depersonalization Strategies**: Focus on problems, not people
- **Visual Design Best Practices**: 3-5 bullets, one idea per slide, effective charts
- **Use Case Examples**: Sales enablement, innovation, crisis communication, workforce
- **Common Pitfalls**: Jargon overload, burying insights, missing "so what"
- **Advanced Techniques**: Emotional tone, pre-wiring, scenario planning
- **Troubleshooting Guide**: Solutions for common presentation challenges

### Resources Folder

Practical templates and reference materials:

**Templates:**

- `narrative-template.md` - What/Why/Next structure for drafting
- `slide-deck-template.pptx` - PowerPoint with proper formatting
- `priority-alignment-matrix.md` - Map metrics to CEO priorities
- `decision-framework.md` - "Decision Required" slide template
- `appendix-structure.md` - Organize supporting materials
- `scenario-planning-template.md` - Multiple scenario framework

**Checklists:**

- `pre-presentation-checklist.md` - 20-point quality verification
- `visual-design-checklist.md` - Chart and slide design checks
- `jargon-audit-checklist.md` - Eliminate unclear terminology
- `depersonalization-checklist.md` - Ensure analytical tone

**Reference Materials:**

- `ceo-priorities-2024.md` - Gartner data on CEO priorities
- `emotional-tone-guide.md` - When to use surprise, inspiration, reassurance
- `chart-selection-guide.md` - Which chart for which data
- `color-psychology-guide.md` - Strategic color use
- `executive-vocabulary.md` - Common terms by role (CFO, CRO, CTO)

### Scripts Folder

Python utilities for analysis and validation:

- `analyze-presentation.py` - Check for jargon, bullet count, readability
- `priority-mapper.py` - Map your metrics to CEO priorities
- `narrative-validator.py` - Verify What/Why/Next components
- `appendix-organizer.py` - Structure and reference appendix slides

## Key Features

### 1. The What/Why/Next Framework

**WHAT (Opening Image):**

- Current state, on track for targets?
- Align metrics with CEO/ELT priorities

**WHY (Catalyst):**

- Data-driven root cause analysis
- Depersonalize failures (focus on problem, not "we/our team")

**NEXT (Break Into Two):**

- Clear recommendations with outcomes
- Embed emotional tone (surprised, inspired, reassured)

### 2. CEO Priority Alignment

Map every metric to strategic priorities:

- **Growth (59%)**: Revenue, market share, customer acquisition
- **Technology (29%)**: Digital transformation, AI/ML, innovation
- **Workforce (25%)**: Talent retention, skills, productivity
- **Financial (22%)**: Cost optimization, profitability, ROI

### 3. Visual Design Principles

- **3-5 bullets maximum** per slide (67-second attention span)
- **One slide, one idea** principle
- **Simple visuals**: Charts, graphs, relevant images
- **Clear hierarchy**: Title → Insight → Data → Recommendation

### 4. Depersonalization Strategies

Transform defensive language into analytical insights:

❌ "We struggled to deliver features on time"
✅ "Feature delivery was impacted by technical debt requiring 40% more QA cycles"

### 5. Decision-Driven Structure

Always include explicit "Decision Required" section:

- Approval, prioritization, resource allocation, or direction
- Clear options with trade-offs
- Specific timeline and next steps

## Usage Examples

### Example 1: Quarterly Business Review

**Prompt:** "Create an ELT presentation for Q2 results showing we missed our revenue target by 18%"

**Claude will:**

1. Structure narrative using What/Why/Next (current state, root causes, path forward)
2. Depersonalize failure (market factors, systemic issues, data-driven analysis)
3. Align with CEO priorities (likely Growth + Financial)
4. Create 7-10 slide deck with appendix
5. Include clear recommendations and decision required

### Example 2: Investment Business Case

**Prompt:** "Draft a board memo requesting $2M for AI/ML infrastructure"

**Claude will:**

1. Connect to Technology priority (29% of CEO focus)
2. Build What/Why/Next narrative (current limitations, why invest now, expected outcomes)
3. Provide financial model with ROI
4. Include scenario planning (optimistic/base/pessimistic)
5. State decision required with timeline

### Example 3: Crisis Communication

**Prompt:** "Prepare an executive briefing on the security incident from last week"

**Claude will:**

1. Lead with reassuring tone (contained, zero customer impact)
2. Explain incident with depersonalized language
3. Show lessons learned and controls implemented
4. Connect to Technology priority (security-by-design)
5. Provide clear path forward with investment requirements

### Example 4: Dashboard Design

**Prompt:** "Design an executive dashboard for customer retention metrics"

**Claude will:**

1. Focus on strategic implications, not operational details
2. Use simple visuals (trend lines, comparison bars)
3. Connect retention to Growth and Financial priorities
4. Provide "So what" context for each metric
5. Include recommendations based on data trends

## Best Practices Summary

### The 10 Commandments

1. Align with CEO priorities (Growth/Technology/Workforce/Financial)
2. Lead with the insight, don't make executives wait
3. Use What/Why/Next structure systematically
4. Depersonalize failures (problems, not people)
5. Apply 3-5 bullet rule ruthlessly
6. One slide, one idea principle
7. Show with charts, don't tell with paragraphs
8. Be specific about decisions required
9. Build comprehensive appendix for deep dives
10. Pre-wire stakeholders before formal presentation

### Quick Reference Checklist

**Before every executive presentation:**

- [ ] Does narrative follow What/Why/Next?
- [ ] Is every metric aligned with a CEO priority?
- [ ] Are failures depersonalized?
- [ ] Is each slide limited to 3-5 bullets?
- [ ] Does each slide have one clear idea?
- [ ] Have I eliminated jargon?
- [ ] Is the decision required explicit?
- [ ] Have I pre-wired key stakeholders?

## Related Skills

- **api-design**: Apply storytelling to technical API decisions
- **prompt-engineering**: Explain AI patterns using data storytelling
- **security-review**: Present security findings to board with depersonalization
- **feature-flags**: Justify gradual rollout with What/Why/Next
- **mcp-development**: Translate technical benefits to business outcomes

## Integration Patterns

### With Security Review

Present vulnerabilities to board:

1. Use security-review for analysis
2. Use executive-data-storytelling for presentation
3. Apply depersonalization (gaps, not blame)
4. Use "reassured" tone for contained incidents

### With API Design

Present technical strategy:

1. Use api-design for technical accuracy
2. Use executive-data-storytelling for narrative structure
3. Translate technical benefits (scalability) to business outcomes (faster delivery)
4. Connect to Technology or Growth priorities

## Common Pitfalls to Avoid

1. **Jargon overload**: Define acronyms, use plain language
2. **Burying the insight**: Lead with conclusion, not background
3. **Missing "so what"**: Always explain strategic implications
4. **Death by bullets**: 8-12 bullets = slide overload
5. **Ignoring priorities**: Connect departmental metrics to CEO goals
6. **Vague recommendations**: Be specific (action, investment, outcome, timeline)
7. **Defensive posture**: Use data, not excuses
8. **Inconsistent data**: Use same timeframes, cite sources

## Documentation

Full documentation and examples are available in:

- **SKILL.md**: Comprehensive framework guide (20,000+ words)
- **resources/**: Templates, checklists, reference materials
- **scripts/**: Analysis and validation utilities

## Getting Help

**If Claude doesn't invoke this skill automatically:**

Try more specific keywords:

- "Create an executive presentation..."
- "Draft a board memo..."
- "Prepare an ELT update..."
- "Design an executive dashboard..."
- "Build a business case for executives..."

**For deeper customization:**

Reference specific sections:

- "Use the What/Why/Next framework from executive-data-storytelling skill"
- "Apply CEO priority alignment from Gartner framework"
- "Use depersonalization strategies for this failure analysis"

---

**Based on Gartner Research**: "Use Data Storytelling to Engage the Executive Leadership Team" (G00818015, September 2024)

**License**: For use with Claude Code and compatible Claude interfaces
