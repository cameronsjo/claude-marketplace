# Test Prompts for Executive Data Storytelling Skill

Use these prompts to test if the skill triggers correctly when Claude encounters relevant requests.

## Expected to Trigger Skill

### Executive Presentations

1. "Help me create an executive presentation for our Q3 board meeting about AI investment strategy"
   - **Expected**: Skill loads, applies What/Why/Next framework
   - **Key elements**: CEO priority alignment, visual design principles, decision framework

2. "I need to present to the ELT about why we missed our revenue target this quarter"
   - **Expected**: Skill loads, emphasizes depersonalization strategies
   - **Key elements**: Failure communication, root cause analysis, forward-looking recommendations

3. "Draft a board deck for the security incident from last week"
   - **Expected**: Skill loads, uses crisis communication patterns
   - **Key elements**: Reassured tone, depersonalized analysis, clear remediation

4. "Create an executive summary slide for our product roadmap review"
   - **Expected**: Skill loads, applies slide design principles
   - **Key elements**: 3-5 bullets, one idea per slide, connection to growth priority

### Board Memos and Written Communications

5. "Draft a board memo explaining our decision to pivot our go-to-market strategy"
   - **Expected**: Skill loads, uses narrative structure
   - **Key elements**: What/Why/Next, strategic alignment, decision clarity

6. "Write an executive briefing on customer retention metrics for the CEO"
   - **Expected**: Skill loads, focuses on CEO priorities
   - **Key elements**: Priority alignment (Growth or Workforce), data-driven insights

7. "Help me prepare written remarks for the quarterly business review"
   - **Expected**: Skill loads, applies storytelling framework
   - **Key elements**: Narrative flow, depersonalization if needed, clear recommendations

### Business Cases and Investment Requests

8. "Build a business case for $2M infrastructure investment for the CFO"
   - **Expected**: Skill loads, emphasizes financial priority
   - **Key elements**: ROI calculation, scenario planning, decision framework

9. "Create an investment proposal for expanding our sales team to present to the executive committee"
   - **Expected**: Skill loads, connects to growth priority
   - **Key elements**: Data-driven justification, expected outcomes, clear ask

10. "Draft a funding request for design thinking labs to present to the board"
    - **Expected**: Skill loads, uses innovation narrative pattern
    - **Key elements**: Technology priority, financial ROI, pilot-to-scale approach

### Dashboards and Data Visualization

11. "Design an executive dashboard for customer retention that tells a story"
    - **Expected**: Skill loads, applies visual design principles
    - **Key elements**: Chart selection, strategic implications, "so what" context

12. "Help me create a one-page KPI summary for the leadership team"
    - **Expected**: Skill loads, focuses on simplicity and insight
    - **Key elements**: Key metrics only, visual hierarchy, connection to priorities

13. "Build a performance scorecard for the CRO showing sales metrics"
    - **Expected**: Skill loads, aligns with growth priority
    - **Key elements**: Appropriate chart types, progress to goal, trend analysis

### Quarterly and Annual Reviews

14. "Prepare my Q4 business review presentation for the executive team"
    - **Expected**: Skill loads, full framework application
    - **Key elements**: Complete What/Why/Next, appendix strategy, pre-wiring guidance

15. "Create an annual performance summary for the board of directors"
    - **Expected**: Skill loads, emphasizes strategic storytelling
    - **Key elements**: Year-over-year trends, strategic alignment, forward-looking

### Stakeholder Communications

16. "Draft a communication to executive stakeholders about the delayed product launch"
    - **Expected**: Skill loads, crisis/challenge communication
    - **Key elements**: Depersonalization, transparent analysis, mitigation plan

17. "Write an update for the steering committee on the transformation initiative"
    - **Expected**: Skill loads, progress narrative
    - **Key elements**: Current state, milestones, next steps with timeline

## Expected NOT to Trigger Skill

### Technical Documentation (should use other skills or no skill)

18. "Write API documentation for our REST endpoints"
    - **Expected**: Should trigger api-design skill, not executive-data-storytelling
    - **Reason**: Technical audience, not executive narrative

19. "Create a technical design document for the microservices architecture"
    - **Expected**: No skill or architecture-related skill
    - **Reason**: Technical content, not executive communication

### Operational/Team Communications

20. "Draft an email to my engineering team about sprint planning"
    - **Expected**: No skill trigger
    - **Reason**: Team-level communication, not executive narrative

21. "Write a performance review for a direct report"
    - **Expected**: No skill trigger
    - **Reason**: HR/people process, not executive storytelling

### General Questions

22. "What is data storytelling?"
    - **Expected**: No skill trigger (informational question)
    - **Reason**: Educational query, not creation task

23. "How do I calculate ROI?"
    - **Expected**: No skill trigger
    - **Reason**: Basic information request, not narrative creation

## Edge Cases (Could Trigger or Not)

### Department-Level Presentations (may or may not be executive-focused)

24. "Create a presentation for the sales team kickoff"
    - **Context needed**: If presenting to sales team → probably not executive skill
    - **If presenting to CRO about sales kickoff** → should trigger skill

25. "Draft talking points for the engineering all-hands"
    - **Context needed**: Team communication vs. presenting engineering strategy to ELT
    - **If ELT-focused** → should trigger skill

### Cross-Functional Reviews

26. "Prepare a project status update for stakeholders"
    - **Context needed**: Who are the stakeholders?
    - **If executive stakeholders** → should trigger skill
    - **If project team** → probably not

## Testing Methodology

### For Each Prompt

1. **Submit prompt to Claude**
2. **Observe if skill loads** (look for skill invocation message)
3. **Check if skill content is applied**:
   - Does response reference What/Why/Next framework?
   - Does it mention CEO priorities?
   - Does it apply visual design principles?
   - Does it use depersonalization strategies?
4. **Evaluate appropriateness**: Should the skill have loaded for this prompt?

### Success Criteria

- **Triggers correctly**: 80%+ of "Expected to Trigger" prompts load the skill
- **Doesn't trigger incorrectly**: 90%+ of "Expected NOT to Trigger" don't load skill
- **Useful when loaded**: Skill content meaningfully improves the response
- **Edge cases handled**: Context-dependent prompts make reasonable decisions

### Refinement Based on Results

If skill **doesn't trigger when it should**:

- Add keywords to "When to Use This Skill" section
- Make description more explicit about use cases
- Add more trigger phrases to skill documentation

If skill **triggers when it shouldn't**:

- Make description more specific about audience (executives, not teams)
- Add exclusions to "When to Use This Skill" section
- Refine keywords to be more precise

## Keyword Analysis

### High-Priority Trigger Keywords (should definitely trigger)

- executive presentation
- board memo, board deck, board meeting
- ELT update, ELT presentation
- C-suite, CEO, CFO, CRO, CTO, CIO
- quarterly business review, QBR
- stakeholder communication (executive stakeholders)
- business case (for executives/board)
- investment proposal, funding request
- executive dashboard, executive summary
- leadership briefing, leadership team

### Medium-Priority Trigger Keywords (context-dependent)

- presentation (to whom?)
- stakeholder update (who are stakeholders?)
- performance review (business unit vs. individual?)
- strategic update (audience?)
- project status (executive steering committee?)

### Should NOT Trigger

- API documentation
- technical design
- team communication
- individual performance review
- sprint planning
- code review
- implementation details

## Skill Integration Test

### Test with Related Skills

27. "Create an executive presentation on our API strategy for the board"
    - **Expected**: executive-data-storytelling skill (primary)
    - **Possible**: api-design skill (supporting technical accuracy)
    - **Result**: Should blend both - API technical content in executive narrative format

28. "Draft a board memo on the security breach and our response"
    - **Expected**: executive-data-storytelling skill (primary)
    - **Possible**: security-review skill (supporting technical details)
    - **Result**: Security analysis presented with depersonalization and crisis tone

29. "Build a business case for implementing feature flags to present to the CTO"
    - **Expected**: executive-data-storytelling skill (primary)
    - **Possible**: feature-flags skill (technical details)
    - **Result**: Technical benefits translated to business outcomes with clear ROI

## Real-World Scenarios

### Scenario 1: Missed Target

**Prompt**: "We missed our Q2 revenue target by 18%. Help me prepare a presentation for the board explaining what happened and our plan to get back on track."

**Expected Behavior**:

- Skill loads immediately
- Applies depersonalization strategies heavily
- Uses What/Why/Next structure
- Provides failure communication framework
- Emphasizes root cause analysis with data
- Includes forward-looking recommendations
- Suggests pre-wiring stakeholders

### Scenario 2: Investment Request

**Prompt**: "I need to request $5M for AI infrastructure at the next executive committee meeting. Help me build the business case."

**Expected Behavior**:

- Skill loads immediately
- Aligns with Technology priority (29%)
- Secondary alignment with Growth or Financial
- Uses scenario planning (optimistic/base/pessimistic)
- Includes clear ROI calculation
- Provides decision framework template
- Suggests appendix with detailed financial model

### Scenario 3: Success Story

**Prompt**: "Our retention program reduced turnover from 24% to 11%. I want to present this to the ELT and get approval to expand to other departments."

**Expected Behavior**:

- Skill loads immediately
- Aligns with Workforce priority (25%)
- Shows secondary Financial benefit (cost avoidance)
- Uses "inspired" emotional tone
- Provides expansion recommendation structure
- Includes investment and ROI for expansion
- Clear decision required section

### Scenario 4: Dashboard Design

**Prompt**: "The CEO wants a one-page dashboard showing our growth metrics. Help me design something that tells the story."

**Expected Behavior**:

- Skill loads immediately
- Applies chart selection guide
- Emphasizes Growth priority (59%)
- Focuses on strategic implications, not operational detail
- Uses "one slide, one idea" principle
- Provides "so what" context for each metric
- Visual hierarchy recommendations

## Test Results Template

```markdown
## Test Date: [DATE]

### Prompt: [PROMPT TEXT]

**Expected Outcome**: [Should trigger / Should not trigger / Edge case]

**Actual Outcome**: [Did it trigger? Yes/No]

**Quality Check** (if triggered):
- [ ] What/Why/Next framework applied
- [ ] CEO priority alignment mentioned
- [ ] Visual design principles referenced
- [ ] Depersonalization strategies used (if applicable)
- [ ] Decision framework included
- [ ] Appropriate emotional tone suggested
- [ ] Skill content enhanced response quality

**Issues Found**: [None / List issues]

**Recommendation**: [None / Refine keywords / Update description / etc.]
```

## Continuous Testing

Run these test prompts:

- **Weekly** during initial deployment (first month)
- **Monthly** after stabilization
- **After any skill updates** to ensure changes work as expected
- **When user feedback** suggests skill isn't triggering appropriately

Track results over time to identify:

- Patterns in missed triggers
- False positive triggers
- Keywords that work best
- User feedback on skill utility

---

_These test prompts ensure the skill triggers appropriately and provides value when it does. Refine based on real-world usage patterns._
