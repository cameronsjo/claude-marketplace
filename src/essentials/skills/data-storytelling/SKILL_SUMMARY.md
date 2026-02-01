# Executive Data Storytelling Skill - Creation Summary

## Overview

This skill teaches Claude to transform data and metrics into compelling narratives that drive executive action using the proven Gartner research framework.

**Based on**: Gartner Research "Use Data Storytelling to Engage the Executive Leadership Team" (G00818015, September 2024)

**Key Finding**: 84% of high-performing ELTs use data and analytics for decision-making, but executives often struggle with operational metrics instead of strategic storytelling.

---

## Skill Structure

```
executive-data-storytelling/
├── SKILL.md (58KB)              # Comprehensive framework documentation
├── README.md (10KB)              # Quick reference and overview
├── TEST_PROMPTS.md               # Testing prompts for skill invocation
├── SKILL_SUMMARY.md             # This file
├── resources/                    # Templates and reference materials
│   ├── narrative-template.md    # What/Why/Next structure template
│   ├── pre-presentation-checklist.md # 150+ point quality checklist
│   ├── ceo-priorities-2024.md   # Gartner CEO priority data with examples
│   ├── depersonalization-checklist.md # Failure communication framework
│   └── chart-selection-guide.md # Visual design best practices
└── scripts/                      # Python analysis utilities
    ├── analyze-presentation.py   # Analyze deck for issues
    └── narrative-validator.py    # Validate What/Why/Next structure
```

---

## Core Framework

### The Three-Step Framework (from Gartner)

**Step 1: Identify Metrics That Align With Executive Peers' Key Priorities**

- CEO priorities: Growth (59%), Technology (29%), Workforce (25%), Financial (22%)
- Mirror language and acronyms used by executives
- Identify who will be affected and whose support you need

**Step 2: Draft a Compelling Data-Based Narrative**

- **WHAT (Opening Image)**: Current state, on track for targets, align with priorities
- **WHY (Catalyst)**: Data-driven root cause, depersonalize failures
- **NEXT (Break Into Two)**: Clear recommendations with outcomes, embed emotional tone

**Step 3: Create Concise, Visually Appealing Presentation**

- 3-5 bullets per slide (67-second attention span)
- "One slide, one idea" principle
- Simple visuals: charts, graphs, relevant images
- Match CEO/peer formatting

---

## Key Features

### 1. What/Why/Next Narrative Structure

Adapted from Blake Snyder's "Save the Cat" storytelling method for executive contexts:

- Current state with metrics
- Root cause analysis with data
- Recommendations with outcomes and timeline

### 2. CEO Priority Alignment

Maps metrics to strategic priorities with specific examples:

- Growth: Revenue, market share, customer acquisition
- Technology: Digital transformation, AI/ML, innovation
- Workforce: Talent retention, skills development, productivity
- Financial: Cost optimization, profitability, ROI

### 3. Depersonalization Strategies

Frameworks for presenting failures analytically, not defensively:

- Focus on problems, not people
- Use data to explain causality
- Externalize appropriately with evidence
- Show lessons learned and corrective actions

### 4. Visual Design Principles

Comprehensive guidance on slide design and chart selection:

- Bullet count limits (3-5 maximum)
- Chart selection matrix (line, bar, pie, scatter, etc.)
- Color psychology for executive presentations
- Typography and readability standards

### 5. Decision-Driven Structure

Templates for explicit decision requests:

- Decision type (approval, prioritization, resource allocation, direction)
- Clear options with trade-offs
- Specific timeline and next steps
- "What happens next" based on each decision

---

## Use Cases Covered

### 1. Executive Presentations

- ELT updates and board meetings
- Quarterly business reviews
- Strategic initiative presentations
- Investment proposals

### 2. Crisis Communications

- Security incidents
- Missed targets or failures
- Operational disruptions
- Market challenges

### 3. Success Stories

- Innovation results (design thinking labs example)
- Performance improvements (retention program example)
- Revenue growth (premium leads example)
- Technology wins

### 4. Investment Requests

- Infrastructure investments
- Team expansion
- New initiatives
- Tool and platform decisions

### 5. Dashboard and Data Visualization

- Executive dashboards
- KPI scorecards
- Performance tracking
- Trend analysis

---

## Resources Provided

### Templates (5 documents)

1. **narrative-template.md** (8.8KB)
   - Complete What/Why/Next structure
   - Stakeholder analysis
   - Language mirroring
   - Jargon audit
   - Decision framework
   - Quality checklist

2. **pre-presentation-checklist.md** (12KB)
   - 150+ point comprehensive checklist
   - Content, design, language, data quality
   - Stakeholder management
   - Practical logistics
   - Quality assurance tests

3. **ceo-priorities-2024.md** (15KB)
   - Gartner research data on CEO priorities
   - Detailed breakdown of each priority category
   - Keywords and metrics by priority
   - How to connect your work to priorities
   - Priority mapping strategy
   - Industry-specific variations

4. **depersonalization-checklist.md** (14KB)
   - Language audit (pronouns, defensive phrases)
   - Transformation techniques (5 methods)
   - Section-specific guidelines
   - Real examples (before/after)
   - Practice exercises
   - Common objections addressed

5. **chart-selection-guide.md** (15KB)
   - Chart selection matrix
   - Design best practices for each chart type
   - Color psychology
   - Typography guidelines
   - Common mistakes to avoid
   - Testing your charts

### Scripts (2 Python utilities)

1. **analyze-presentation.py** (12KB)
   - Analyzes presentation for common issues
   - Checks bullet count, jargon, readability
   - Generates markdown report
   - Command-line tool with verbose mode

2. **narrative-validator.py** (11KB)
   - Validates What/Why/Next structure
   - Checks for required elements
   - Identifies depersonalization issues
   - Provides improvement recommendations

---

## Triggering Patterns

### Primary Keywords (High Confidence)

- executive presentation, board memo, board deck
- ELT update, C-suite presentation
- quarterly business review, QBR
- stakeholder communication (executive)
- business case, investment proposal
- executive dashboard, executive summary
- leadership briefing

### Use Case Patterns

- Creating executive presentations for [topic]
- Drafting board memos about [issue]
- Preparing ELT updates on [initiative]
- Building business cases for [investment]
- Designing executive dashboards for [metrics]
- Transforming technical analysis into executive-ready insights

### Context Indicators

- Presenting to: CEO, CFO, CTO, CRO, board, executives, leadership team
- For: board meeting, executive committee, steering committee
- Purpose: approval, investment request, strategic decision

---

## Example Applications

### Example 1: Missed Revenue Target

**Input**: "We missed our Q2 revenue target by 18%. Help me prepare a presentation for the board."

**Skill Application**:

- Depersonalization strategies (focus on factors, not "we missed")
- What/Why/Next structure
- Root cause analysis with data
- Forward-looking recommendations
- Financial + Growth priority alignment
- Pre-wiring guidance for board members

### Example 2: Innovation Success

**Input**: "Our design thinking labs generated 3 prototypes targeting $2.3M in savings. I need to request expansion funding."

**Skill Application**:

- Technology + Financial priority alignment
- Success story narrative with inspired tone
- Investment request framework with ROI
- Scenario planning (1 lab vs 3 labs)
- Clear decision required
- Appendix with detailed financial model

### Example 3: Executive Dashboard

**Input**: "The CEO wants a one-page dashboard showing our growth metrics."

**Skill Application**:

- Chart selection guide (line charts for trends, bars for comparisons)
- Growth priority focus (59% of CEO priorities)
- "One slide, one idea" principle
- Strategic implications, not operational detail
- Visual hierarchy and simplicity
- "So what" context for each metric

---

## Advanced Techniques

### 1. Emotional Tone Embedding

- Surprised: Unexpected results challenging assumptions
- Inspired: Transformative opportunities
- Reassured: Control and stability during uncertainty
- Concerned: Risks requiring immediate attention

### 2. Pre-Wiring Executive Conversations

- Schedule 1:1s before formal presentation
- Share executive summary in advance
- Solicit feedback and incorporate
- Build coalition of support

### 3. The Appendix Strategy

- Main deck: 7-12 slides for decision
- Appendix: Comprehensive supporting detail
- Know which slide answers which question
- Navigate quickly during Q&A

### 4. The "Decision Required" Framework

- Explicit decision type and ask
- Clear options with trade-offs
- Specific timeline and next steps
- "What happens next" scenarios

### 5. Scenario Planning Approach

- Optimistic/Base/Pessimistic scenarios
- Probabilities and expected outcomes
- Response strategy for each scenario
- Decision points for strategy adjustment

### 6. Competitive Positioning Narrative

- First-mover advantage
- Defensive play
- Leapfrog strategy
- Market expansion

---

## Quality Standards

### Content Excellence

- Every metric connects to CEO priority
- What/Why/Next structure complete
- Data-driven, not speculative
- Depersonalized failures
- Clear recommendations with outcomes

### Design Excellence

- 3-5 bullets maximum per slide
- One slide, one idea
- Appropriate chart types
- High contrast and readability
- Professional color scheme

### Communication Excellence

- No jargon or undefined acronyms
- Mirror executive language
- Confident, not defensive tone
- Specific, actionable recommendations
- Clear decision required

---

## Integration with Other Skills

### With Security Review

- Use security-review for technical analysis
- Use executive-data-storytelling for board presentation
- Apply depersonalization for vulnerabilities
- Connect to Technology + Financial priorities

### With API Design

- Use api-design for technical decisions
- Use executive-data-storytelling for narrative structure
- Translate technical benefits to business outcomes
- Connect to Technology or Growth priorities

### With Feature Flags

- Use feature-flags for technical implementation
- Use executive-data-storytelling to justify approach
- Frame gradual rollout as risk mitigation
- Connect to Technology priority (modern deployment)

---

## Success Metrics

### Skill Effectiveness

- Triggers on 80%+ of relevant executive communication prompts
- Doesn't trigger on non-executive content
- Users report improved presentation quality
- Executives provide positive feedback

### Content Quality

- Narratives follow What/Why/Next structure
- Failures are depersonalized appropriately
- Metrics align with CEO priorities
- Recommendations are clear and actionable

### User Outcomes

- Faster executive presentation creation
- Fewer revisions needed
- Better executive engagement
- More successful approvals/decisions

---

## Continuous Improvement

### Testing Protocol

- Run test prompts weekly (first month)
- Monitor trigger accuracy
- Collect user feedback
- Refine keywords as needed

### Update Triggers

- CEO priority data changes annually
- Update when new Gartner research available
- Add industry-specific variations
- Incorporate user-reported use cases

### Content Updates

- Add new examples from real usage
- Expand troubleshooting guide
- Create additional templates
- Update scripts with new features

---

## Documentation

**Primary Documentation**: SKILL.md (58KB)

- Complete framework guide
- All techniques and examples
- Troubleshooting and best practices

**Quick Reference**: README.md (10KB)

- Overview and key features
- When to use the skill
- Quick start guide
- Integration patterns

**Testing Guide**: TEST_PROMPTS.md

- 29 test prompts
- Expected trigger behavior
- Testing methodology
- Success criteria

---

## File Statistics

| File | Size | Purpose |
|------|------|---------|
| SKILL.md | 58KB | Comprehensive framework documentation |
| README.md | 10KB | Quick reference and overview |
| narrative-template.md | 8.8KB | What/Why/Next structure template |
| pre-presentation-checklist.md | 12KB | 150+ point quality checklist |
| ceo-priorities-2024.md | 15KB | Gartner CEO priority data |
| depersonalization-checklist.md | 14KB | Failure communication framework |
| chart-selection-guide.md | 15KB | Visual design best practices |
| analyze-presentation.py | 12KB | Presentation analysis script |
| narrative-validator.py | 11KB | Narrative validation script |
| **Total** | **~156KB** | Complete skill package |

---

## Next Steps

### Immediate (Post-Creation)

1. ✅ Skill files created and organized
2. ✅ Documentation complete
3. ✅ Scripts executable
4. ⏳ Test with real prompts
5. ⏳ Verify trigger patterns
6. ⏳ Validate resource accessibility

### Short-Term (First Month)

1. Monitor skill invocation patterns
2. Collect user feedback
3. Refine keywords if needed
4. Add examples from real usage
5. Update troubleshooting guide

### Long-Term (Ongoing)

1. Annual update with new CEO priority data
2. Add industry-specific examples
3. Expand script capabilities
4. Create additional templates
5. Integration improvements with other skills

---

## Deliverables Summary

### ✅ Complete Skill Structure

- Primary documentation (SKILL.md, README.md)
- 5 comprehensive resource templates
- 2 working Python scripts
- Test prompts and validation methodology

### ✅ Comprehensive Framework

- Three-step Gartner framework fully documented
- What/Why/Next narrative structure with examples
- CEO priority alignment with 2024 data
- Depersonalization strategies for failures
- Visual design principles and chart selection

### ✅ Practical Tools

- Narrative template (8.8KB)
- Pre-presentation checklist (150+ points)
- Depersonalization checklist with before/after examples
- Chart selection guide with decision tree
- Analysis and validation scripts

### ✅ Integration Guidance

- Cross-references with related skills
- Integration patterns documented
- Use case examples for skill composition
- Clear boundaries (when to use vs. not use)

### ✅ Quality Assurance

- Test prompts for trigger validation
- Success criteria defined
- Continuous improvement protocol
- User feedback collection plan

---

## Key Differentiators

**What makes this skill unique:**

1. **Grounded in Research**: Based on Gartner's 2024 study, not generic advice
2. **Comprehensive**: 58KB of detailed guidance, examples, and best practices
3. **Actionable**: Templates, checklists, and scripts ready to use
4. **Depersonalization Focus**: Unique framework for presenting failures analytically
5. **CEO Priority Data**: Specific 2024 data (Growth 59%, Technology 29%, etc.)
6. **Visual Design**: Detailed chart selection and design principles
7. **Real Examples**: 4 complete use case examples with before/after
8. **Testing Support**: Test prompts and validation methodology included
9. **Script Automation**: Python tools for analysis and validation
10. **Integration Ready**: Works with security-review, api-design, feature-flags skills

---

## Production-Ready Status

This skill is **production-ready** with:

- ✅ Complete documentation (SKILL.md, README.md)
- ✅ Comprehensive resources (5 templates)
- ✅ Working scripts (2 Python utilities)
- ✅ Test prompts for validation
- ✅ Clear trigger patterns
- ✅ Integration documentation
- ✅ Quality standards defined
- ✅ Continuous improvement plan

**Recommended**: Test with 10-15 real executive presentation requests to validate trigger accuracy and content quality before considering fully deployed.

---

*Skill created by Skill Builder agent on 2025-11-10. Based on Gartner Research G00818015, September 2024.*
