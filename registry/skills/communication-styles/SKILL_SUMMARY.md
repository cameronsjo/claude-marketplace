# Communication Styles Skill - Comprehensive Summary

## Skill Overview

**Name:** Communication Style Flexing Skill

**Purpose:** Master the art of adapting communication style to build rapport, influence decisions, and collaborate effectively with any stakeholder using the research-backed Social Styles Framework.

**Based on:** Gartner research "Quick Answer: How to Flex Your Communication Style" (G00799890, August 2023) by Bolton & Bolton.

**Size:** 35KB SKILL.md + 64KB resources (99KB total)

**Lines of code/documentation:** 4,342 lines

---

## Skill Structure

```
communication-styles/
├── SKILL.md (35KB, 1,061 lines)
│   └── Comprehensive guide to Social Styles Framework
│
├── README.md (197 lines)
│   └── Quick overview and GitHub discoverability
│
├── resources/
│   ├── quick-reference-cheat-sheet.md (8.6KB, 297 lines)
│   │   └── One-page reference for all four styles
│   │
│   ├── email-templates.md (19KB, 669 lines)
│   │   └── Email templates for each style with examples
│   │
│   ├── presentation-frameworks.md (20KB, 762 lines)
│   │   └── Multi-style presentation structures
│   │
│   └── stakeholder-analysis-worksheet.md (16KB, 576 lines)
│       └── Fillable worksheet for stakeholder planning
│
├── scripts/
│   └── style-diagnostic.py (780 lines)
│       └── Interactive Python tool for style assessment
│
├── INTEGRATION_GUIDE.md
│   └── How this skill integrates with other skills
│
└── TEST_PROMPTS.md
    └── Test cases for skill activation
```

---

## Core Framework: The Four Social Styles

### Visual Model

```
                      RELATIONSHIP
                           ↑
                AMIABLE  |  EXPRESSIVE
           (People)      |      (Ideas)
      ASK ←────────────────────────────→ TELL
           (Process)     |     (Results)
                ANALYTIC |    DRIVER
                           ↓
                         TASK
```

### Two Key Dimensions

1. **Relationship vs. Task Focus**
   - Relationship-oriented: Prioritize people, emotions, consensus
   - Task-oriented: Prioritize results, processes, data

2. **Ask vs. Tell Communication**
   - Ask: Communicate through questions, seek input, reserved
   - Tell: Communicate through statements, share opinions, assertive

### Four Styles Summary

| Style | Focus | Seeks | Decision | Saves | Questions | Stress Response |
|-------|-------|-------|----------|-------|-----------|----------------|
| **AMIABLE** | People | Consensus | Slow/thoughtful | Relationships | Why | Acquiesce |
| **EXPRESSIVE** | Ideas | Recognition | Fast/spontaneous | Effort | Who | Attack |
| **ANALYTIC** | Process | Accuracy | Slow/systematic | Face | How | Avoid |
| **DRIVER** | Results | Results | Decisive | Time | What | Autocracy |

---

## Key Content Sections in SKILL.md

### 1. Core Framework (Lines 1-450)
- Social Styles Framework introduction
- Detailed profiles of all four styles
- Engagement strategies for each
- Factors that create tension
- Power words by style
- Stress responses

### 2. Diagnostic Tools (Lines 451-550)
- 20-second assessment method
- Observable behaviors checklist
- Stress response recognition
- Style compatibility matrix

### 3. Application Scenarios (Lines 551-750)
- Stakeholder presentations
- Conflict resolution
- Executive emails (4 versions of same message)
- Board presentations
- Negotiations

### 4. Communication Templates (Lines 751-850)
- Meeting openers by style
- Email subject lines
- Closing statements
- Multi-style presentations

### 5. Advanced Techniques (Lines 851-950)
- Multi-style presentations
- Real-time style flexing (mirror and lead)
- Written communication adaptation
- Conflict de-escalation by style

### 6. Practice and Troubleshooting (Lines 951-1061)
- Self-assessment questionnaire
- Practice exercises
- Common pitfalls and solutions
- Troubleshooting guide
- Best practices summary

---

## Resource Files

### Quick Reference Cheat Sheet (8.6KB)
**Purpose:** One-page printable reference

**Contents:**
- 4-style visual framework
- Engagement strategies table
- Power words by style
- Stress responses
- Compatibility matrix
- Email/meeting formulas
- Emergency flex guide

**Use case:** Print and keep at desk, review before meetings

---

### Email Templates (19KB)
**Purpose:** Pre-written email structures for each style

**Contents:**
- 4 templates per style (12 total)
- Comparative example (same message, 4 styles)
- Subject line formulas
- Email checklist by style
- Emergency email rewrites

**Use case:** Copy/paste starting point for stakeholder emails

---

### Presentation Frameworks (20KB)
**Purpose:** Multi-style presentation structures

**Contents:**
- Four-layer presentation framework
- Style-specific presentation formats
- Board presentation structure (30 min)
- Stakeholder meeting framework (60 min)
- Visual design principles by style
- Delivery tips by audience style
- Virtual presentation adaptations

**Use case:** Structure presentations for mixed audiences

---

### Stakeholder Analysis Worksheet (16KB)
**Purpose:** Fillable planning template

**Contents:**
- Stakeholder profile templates
- Quick diagnostic questions
- Engagement strategy planning
- Communication timeline
- Meeting planning sections
- Post-meeting follow-up checklist
- Success metrics

**Use case:** Plan comprehensive stakeholder engagement

---

## Python Diagnostic Script

**File:** `scripts/style-diagnostic.py` (780 lines)

**Capabilities:**
1. **Self-assessment mode:** Interactive questionnaire to identify your own style
2. **Other assessment mode:** Diagnose someone else's style through behavioral observations
3. **Stakeholder analysis mode:** Create communication plan for multiple stakeholders

**Usage:**
```bash
# Self-assessment
python style-diagnostic.py --self

# Assess someone else
python style-diagnostic.py --other

# Stakeholder analysis
python style-diagnostic.py --stakeholder-analysis

# Interactive menu
python style-diagnostic.py
```

**Features:**
- 20-second quick diagnostic
- Detailed behavioral observations
- Style scoring with primary/secondary identification
- Personalized recommendations
- Engagement strategy generation
- Stakeholder conflict identification
- Group communication planning

---

## Skill Activation Keywords

### Primary Triggers
- communication style
- stakeholder engagement
- executive communication
- flex communication
- adapt communication
- social styles
- communication preferences

### Style-Specific Triggers
- relationship-focused / task-focused
- consensus / results-oriented
- data-driven / story-driven
- analytical / decisive
- people-focused / process-focused

### Scenario Triggers
- present to executives
- communicate with stakeholder
- influence decision
- build rapport
- resolve conflict
- engagement strategy
- board presentation
- email [executive/stakeholder]

---

## Integration with Other Skills

### Primary Integrations

**executive-data-storytelling:**
- Combine data narrative with audience adaptation
- Use storytelling for structure, communication-styles for delivery

**political-attack-neutralization:**
- Tailor attack neutralization to attacker's communication style
- Style-matched defensive strategies

**feature-flags:**
- Explain technical concepts to different stakeholder types
- Get buy-in from diverse audiences

**api-design / python-development / cli-development:**
- Present technical decisions to non-technical stakeholders
- Justify technical approaches to business leaders

**security-review:**
- Communicate security findings appropriately by audience
- Frame vulnerabilities for Driver (risk), Analytic (technical), Expressive (story), Amiable (impact)

### Integration Pattern

1. Domain skill provides **substance** (what to communicate)
2. Communication skill provides **delivery** (how to communicate)
3. Combined: Content matched to audience

---

## Unique Value Propositions

### What Makes This Skill Special

1. **Research-backed framework:** Based on validated Gartner research, not generic advice

2. **Actionable and immediate:** 20-second diagnostic provides instant value

3. **Comprehensive coverage:** 35KB of detailed guidance with real-world examples

4. **Practical tools:** Working Python script, fillable worksheets, copy/paste templates

5. **Multi-scenario application:** Works for emails, presentations, meetings, conflicts, negotiations

6. **Style-specific depth:** Not just "adapt to audience" but HOW to adapt with specific tactics

7. **Integration-ready:** Works with other skills to provide comprehensive solutions

8. **Relationship preservation:** Focuses on removing barriers, not manipulation

---

## Expected Usage Patterns

### High-Frequency Use Cases

1. **Executive email writing** - User needs to email senior leaders
2. **Presentation preparation** - User preparing for stakeholder presentation
3. **Conflict resolution** - User dealing with communication breakdowns
4. **Stakeholder engagement** - User building relationships with business partners
5. **Board presentations** - User presenting to diverse board members

### Medium-Frequency Use Cases

1. **Team communication improvement** - User optimizing team dynamics
2. **Negotiation preparation** - User preparing for negotiations
3. **Change management** - User rolling out organizational changes
4. **Coaching/mentoring** - User adapting approach to mentee's style
5. **Self-improvement** - User learning their own style and flex areas

### Low-Frequency Use Cases

1. **Hiring/interviewing** - User adapting interview style
2. **Customer engagement** - User adapting to customer communication styles
3. **Crisis communication** - User managing high-stakes communications
4. **Cross-cultural communication** - User bridging communication differences

---

## Success Metrics

### Skill is successful when:

1. **Accurate diagnosis:** User can identify communication styles in 20 seconds
2. **Practical application:** User successfully adapts communication approach
3. **Improved outcomes:** User reports better stakeholder engagement
4. **Template usage:** User leverages email/presentation templates
5. **Integration:** Skill combines effectively with other skills
6. **Relationship improvement:** User builds better working relationships
7. **Conflict reduction:** User navigates opposite-style conflicts effectively

---

## Quality Indicators

### Content Quality
✅ Comprehensive: 35KB SKILL.md with deep coverage
✅ Practical: Real-world examples throughout
✅ Actionable: Specific tactics, not generic advice
✅ Research-backed: Based on validated framework
✅ Complete: No placeholder content

### Structure Quality
✅ Clear organization: Logical flow from framework to application
✅ Progressive disclosure: Quick reference → detailed guidance → advanced techniques
✅ Multiple entry points: Cheat sheet, templates, scripts, main doc
✅ Integration-ready: Cross-references other skills

### Tool Quality
✅ Working script: Tested Python diagnostic tool
✅ Practical templates: Copy/paste email and presentation structures
✅ Fillable worksheets: Stakeholder analysis planning tool
✅ Quick references: One-page cheat sheet

### Discoverability
✅ Clear triggers: Multiple keyword patterns
✅ Use cases documented: 20+ example prompts
✅ README optimized: GitHub discoverability
✅ Related skills linked: Integration patterns documented

---

## Maintenance and Updates

### When to update this skill:

1. **New research published** - Gartner or other validated research on communication styles
2. **User feedback** - Patterns of confusion or misapplication
3. **New scenarios** - Additional application contexts identified
4. **Integration opportunities** - New skills created that benefit from communication adaptation
5. **Template improvements** - Better email/presentation structures discovered

### Version history:

**v1.0 (Nov 2025):**
- Initial creation based on Gartner G00799890
- Four social styles framework
- Comprehensive templates and tools
- Python diagnostic script
- Integration guide

---

## Known Limitations

1. **Cultural context:** Framework developed in Western business context, may need adaptation for other cultures

2. **Style evolution:** People's styles may shift over time or in different contexts

3. **Oversimplification risk:** Four-box model is useful but not absolute truth

4. **Self-awareness required:** User must accurately observe behaviors to diagnose styles

5. **Authenticity balance:** Flexing must remain genuine, not manipulative

---

## Comparison to Existing Solutions

### vs. Generic "Communication Skills" Advice
✅ Research-backed framework
✅ Specific diagnostic method (20 seconds)
✅ Concrete tactics, not platitudes
✅ Style-specific power words and strategies

### vs. DISC/Myers-Briggs
✅ Simpler (4 styles vs. 16 types)
✅ Observable behaviors vs. self-reported preferences
✅ Focused on professional communication specifically
✅ Actionable engagement strategies included

### vs. Emotional Intelligence Training
✅ More structured framework
✅ Faster diagnostic (20 seconds vs. lengthy assessment)
✅ Specific to communication styles, not general EQ
✅ Immediately applicable templates

---

## File Paths Reference

**Main documentation:**
- `~/.claude/skills/communication-styles/SKILL.md`
- `~/.claude/skills/communication-styles/README.md`

**Resources:**
- `~/.claude/skills/communication-styles/resources/quick-reference-cheat-sheet.md`
- `~/.claude/skills/communication-styles/resources/email-templates.md`
- `~/.claude/skills/communication-styles/resources/presentation-frameworks.md`
- `~/.claude/skills/communication-styles/resources/stakeholder-analysis-worksheet.md`

**Tools:**
- `~/.claude/skills/communication-styles/scripts/style-diagnostic.py`

**Meta:**
- `~/.claude/skills/communication-styles/INTEGRATION_GUIDE.md`
- `~/.claude/skills/communication-styles/TEST_PROMPTS.md`
- `~/.claude/skills/communication-styles/SKILL_SUMMARY.md`

---

## Quick Start for Users

**Step 1: Identify a stakeholder you need to communicate with**

**Step 2: Run 20-second diagnostic**
- Relationship or Task focus?
- Ask or Tell communication?

**Step 3: Determine their style**
- Relationship + Ask = Amiable
- Relationship + Tell = Expressive
- Task + Ask = Analytic
- Task + Tell = Driver

**Step 4: Apply engagement strategies**
- Use their power words
- Match their decision speed
- Address their primary interest
- Avoid their tension factors

**Step 5: Use templates**
- Email templates by style
- Presentation frameworks
- Meeting openers/closers

**Step 6: Observe and adjust**
- Watch for feedback
- Flex in real-time
- Build rapport

---

## Final Notes

This skill represents a production-ready, comprehensive implementation of the Social Styles Framework for professional communication. It provides:

✅ Research-backed methodology
✅ Practical, actionable guidance
✅ Working diagnostic tools
✅ Extensive templates and examples
✅ Integration with other skills
✅ Real-world application scenarios

The skill is designed for autonomous discovery by Claude based on trigger keywords related to stakeholder communication, executive engagement, presentation preparation, conflict resolution, and communication style adaptation.

**Total development:** ~4,300 lines of documentation and code across 9 files.

**Skill readiness:** Production-ready, fully tested, comprehensive.

**Expected impact:** Significantly improved stakeholder communication effectiveness through style-aware engagement strategies.
