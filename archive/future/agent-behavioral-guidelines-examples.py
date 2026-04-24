"""
Scalix World Agent Behavioral Guidelines - Implementation Examples

This file demonstrates how to use behavioral guidelines to create
sophisticated agents that think systematically and provide high-quality results.
"""

from scalix import Agent, Tool, Team
from scalix.guidelines import guidelines
import json
from typing import Optional


# ============================================================================
# Example 1: Data Analyst with Confidence-Based Filtering
# ============================================================================

async def example_data_analyst():
    """
    Create a data analyst agent that:
    - Phases analysis into discovery, exploration, insights
    - Only reports findings with ≥75% confidence
    - Provides evidence for all claims
    """

    # Create agent with analytical methodology
    analyst = Agent(
        model="scalix-advanced",
        instructions=guidelines.load("data-analyst"),
        tools=[
            Tool.sql_query(database="analytics"),
            Tool.data_visualization(),
            Tool.statistical_analysis()
        ],
        confidence_threshold=75,  # Only report high-confidence findings
        memory=True,  # Remember previous analyses
    )

    # Run analysis with explicit phases
    result = await analyst.run(
        prompt="Which products have declining revenue trends in Q1?",
        phases=[
            "characterization",    # Understand the data
            "exploration",        # Find patterns
            "insight_generation", # Generate insights
            "communication"       # Prepare output
        ]
    )

    # Access results
    print(f"Phase completed: {result.phase}")
    print(f"Total findings: {len(result.findings)}")
    print(f"High-confidence findings: {len(result.findings_high_confidence)}")
    print(f"Analysis time: {result.execution_time:.1f}s")

    # Show high-confidence findings with evidence
    for finding in result.findings_high_confidence:
        print(f"\n✓ {finding.text}")
        print(f"  Confidence: {finding.confidence}%")
        print(f"  Evidence: {json.dumps(finding.evidence, indent=2)}")

    # Show methodology explanation
    print(f"\nMethodology used:\n{result.methodology}")

    return result


# ============================================================================
# Example 2: API Designer with Checkpoints
# ============================================================================

async def example_api_designer_with_checkpoints():
    """
    Design an API with user approval at critical phases.

    This demonstrates:
    - Phase-based workflow with checkpoints
    - Human-in-the-loop decision making
    - Structured output (OpenAPI spec, examples, guides)
    """

    designer = Agent(
        model="scalix-advanced",
        instructions=guidelines.load("api-designer"),
        tools=[
            Tool.code_search(),
            Tool.schema_generator(),
            Tool.openapi_spec_generator()
        ]
    )

    # First phase: Requirements and research
    print("=== Phase 1: Requirements Analysis ===")
    result1 = await designer.run(
        prompt="Design API for product catalog management",
        phases=["requirements", "patterns"]
    )

    # Show findings
    print(f"Key requirements identified:")
    for finding in result1.findings_high_confidence:
        print(f"  - {finding.text}")

    # User checkpoint: Approve requirements?
    print("\nRequirements summary:")
    print(result1.methodology)

    approved = input("\nApprove these requirements? (y/n): ")
    if approved != "y":
        print("Requirements rejected. Please revise.")
        return None

    # Second phase: Design
    print("\n=== Phase 2: Architecture Design ===")
    result2 = await designer.run(
        prompt="Design API for product catalog management (approved requirements)",
        phases=["design", "implementation"]
    )

    # Show design
    print(f"Design decisions:")
    for finding in result2.findings_high_confidence:
        print(f"  - {finding.text}")

    # Extract OpenAPI spec
    openapi_spec = result2.evidence.get("openapi_spec")
    print(f"\nGenerated OpenAPI spec:\n{openapi_spec}")

    # User checkpoint: Approve design?
    approved = input("\nApprove this design? (y/n): ")
    if approved == "y":
        # Save spec
        with open("api_spec.json", "w") as f:
            json.dump(openapi_spec, f, indent=2)
        print("Design approved and saved to api_spec.json")

    return result2


# ============================================================================
# Example 3: Code Migration with Evidence
# ============================================================================

async def example_code_migration():
    """
    Plan a code migration with detailed evidence.

    Demonstrates:
    - Impact analysis with confidence scoring
    - Risk assessment
    - Phased migration planning
    - Rollback strategy
    """

    migrator = Agent(
        model="scalix-advanced",
        instructions=guidelines.load("code-migrator"),
        tools=[
            Tool.codemod(),
            Tool.test_runner(),
            Tool.git_operations(),
            Tool.code_search()
        ],
        confidence_threshold=80  # High bar for migrations
    )

    # Analyze migration impact
    result = await migrator.run(
        prompt="Plan migration from SQLAlchemy 1.x to 2.x",
        phases=[
            "impact-analysis",
            "strategy-design",
            "implementation-planning"
        ]
    )

    # Show findings with evidence
    print("=== Migration Impact Analysis ===\n")

    for finding in result.findings_high_confidence:
        print(f"Finding: {finding.text}")
        print(f"Confidence: {finding.confidence}%")

        evidence = finding.evidence
        print(f"Evidence:")
        print(f"  - Files affected: {evidence.get('files_affected', 0)}")
        print(f"  - Complexity: {evidence.get('complexity', 'unknown')}")
        print(f"  - Estimated effort: {evidence.get('estimated_hours', '?')} hours")
        print(f"  - Risk level: {evidence.get('risk_level', 'unknown')}")
        print()

    # Show implementation steps
    print("Implementation steps:")
    for i, step in enumerate(result.next_steps, 1):
        print(f"  {i}. {step}")

    # Save migration plan
    with open("migration_plan.json", "w") as f:
        json.dump({
            "findings": [f.to_dict() for f in result.findings_high_confidence],
            "methodology": result.methodology,
            "evidence": result.evidence,
            "next_steps": result.next_steps
        }, f, indent=2)

    print("\nMigration plan saved to migration_plan.json")
    return result


# ============================================================================
# Example 4: Performance Optimization with Strict Confidence
# ============================================================================

async def example_performance_optimization():
    """
    Identify and optimize performance bottlenecks.

    Demonstrates:
    - High confidence threshold (only very certain recommendations)
    - Metrics-based analysis
    - Actionable optimization strategies
    - Before/after measurement
    """

    optimizer = Agent(
        model="scalix-advanced",
        instructions=guidelines.load("performance-optimization"),
        tools=[
            Tool.profiler(),
            Tool.metrics_collector(),
            Tool.load_tester(),
            Tool.code_analyzer()
        ],
        confidence_threshold=85  # Very high bar for perf changes
    )

    # Profile and optimize
    result = await optimizer.run(
        prompt="Optimize API response time for user endpoints",
        phases=[
            "profiling",
            "root-cause-analysis",
            "optimization-design",
            "implementation"
        ]
    )

    print("=== Performance Optimization Results ===\n")

    # Only show high-confidence findings
    print(f"Issues found: {len(result.findings)}")
    print(f"High-confidence issues: {len(result.findings_high_confidence)}")
    print(f"Confidence threshold: {result.findings_high_confidence[0].confidence if result.findings_high_confidence else 'N/A'}%+\n")

    # Show detailed findings
    for i, finding in enumerate(result.findings_high_confidence, 1):
        print(f"{i}. {finding.text}")

        evidence = finding.evidence
        print(f"   Current: {evidence.get('current_latency', '?')}ms")
        print(f"   Target: {evidence.get('target_latency', '?')}ms")
        print(f"   Estimated improvement: {evidence.get('improvement', '?')}%")
        print(f"   Implementation effort: {evidence.get('effort_hours', '?')} hours")
        print(f"   Risk: {evidence.get('risk', 'unknown')}")
        print()

    # Show methodology
    print("Analysis methodology:")
    print(result.methodology)

    return result


# ============================================================================
# Example 5: Team of Agents with Different Guidelines
# ============================================================================

async def example_team_of_agents():
    """
    Use multiple agents with different behavioral guidelines
    working together on a complex task.

    Demonstrates:
    - Agent specialization
    - Sequential workflow (analyst → designer → optimizer)
    - Sharing context between agents
    """

    # Create specialized agents
    analyst = Agent(
        model="scalix-advanced",
        instructions=guidelines.load("data-analyst"),
        tools=[Tool.sql_query(), Tool.data_visualization()]
    )

    designer = Agent(
        model="scalix-advanced",
        instructions=guidelines.load("api-designer"),
        tools=[Tool.code_search(), Tool.schema_generator()]
    )

    optimizer = Agent(
        model="scalix-advanced",
        instructions=guidelines.load("performance-optimization"),
        tools=[Tool.profiler(), Tool.metrics_collector()],
        confidence_threshold=85
    )

    # Create team
    team = Team(
        agents={
            "analyst": analyst,
            "designer": designer,
            "optimizer": optimizer
        },
        workflow="sequential"  # Run in order
    )

    # Run team workflow
    result = await team.run(
        prompt="Build analytics API: analyze data, design API, optimize performance"
    )

    print("=== Team Results ===\n")

    # Show results from each agent
    for agent_name, agent_result in result.agent_results.items():
        print(f"\n{agent_name.upper()}")
        print(f"  Findings: {len(agent_result.findings_high_confidence)}")
        print(f"  Time: {agent_result.execution_time:.1f}s")

        for finding in agent_result.findings_high_confidence[:3]:  # Top 3
            print(f"    - {finding.text}")

    # Save team results
    with open("team_results.json", "w") as f:
        json.dump({
            "team_workflow": "sequential",
            "agent_results": {
                name: {
                    "findings": len(res.findings_high_confidence),
                    "time": res.execution_time
                }
                for name, res in result.agent_results.items()
            }
        }, f, indent=2)

    return result


# ============================================================================
# Example 6: Custom Confidence Threshold
# ============================================================================

async def example_custom_confidence():
    """
    Demonstrate different confidence thresholds for different scenarios.

    High threshold (90%): Critical decisions (migrations, infrastructure)
    Medium threshold (75%): Normal decisions (features, optimizations)
    Low threshold (50%): Exploratory work (brainstorming, ideas)
    """

    # Strict: Critical decisions
    print("=== Strict Analysis (90% confidence) ===")
    migrator_strict = Agent(
        instructions=guidelines.load("code-migrator"),
        confidence_threshold=90
    )

    result_strict = await migrator_strict.run(
        "Plan database migration"
    )

    print(f"High-confidence findings: {len(result_strict.findings_high_confidence)}")
    print("(Only the most certain recommendations)")

    # Medium: Normal decisions
    print("\n=== Normal Analysis (75% confidence) ===")
    analyst_normal = Agent(
        instructions=guidelines.load("data-analyst"),
        confidence_threshold=75
    )

    result_normal = await analyst_normal.run(
        "Analyze sales trends"
    )

    print(f"High-confidence findings: {len(result_normal.findings_high_confidence)}")
    print("(Well-supported recommendations)")

    # Low: Exploratory work
    print("\n=== Exploratory Analysis (50% confidence) ===")
    designer_exploratory = Agent(
        instructions=guidelines.load("api-designer"),
        confidence_threshold=50
    )

    result_exploratory = await designer_exploratory.run(
        "Brainstorm API designs for new feature"
    )

    print(f"High-confidence findings: {len(result_exploratory.findings_high_confidence)}")
    print("(More ideas, less certainty)")


# ============================================================================
# Main execution
# ============================================================================

async def main():
    """Run all examples"""

    print("Scalix World Agent Behavioral Guidelines - Examples\n")
    print("=" * 60)

    # Uncomment examples to run

    # print("\n1. Data Analyst with Confidence Filtering")
    # await example_data_analyst()

    # print("\n2. API Designer with Checkpoints")
    # await example_api_designer_with_checkpoints()

    # print("\n3. Code Migration with Evidence")
    # await example_code_migration()

    # print("\n4. Performance Optimization")
    # await example_performance_optimization()

    # print("\n5. Team of Agents")
    # await example_team_of_agents()

    # print("\n6. Custom Confidence Thresholds")
    # await example_custom_confidence()

    print("\nTo run examples, uncomment desired sections in main()")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
