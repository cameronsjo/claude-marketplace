# Prompt Engineering Skill - Test Prompts

Test prompts to verify this skill triggers correctly.

## Should Trigger Skill ✅

### Test 1: Prompt Optimization
```
This prompt gives inconsistent results. How can I improve it?
```
**Expected:** Skill loads, provides optimization techniques

### Test 2: Few-Shot Learning
```
Create a few-shot prompt for entity extraction from text
```
**Expected:** Skill loads, provides few-shot template

### Test 3: Chain-of-Thought
```
How do I use chain-of-thought reasoning for complex math problems?
```
**Expected:** Skill loads, provides CoT patterns

### Test 4: LLM Prompting
```
Design a prompt for Claude to analyze code for security issues
```
**Expected:** Skill loads, provides prompt design guidance

### Test 5: Prompt Testing
```
How should I A/B test different prompt variations?
```
**Expected:** Skill loads, provides testing methodology

### Test 6: System Prompt
```
Create a system prompt for an AI customer service agent
```
**Expected:** Skill loads, provides role-based prompting patterns

### Test 7: Output Format
```
My LLM outputs aren't consistently formatted. How do I fix this?
```
**Expected:** Skill loads, provides format specification techniques

### Test 8: GPT vs Claude
```
What are the prompt differences between GPT-4 and Claude?
```
**Expected:** Skill loads, provides model-specific guidance

### Test 9: Prompt Injection
```
How do I prevent prompt injection attacks in my AI application?
```
**Expected:** Skill loads, provides security patterns

## Should NOT Trigger Skill ❌

### Test 10: General AI Development
```
How do I build a RAG system with vector search?
```
**Expected:** ai-integration skill (if exists), NOT prompt-engineering

### Test 11: MCP Development
```
Create an MCP server with tool definitions
```
**Expected:** mcp-development skill, NOT prompt-engineering

### Test 12: API Design
```
Design a REST API for user authentication
```
**Expected:** api-design skill, NOT prompt-engineering

## Edge Cases

### Test 13: AI Feature with Prompting
```
Build an AI feature that summarizes documents. What prompt should I use?
```
**Expected:** Should trigger skill (prompt design is central)

### Test 14: Agent Orchestration
```
Create prompts for a multi-agent system with specialized roles
```
**Expected:** Should trigger skill (prompt design for agents)

### Test 15: LLM Engineering
```
Optimize my LLM prompts for cost and performance
```
**Expected:** Should trigger skill (LLM + prompt keywords)
