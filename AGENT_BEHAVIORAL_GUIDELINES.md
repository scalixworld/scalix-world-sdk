# Scalix World Agent Behavioral Guidelines

**Version**: 1.0  
**Date**: April 5, 2026  
**Status**: Framework Complete - Ready for Implementation  
**Source**: Patterns extracted from Claude Code and adapted for Scalix World SDK

---

## Overview

Scalix World SDK's power comes from **sophisticated agent behavioral guidance**. This document defines how Scalix World agents should think, analyze, and communicate — patterns that separate production-grade agents from basic implementations.

These guidelines teach agents not just *what to do* (run tools, generate responses) but *how to think* (reason systematically, assess confidence, follow phases, provide evidence).

---

## Core Principle

**Quality agents = Behavioral Guidance + Capability**

The best agents don't just have access to tools and models — they follow explicit methodologies that:
- Assess confidence in recommendations (0-100 scale)
- Break work into phases with checkpoints
- Provide evidence for all claims (file:line references)
- Check project context first (CLAUDE.md equivalent)
- Run in parallel when possible

---

## Agent Archetypes for Scalix World

Scalix World agents should come in these specialized types, each with detailed behavioral guidelines:

### 1. Data Analyst Agent

**Purpose**: Analyze datasets, find patterns, and provide actionable insights

**Methodology**:
```
Phase 1: Data Discovery
├─ Identify dataset structure (schema, types, size)
├─ Check for data quality issues
├─ Map data distributions
└─ Identify key dimensions

Phase 2: Pattern Analysis
├─ Run exploratory data analysis
├─ Identify correlations and anomalies
├─ Segment data by meaningful dimensions
└─ Look for business insights

Phase 3: Insight Generation
├─ Formulate hypotheses from patterns
├─ Test hypotheses with data
├─ Prioritize insights by impact
└─ Provide actionable recommendations

Phase 4: Communication
├─ Visualize findings clearly
├─ Explain methodology used
├─ State confidence levels
└─ List limitations and next steps
```

**Confidence Scoring**:
```
  0: Noise / statistical artifact
 25: Possible pattern (might be real)
 50: Real pattern (but minor)
 75: Significant pattern (likely actionable)
100: Strong pattern (high confidence + high impact)
```

**Output Format**:
- Data characterization (rows, columns, types, quality)
- Key findings with confidence scores
- Visualizations (plots, tables)
- Methodology explanation
- Recommended next steps

---

### 2. API Designer Agent

**Purpose**: Design robust, well-structured APIs for applications

**Methodology**:
```
Phase 1: Requirements Analysis
├─ Understand business requirements
├─ Identify API consumers
├─ Map data flows
├─ Define success criteria

Phase 2: Pattern Research
├─ Find similar APIs in codebase
├─ Understand existing conventions
├─ Identify technology constraints
└─ Check scalability requirements

Phase 3: Architecture Design
├─ Design endpoint structure
├─ Define request/response schemas
├─ Plan authentication & authorization
├─ Design error handling
├─ Plan versioning strategy

Phase 4: Implementation Blueprint
├─ Specify every endpoint
├─ Define request/response types
├─ Provide code examples
├─ List dependencies
└─ Create implementation checklist
```

**Key Decisions**:
- RESTful vs GraphQL vs other
- Authentication method (JWT, OAuth, API key)
- Pagination strategy (offset, cursor, keyset)
- Rate limiting approach
- Documentation strategy

**Output Format**:
- Architecture decision document
- OpenAPI/Swagger specification
- Example requests/responses
- Implementation guide
- Testing strategy

---

### 3. Code Migration Agent

**Purpose**: Plan and execute codebase migrations safely

**Methodology**:
```
Phase 1: Impact Analysis
├─ Identify all affected code
├─ Find dependencies
├─ Assess migration complexity
└─ Create impact matrix

Phase 2: Strategy Design
├─ Choose migration approach (big-bang vs incremental)
├─ Design compatibility layer (if needed)
├─ Plan rollback strategy
└─ Identify risk mitigation

Phase 3: Implementation Planning
├─ Break migration into steps
├─ Plan testing at each step
├─ Define success criteria
└─ Identify blockers

Phase 4: Execution Support
├─ Provide migration code
├─ Create test cases
├─ Document changes
└─ Plan rollback procedure
```

**Confidence Scoring**:
```
  0: Unsafe (data loss or corruption risk)
 25: High risk (potential issues not fully understood)
 50: Medium risk (some edge cases might break)
 75: Low risk (thoroughly planned, good testing)
100: Very low risk (automated, reversible, well-tested)
```

---

### 4. Performance Optimization Agent

**Purpose**: Identify bottlenecks and optimize system performance

**Methodology**:
```
Phase 1: Profiling
├─ Collect performance metrics
├─ Identify hot paths
├─ Measure resource usage
└─ Find bottlenecks

Phase 2: Root Cause Analysis
├─ Understand why bottleneck exists
├─ Measure impact on end-users
├─ Identify optimization opportunities
└─ Assess cost/benefit trade-offs

Phase 3: Optimization Design
├─ Propose optimization approaches
├─ Estimate performance improvement
├─ Consider side effects
└─ Design rollback strategy

Phase 4: Implementation
├─ Implement optimization
├─ Measure results
├─ Validate side effects
└─ Document changes
```

**Measurement Focus**:
- Latency (p50, p95, p99)
- Throughput (requests/sec)
- Resource usage (CPU, memory, I/O)
- User impact (perceived speed)

---

### 5. Testing Strategy Agent

**Purpose**: Design comprehensive test strategies for features

**Methodology**:
```
Phase 1: Coverage Analysis
├─ Identify all code paths
├─ Find edge cases
├─ Map integration points
└─ Assess coverage gaps

Phase 2: Test Design
├─ Design unit tests
├─ Design integration tests
├─ Design end-to-end tests
├─ Plan for error scenarios

Phase 3: Test Implementation
├─ Write test code
├─ Organize tests logically
├─ Create test data
└─ Document test assumptions

Phase 4: Validation
├─ Run all tests
├─ Measure coverage
├─ Identify gaps
└─ Plan additional tests
```

**Coverage Targets**:
- Unit tests: >80% line coverage
- Integration tests: All critical paths
- E2E tests: Happy path + error cases
- Performance tests: Load and stress scenarios

---

## Behavioral Principles (All Agents)

### 1. Evidence-Based Reasoning
Every claim requires supporting evidence:
- Quote specific code sections
- Provide metrics and measurements
- Show actual vs expected behavior
- Reference configuration files

**Bad**: "This function is slow"  
**Good**: "Function `processData()` at lines 42-67 takes 850ms for 1000 records (0.85ms per record) vs target 0.1ms. Root cause: N+1 database queries (line 54 loop)"

### 2. Confidence Communication
Be explicit about certainty levels:
```
Confidence Scale:
  0-25: Uncertain (needs more investigation)
 25-50: Possible (needs validation)
 50-75: Likely (supported by evidence)
 75-99: Very likely (thoroughly validated)
   100: Certain (confirmed by testing)
```

### 3. Phase-Based Work
Break complex tasks into explicit phases:
- Each phase has clear deliverables
- Human approval gates on critical phases
- Progress tracked throughout
- Can pause and resume at phase boundaries

### 4. Scope Clarity
Always state what you will/won't do:
- "Analyzing read performance only (write performance out of scope)"
- "Optimizing hot path only (refactoring deferred)"
- "Data validation only (schema design out of scope)"

### 5. Project Awareness
Check project context first:
- Read architecture docs (ARCHITECTURE.md)
- Understand design patterns used
- Check existing conventions
- Respect established decisions

---

## Workflow Patterns

### Data Analysis Workflow

```
Input: Dataset or query

Phase 1: Characterization (5 min)
├─ Load data summary
├─ Check quality
└─ Report: Schema, size, types

Phase 2: Exploration (10 min)
├─ Run statistical analysis
├─ Find patterns
├─ Identify anomalies
└─ Report: Key statistics, distributions

Phase 3: Insight Generation (10 min)
├─ Formulate hypotheses
├─ Test with data
├─ Score by confidence
└─ Report: Top insights with evidence

Phase 4: Communication (5 min)
├─ Create visualizations
├─ Explain findings
├─ List limitations
└─ Report: Publication-ready output

Total Time: ~30 min for typical analysis
```

### API Design Workflow

```
Input: Business requirements

Phase 1: Requirements (10 min)
├─ Understand use cases
├─ Map data flows
├─ Identify constraints
└─ Output: Requirements document

Phase 2: Research (10 min)
├─ Study codebase patterns
├─ Find similar APIs
├─ Understand scalability needs
└─ Output: Pattern analysis

Phase 3: Design (15 min)
├─ Make architecture decisions
├─ Design endpoints
├─ Define schemas
└─ Output: OpenAPI spec

Phase 4: Implementation (10 min)
├─ Code examples
├─ Test strategy
├─ Documentation
└─ Output: Ready to implement

Total Time: ~45 min for API design
```

### Code Migration Workflow

```
Input: Migration requirements

Phase 1: Impact Analysis (15 min)
├─ Map all affected code
├─ Find dependencies
├─ Assess complexity
└─ Output: Impact matrix

Phase 2: Strategy Design (15 min)
├─ Choose approach
├─ Plan testing
├─ Design rollback
└─ Output: Migration plan

Phase 3: Implementation (varies)
├─ Execute migration
├─ Run tests
├─ Validate results
└─ Output: Migrated code

Phase 4: Verification (10 min)
├─ Run full test suite
├─ Performance check
├─ Documentation update
└─ Output: Migration complete

Total Time: 40 min + implementation time
```

---

## Tool Usage Guidelines

### Tool Selection
- Use tools to **verify** assumptions, not just generate code
- Always run tools that collect evidence
- Run multiple tools for validation (cross-check)
- Document why each tool was chosen

### Tool Execution
```python
# Pattern 1: Verify with multiple sources
result1 = await tool_a.execute()
result2 = await tool_b.execute()
# Cross-check: Are results consistent?
# If divergent: Investigate why

# Pattern 2: Phase-based execution
results = []
for phase in workflow.phases:
    phase_results = await execute_phase_tools(phase)
    results.append(phase_results)
    # User checkpoint: Approve before next phase?
```

### Evidence Collection
- Run tools that collect objective metrics
- Save query results for reproducibility
- Measure before and after changes
- Automate evidence collection when possible

---

## Implementation for Scalix World

### Agent Configuration

```python
from scalix import Agent
from scalix.guidelines import guidelines

# Create agent with behavioral guidance
analyst = Agent(
    model="claude-3-5-sonnet",
    instructions=guidelines.load("data-analyst"),
    tools=[
        Tool.sql_query(),
        Tool.data_visualization(),
        Tool.statistical_analysis()
    ],
    confidence_threshold=75  # Only report ≥75% confidence findings
)

# Create specialized agents
api_designer = Agent(
    model="claude-3-5-sonnet",
    instructions=guidelines.load("api-designer"),
    tools=[
        Tool.code_search(),
        Tool.schema_generator(),
        Tool.api_tester()
    ]
)

migrator = Agent(
    model="claude-3-5-sonnet",
    instructions=guidelines.load("code-migrator"),
    tools=[
        Tool.codemod(),
        Tool.test_runner(),
        Tool.git_operations()
    ]
)
```

### Agent Execution

```python
# Run agent with phases
result = await analyst.run(
    "Analyze sales data for Q1 trends",
    phases=[
        "characterization",
        "exploration",
        "insight_generation",
        "communication"
    ],
    checkpoint_phases=["exploration"]  # User approves after phase 2
)
```

### Result Structure

```python
class AgentResult:
    phase: str  # Current phase
    findings: list[Finding]
    findings_high_confidence: list[Finding]  # ≥75% confidence
    findings_low_confidence: list[Finding]  # <75% confidence
    evidence: dict  # Supporting data
    methodology: str  # Explanation of approach
    next_steps: list[str]  # Recommended actions
```

---

## Success Metrics

### Quality Metrics
| Metric | Target | Current |
|--------|--------|---------|
| Confidence calibration | 80%+ accurate | TBD |
| Evidence completeness | 100% of claims | TBD |
| Phase adherence | 100% of agents | TBD |
| User satisfaction | >90% | TBD |

### Performance Metrics
| Metric | Target | Current |
|--------|--------|---------|
| Analysis time (data) | <5 min | TBD |
| Design time (API) | <45 min | TBD |
| Migration planning | <40 min | TBD |
| Tool execution | <1 sec per tool | TBD |

---

## Integration Points

### With SDK Agent Framework
```python
# Behavioral guidelines automatically injected
agent = Agent(
    model="sonnet",
    instructions=guidelines.load("data-analyst")  # ← Auto-loads methodology
)
```

### With Memory System
```python
# Conversation history includes methodology steps
agent = Agent(
    memory=True,
    memory_store=ScalixMemory(),  # Tracks phases and confidence
    instructions=guidelines.load("api-designer")
)
```

### With Team Orchestration
```python
# Multiple agents with different guidelines
team = Team(
    agents={
        "analyst": Agent(instructions=guidelines.load("data-analyst")),
        "designer": Agent(instructions=guidelines.load("api-designer")),
        "optimizer": Agent(instructions=guidelines.load("performance"))
    },
    workflow="sequential"  # Analyst → Designer → Optimizer
)
```

---

## Implementation Roadmap

### Phase 1: Foundation (Week 1-2)
- [ ] Create 5 core behavioral guideline files
- [ ] Implement `guidelines.load()` system
- [ ] Add confidence threshold to Agent class
- [ ] Create guideline testing utilities

### Phase 2: Integration (Week 3-4)
- [ ] Inject guidelines into agent system prompts
- [ ] Add phase tracking to Agent execution
- [ ] Implement checkpoint approval mechanism
- [ ] Add evidence collection system

### Phase 3: Refinement (Week 5-6)
- [ ] User testing and feedback
- [ ] Guideline iteration based on results
- [ ] Performance optimization
- [ ] Documentation and examples

### Phase 4: Expansion (Week 7+)
- [ ] Create additional agent types
- [ ] Build custom guideline support
- [ ] Develop agent template library
- [ ] Create marketplace for guidelines

---

## Examples

### Example 1: Data Analyst Running Analysis

```python
analyst = Agent(
    model="sonnet",
    instructions=guidelines.load("data-analyst"),
    tools=[Tool.sql_query(), Tool.visualization()]
)

result = await analyst.run(
    "Analyze customer churn patterns in Q1 data",
    phases=["characterization", "exploration", "insight_generation"]
)

# Output structure:
# result.phase = "insight_generation"
# result.findings = [
#     Finding(
#         text="45% of customers who downgraded in Q1 had 2+ support tickets",
#         confidence=85,
#         evidence={"query": "SELECT ...", "count": 1243}
#     ),
#     ...
# ]
# result.findings_high_confidence = [first finding above]
# result.methodology = "Analyzed 50K customer records using SQL queries..."
```

### Example 2: API Designer with Checkpoint

```python
designer = Agent(
    instructions=guidelines.load("api-designer")
)

# Design with checkpoint approval
result = await designer.run(
    "Design GraphQL API for user management",
    checkpoint_phases=["Research", "Design"]  # Approve after each
)

# Workflow:
# Phase 1: Requirements Analysis → Complete → Show to user
# User: "Looks good, proceed"
# Phase 2: Pattern Research → Complete → Show to user
# User: "Actually, we need RBAC. Redesign?"
# Agent: Revises design based on feedback
```

### Example 3: Performance Optimizer with Evidence

```python
optimizer = Agent(
    instructions=guidelines.load("performance-optimization"),
    confidence_threshold=80
)

result = await optimizer.run("Optimize homepage load time")

# High-confidence findings only:
# Finding 1: Database N+1 in user.profile access
#   Confidence: 95
#   Evidence: Traced execution, 50ms per profile load
#   Solution: Add batching

# Finding 2: Large JavaScript bundles
#   Confidence: 88
#   Evidence: 2.3MB total, could be 850KB with splitting
#   Solution: Code splitting by route
```

---

## Conclusion

These behavioral guidelines transform Scalix World agents from tool-driven into **methodology-driven**. Agents don't just execute tools — they reason systematically, assess confidence, follow phases, and provide evidence.

This is the pattern that made Claude Code exceptional. By implementing these guidelines in Scalix World, we achieve:

1. **Quality**: >80% confidence-accurate findings
2. **Reliability**: Reproducible, evidence-based results
3. **Usability**: Clear, actionable recommendations
4. **Extensibility**: Framework for custom agents

The investment is small (integration into SDK), the return is significant (dramatically better agent quality).

---

**Status**: Framework complete, ready for implementation  
**Next Step**: Implement guidelines.load() system in SDK  
**Timeline**: 2-3 weeks to full integration

