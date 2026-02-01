# Communication Styles Skill - Test Prompts

This document contains test prompts to verify the skill triggers correctly.

## Prompts That SHOULD Trigger This Skill

### Executive Communication

1. "I need to email the CFO requesting budget approval. She's very results-focused and doesn't like long emails."

2. "Preparing a presentation for the VP of Engineering next week. He's extremely detail-oriented and asks lots of technical questions."

3. "How should I approach the CEO about this project? She's very relationship-focused and wants to make sure the whole team is on board."

### Stakeholder Engagement

4. "I'm meeting with a business partner tomorrow who always starts meetings with stories and gets really excited about ideas. How should I engage with them?"

5. "There's a key stakeholder who keeps saying 'let me think about it' and never makes a decision. What communication approach should I use?"

6. "I need to influence this executive to approve my proposal. What's the best way to present this?"

### Conflict Resolution

7. "Two team members are clashing - one wants to move fast and make decisions, the other needs more time to get team consensus. How do I resolve this?"

8. "Having trouble communicating with my manager. Every meeting feels tense and we're not connecting. What should I do?"

9. "This stakeholder keeps attacking my ideas aggressively. How should I respond?"

### Presentation Preparation

10. "Presenting to the board next week. The audience includes technical leaders, business executives, and HR. How should I structure this?"

11. "Need to prepare a quarterly review presentation for senior leadership with mixed communication preferences. What's the best approach?"

12. "How do I present complex technical information to non-technical executives?"

### Team Communication

13. "How can I improve collaboration with cross-functional partners who have very different communication styles?"

14. "My team has diverse communication preferences. How do I run effective meetings?"

15. "Need to write a proposal that will go to multiple stakeholders. How do I adapt my writing style?"

### Specific Style Keywords

16. "How do I communicate with someone who is very relationship-oriented and seeks consensus?"

17. "This person is extremely task-focused and just wants results. What's my strategy?"

18. "They always ask 'why' and need to understand the people impact. How should I engage?"

19. "This executive just wants the bottom line and makes fast decisions. How do I present to them?"

20. "I'm dealing with someone who is very analytical and wants all the data before deciding."

## Prompts That SHOULD NOT Trigger This Skill

### General Communication (No Style Context)

1. "How do I write a good email?"
   - Expected: General writing advice, not style-specific

2. "What should I say in this meeting?"
   - Expected: General meeting advice without style context

3. "I need to improve my presentation skills"
   - Expected: General presentation tips, not style-based

### Technical Questions

4. "How do I configure this API?"
   - Expected: Technical API guidance, not communication

5. "What's the best way to structure this code?"
   - Expected: Code architecture advice

6. "Debug this error message"
   - Expected: Technical debugging

### Different Skill Domains

7. "How do I create a feature flag?"
   - Expected: feature-flags skill

8. "Review this API design"
   - Expected: api-design skill

9. "How do I secure this endpoint?"
   - Expected: security-review skill

10. "Help me tell a story with this data"
    - Expected: executive-data-storytelling skill (unless paired with stakeholder style context)

## Edge Cases (May or May Not Trigger)

### Borderline Cases

1. "How do I negotiate this contract?"
   - Context needed: If focused on adapting to negotiation partner's style → SHOULD trigger
   - If focused on contract terms → should NOT trigger

2. "I need to write a persuasive proposal"
   - Context needed: If audience style is mentioned → SHOULD trigger
   - If generic persuasion → may not trigger

3. "Help me prepare for this job interview"
   - Context needed: If adapting to interviewer's style → SHOULD trigger
   - If general interview prep → should NOT trigger

4. "This relationship isn't working"
   - Context needed: Professional relationship with communication friction → SHOULD trigger
   - Personal relationship → should NOT trigger

## Test Results Format

When testing, document results as:

```
PROMPT: [exact prompt tested]
EXPECTED: Should trigger / Should not trigger
ACTUAL: Did trigger / Did not trigger
STATUS: ✅ Pass / ❌ Fail
NOTES: [any relevant observations]
```

## Integration Test: Combined Skills

These prompts should trigger BOTH communication-styles AND another skill:

1. "I need to present this data story to executives with different communication preferences"
   - Expected: communication-styles + executive-data-storytelling

2. "How do I explain this security vulnerability to different stakeholders?"
   - Expected: communication-styles + security-review

3. "I need to roll out this feature flag and communicate differently to technical vs. business leaders"
   - Expected: communication-styles + feature-flags

4. "How do I present this API design to stakeholders who have very different communication styles?"
   - Expected: communication-styles + api-design

## Success Criteria

The skill is working correctly if:

1. Triggers on 90%+ of the "SHOULD trigger" prompts
2. Does NOT trigger on 90%+ of the "SHOULD NOT trigger" prompts
3. Can identify the four social styles (Amiable, Expressive, Analytic, Driver)
4. Provides style-specific engagement strategies
5. Offers practical templates and examples
6. Includes power words and tension factors
7. Addresses the 20-second diagnostic method
8. Covers multi-style presentation structures

## Keywords That Should Trigger Skill

Primary Keywords:
- communication style
- stakeholder engagement
- executive communication
- social styles
- flexing communication
- adapt communication
- communication preferences

Style-Specific Keywords:
- relationship-focused
- task-focused
- consensus
- results-oriented
- data-driven
- story-driven
- analytical
- decisive

Context Keywords:
- present to executives
- communicate with stakeholder
- influence decision
- build rapport
- resolve conflict
- engagement strategy
- communication approach
- writing style
- presentation structure

## Testing the Diagnostic Script

Test the Python script independently:

```bash
# Self-assessment
python ~/.claude/skills/communication-styles/scripts/style-diagnostic.py --self

# Assess someone else
python ~/.claude/skills/communication-styles/scripts/style-diagnostic.py --other

# Stakeholder analysis
python ~/.claude/skills/communication-styles/scripts/style-diagnostic.py --stakeholder-analysis

# Interactive menu
python ~/.claude/skills/communication-styles/scripts/style-diagnostic.py
```

Expected: Script runs without errors, provides accurate style assessments, generates useful recommendations.
