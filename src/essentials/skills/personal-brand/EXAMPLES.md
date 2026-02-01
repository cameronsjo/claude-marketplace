# Executive Presence Skill - Usage Examples

This document provides real-world examples of how to use the Executive Presence Skill with Claude.

## Example 1: Career Transition from Technical to Business Leadership

### User Prompt

```
I'm a CIO who's been getting feedback that I'm "too in the weeds" and "not strategic enough."
I have deep technical expertise but want to be seen as a business partner, not just an IT leader.
How do I build executive presence for a more business-oriented role?
```

### How Claude Uses This Skill

1. **Activates skill** based on keywords: "CIO," "executive presence," "feedback," "strategic"

2. **Guides discovery process:**
   - Uses brand-observation-journal.md template to track current perceptions
   - Provides brand-discovery-questions.md for structured feedback conversations
   - Helps identify current brand: "Technical expert, detail-oriented, operationally focused"

3. **Analyzes the challenge:**
   - References "Challenge 1: I'm Seen as Too Technical" section in SKILL.md
   - Identifies this as a recalibration (not reinvention) scenario

4. **Establishes zone of distinction:**
   - Uses zone-of-distinction-venn.md to map:
     - Market Need: Business-IT partnership, digital transformation
     - Your Values: Excellence, collaboration, innovation
     - Your Market Value: Technical expertise, stakeholder management, problem-solving
   - Zone of Distinction: "Technology-enabled business transformation leader"

5. **Creates aspirational brand:**
   - Suggests transformation: "Technical expert" → "Business-technology partner"
   - Runs brand-keywords-generator.py for CIO role suggestions
   - Validates with zone-validator.py

6. **Develops recalibration strategy:**
   - Shift language from technical to business outcomes
   - Delegate technical deep-dives to develop team
   - Increase business acumen visibility
   - Reframe expertise: "Digital capability strategist"

7. **Creates anti-brand list:**
   - Stop: Personally troubleshooting technical issues
   - Delegate: Attending every operational status meeting
   - Minimize: Technical architecture deep-dives (except strategic)

8. **Defines brand promise:**
   - "Digital transformation catalyst" or "Business-technology partner"

---

## Example 2: Promotion Readiness Assessment

### User Prompt

```
I want to be promoted to VP level but I'm not sure if I have the executive presence.
How do I know if I'm ready and what I need to work on?
```

### How Claude Uses This Skill

1. **Starts with self-awareness diagnostic:**
   - Uses self-awareness-diagnostic.md (30 questions, 150 points)
   - Helps identify perception gaps and blind spots

2. **Conducts brand discovery:**
   - Guides through brand-observation-journal.md process
   - Facilitates brand-discovery-conversations.md with:
     - Direct reports (how you lead)
     - Peers (how you collaborate)
     - Senior stakeholders (how you influence up)

3. **Evaluates current brand vs. VP expectations:**
   - Uses brand-alignment-check.md assessment
   - Compares current brand against VP-level requirements
   - Identifies gaps in executive presence

4. **Creates development plan:**
   - Uses market-needs-analysis.md to understand what VPs are expected to deliver
   - Uses personal-values-inventory.md to ensure authenticity
   - Uses market-value-inventory.md to document proven capabilities

5. **Builds VP-level brand promise:**
   - Example: "Strategic business outcome architect"
   - Validates with zone-validator.py (target score: 8-10)

6. **Defines proof points:**
   - Helps identify track record examples that demonstrate VP-level impact
   - Creates evidence portfolio for promotion discussion

---

## Example 3: Overcoming Inherited Negative Brand

### User Prompt

```
I just took over as head of IT after an unpopular predecessor who was seen as
"the department of no" and "cost center mentality." How do I build a different
executive presence and change perceptions?
```

### How Claude Uses This Skill

1. **Identifies challenge type:**
   - References "Challenge 5: I'm Inheriting a Negative Brand" section

2. **Develops contrast strategy:**
   - Explicitly acknowledge predecessor's brand
   - Identify opposite behaviors to demonstrate visibly
   - Create psychological distance from old brand

3. **Establishes new zone of distinction:**
   - Market Need: Business enablement, innovation, partnership
   - Your Values: Collaboration, yes-and mentality, value creation
   - Your Market Value: Technical expertise, relationship building, strategic thinking
   - Zone: "Business-enabling technology partner"

4. **Creates anti-brand list:**
   - Inherited perceptions to counter:
     - "Department of no"
     - "Cost center mentality"
     - "Order takers"
     - "Risk-averse"

5. **Builds aspirational brand:**
   - "Business enablement champion"
   - "Value-creation partner"
   - "Yes-and innovator"

6. **Develops quick wins:**
   - Reset relationships with key stakeholders
   - Demonstrate contrasting behaviors in first 90 days
   - Tell stories that illustrate new brand
   - Create new norms and rituals

---

## Example 4: Building Influence Without Positional Authority

### User Prompt

```
I'm an individual contributor who needs to influence senior stakeholders on a
cross-functional initiative, but I don't have positional authority. How do I
build executive presence and credibility?
```

### How Claude Uses This Skill

1. **Focuses on Impact phase:**
   - References Executive Presence Wheel: Image → Impressions → Impact
   - Emphasizes that presence without title requires stronger Impact

2. **Develops influence-based brand:**
   - Zone of distinction focused on value creation and expertise
   - Example: "Cross-functional catalyst" or "Initiative accelerator"

3. **Uses influence-audit.md assessment:**
   - Evaluates current influence patterns
   - Identifies where influence works and where it doesn't
   - Maps stakeholder relationships

4. **Builds credibility strategy:**
   - Create visible proof points of expertise
   - Develop strategic relationships before needing them
   - Communicate in business value terms
   - Demonstrate consistent follow-through

5. **Develops brand promise:**
   - "Trusted advisor" or "Results multiplier"
   - Emphasizes expertise and reliability over title

---

## Example 5: Using the Scripts

### Script Usage Example 1: Validate Zone of Distinction

```bash
# Interactive validation session
python scripts/zone-validator.py --interactive

# Output example:
> Enter your zone of distinction: Digital transformation catalyst
> Analyzing: Digital transformation catalyst
> Specificity Score: 9 / 10
> ✅ Highly distinctive!
>
> Run the five validation tests? (y/n): y
>
> 1. DISTINCTION TEST
>    Could this zone of distinction apply to any of your peers,
>    or is it uniquely yours?
>    Answer (unique/peers/uncertain): unique
>
> [continues through all 5 tests]
>
> Generate full markdown report? (y/n): y
> ✅ Report written to zone-validation-report.md
```

### Script Usage Example 2: Generate Brand Keywords

```bash
# Get CIO-specific brand suggestions
python scripts/brand-keywords-generator.py --role cio

# Output includes:
# - 8 distinctive approaches (Digital transformation, Business-technology partnership, etc.)
# - 8 value descriptors (catalyst, enabler, co-creator, etc.)
# - 5 example brand promises
# - 40+ additional combinations
```

### Script Usage Example 3: Transform Generic Language

```bash
# Test and improve generic brand language
python scripts/brand-keywords-generator.py \
  --input "strategic thinker" \
  --test

# Output includes:
# - Distinctiveness score (1-5)
# - Suggested alternatives:
#   - "business outcome architect"
#   - "future-state planner"
#   - "strategic roadmap curator"
# - Tips for making language more distinctive
```

### Script Usage Example 4: Analyze Feedback

```bash
# Extract themes from performance reviews
python scripts/analyze-feedback.py \
  --file performance-review-2024.txt \
  --output feedback-analysis.md

# Generates report with:
# - Most frequent themes
# - Positive vs. negative sentiment
# - Keywords and phrases
# - Recommendations for brand positioning
```

---

## Example 6: Using Worksheets and Templates

### Worksheet Flow for Complete Brand Development

1. **Start with observation:**
   - Use `resources/templates/brand-observation-journal.md`
   - Track for 2-4 weeks: words people use, why they seek you, meetings you're invited to

2. **Conduct discovery conversations:**
   - Use `resources/templates/brand-discovery-questions.md`
   - Have 5-8 conversations with diverse perspectives
   - Document findings in `resources/worksheets/brand-discovery-synthesis.md`

3. **Distill current brand:**
   - Use `resources/worksheets/current-brand-statement.md`
   - Summarize in 2-3 words: "Technical expert, detail-oriented, operationally focused"

4. **Analyze zone of distinction:**
   - Complete `resources/worksheets/market-needs-analysis.md`
   - Complete `resources/worksheets/personal-values-inventory.md`
   - Complete `resources/worksheets/market-value-inventory.md`
   - Use `resources/templates/zone-of-distinction-venn.md` to find intersection

5. **Create brand lists:**
   - Use `resources/templates/aspirational-brand-list.md`
   - Use `resources/templates/anti-brand-list.md`

6. **Develop brand promise:**
   - Use `resources/worksheets/brand-promise-development.md`
   - Validate with zone-validator.py script
   - Document in `resources/templates/brand-promise-statement.md`

7. **Assess progress:**
   - Use `resources/assessments/self-awareness-diagnostic.md` (baseline)
   - Use `resources/assessments/brand-alignment-check.md` (quarterly)
   - Use `resources/assessments/influence-audit.md` (bi-annually)

---

## Example 7: Common Transformations by Role

### For CIOs

**Current Brand (Generic):**

- "IT leader"
- "Technology executive"
- "Reliable IT partner"

**Aspirational Brand (Distinctive):**

- "Digital transformation catalyst"
- "Business-technology co-creator"
- "Technical debt eliminator"
- "Platform thinking evangelist"

**Zone of Distinction Example:**

- Market Need: Business-IT partnership, digital transformation
- Your Values: Innovation, collaboration, operational excellence
- Your Market Value: Technical expertise, stakeholder management, strategic planning
- **Zone:** "Technology-enabled business transformation leader"

**Brand Promise:** "Digital transformation catalyst"

### For Product Leaders

**Current Brand (Generic):**

- "Product manager"
- "Customer-focused"
- "Data-driven decision maker"

**Aspirational Brand (Distinctive):**

- "Customer journey optimizer"
- "Experimentation evangelist"
- "Product-market fit architect"
- "Outcome obsession champion"

**Zone of Distinction Example:**

- Market Need: Customer experience, product-market fit, rapid iteration
- Your Values: User empathy, continuous improvement, data-informed decisions
- Your Market Value: User research, experiment design, roadmap planning
- **Zone:** "Customer-centric experimentation leader"

**Brand Promise:** "Customer journey optimizer"

### For Engineering Leaders

**Current Brand (Generic):**

- "Engineering manager"
- "Technical leader"
- "Delivery-focused"

**Aspirational Brand (Distinctive):**

- "Developer experience champion"
- "Engineering velocity multiplier"
- "Technical mentorship advocate"
- "Architecture clarity driver"

**Zone of Distinction Example:**

- Market Need: Developer productivity, engineering quality, team growth
- Your Values: Technical excellence, people development, continuous improvement
- Your Market Value: Architecture design, team building, delivery optimization
- **Zone:** "Engineering excellence and growth leader"

**Brand Promise:** "Developer experience champion"

---

## Example 8: Timeline for Brand Development

### Weeks 1-2: Discovery

- Start brand observation journal (daily)
- Review past performance reviews
- Complete self-awareness-diagnostic.md

### Weeks 3-4: Conversations

- Schedule 5-8 brand discovery conversations
- Use brand-discovery-questions.md template
- Document findings in brand-discovery-synthesis.md

### Week 5: Analysis

- Complete zone of distinction worksheets
- Distill current brand statement
- Identify aspirational brand words

### Week 6: Creation

- Create aspirational brand list
- Create anti-brand list
- Develop brand promise statement
- Validate with zone-validator.py

### Weeks 7-8: Validation

- Test brand promise with trusted advisors
- Refine based on feedback
- Run brand-keywords-generator.py for alternatives

### Months 3-6: Implementation

- Begin behavior changes aligned with new brand
- Track progress with brand-alignment-check.md
- Update professional profiles with brand promise

### Months 6-18: Recalibration

- Monitor feedback and perception shifts
- Adjust anti-brand list (delegate/eliminate activities)
- Retake self-awareness-diagnostic.md
- Conduct follow-up brand discovery conversations

---

## Tips for Using This Skill Effectively

### 1. Start with Honesty

Be brutally honest in self-assessments. Remember: 95% of people overestimate their self-awareness.

### 2. Gather Real Feedback

Don't skip the brand discovery conversations. Your perception of yourself is not reality.

### 3. Use the Scripts

The Python scripts provide objective analysis:

- zone-validator.py prevents generic brand promises
- brand-keywords-generator.py sparks distinctive language
- analyze-feedback.py finds patterns you might miss

### 4. Focus on Distinction

"Dependable technologist" is forgettable. "Technical debt eliminator" is memorable.

### 5. Align with Market Needs

Your brand must serve your market's needs, not just your preferences.

### 6. Be Patient

Brand perception shifts take 6-18 months of consistent behavior change.

### 7. Recalibrate, Don't Reinvent

Most leaders need adjustment, not transformation. Work with who you are.

### 8. Maintain Authenticity

Unsustainable brands collapse under pressure. Align with your values.

### 9. Create the Anti-Brand

What you stop doing is as important as what you start doing.

### 10. Measure Impact

Executive presence is proven through what people do (Impact), not just what they think (Image) or feel (Impressions).

---

## When Claude Should NOT Use This Skill

This skill is not appropriate for:

- **Resume writing** (use general writing skills)
- **Interview preparation** (unless focused on executive presence specifically)
- **Performance review writing** (unless framing around brand positioning)
- **General career advice** (unless focused on presence and influence)
- **LinkedIn optimization** (unless incorporating brand promise)

Use this skill specifically for **executive presence development, personal brand creation, and leadership positioning**.

---

## Related Resources

### Inside Claude Skills

- **executive-data-storytelling** - How to communicate data with executive presence
- **communication-styles** - Understanding how to adapt communication for influence
- **prompt-engineering** - Developing effective messaging

### External Resources

- Gartner Research: "Develop an Executive Presence by Building an Intentional Personal Brand" (G00754773)
- Books: "Presence" by Amy Cuddy, "The Brand Called You" by Tom Peters
- Assessments: MBTI, DiSC, StrengthsFinder, 360-degree feedback tools

---

**Last Updated:** 2025-11-10
**Skill Version:** 1.0.0
