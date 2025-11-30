#!/usr/bin/env python3
"""
Political Attack Neutralization - Decision Support Tool

This script helps assess whether neutralization is appropriate and guides
you through the decision-making process using the MOAR framework.

Usage:
    python scripts/decision-support.py --assess
    python scripts/decision-support.py --quick-check
    python scripts/decision-support.py --power-inventory

Examples:
    python scripts/decision-support.py --assess
    # Interactive assessment of situation

    python scripts/decision-support.py --quick-check --situation "Colleague signed unauthorized contract"
    # Quick recommendation without full assessment
"""

import argparse
import sys
from enum import Enum
from typing import Dict, List, Tuple


class DecisionOutcome(Enum):
    """Possible decision outcomes."""
    PROCEED = "proceed"
    ESCALATE = "escalate"
    DIPLOMACY = "use_diplomacy"
    ALTERNATIVE = "use_alternative"
    DO_NOT_PROCEED = "do_not_proceed"


class RiskLevel(Enum):
    """Risk assessment levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    UNACCEPTABLE = "unacceptable"


class PowerSource(Enum):
    """Sources of organizational power."""
    POSITIONAL = "positional"
    EXPERT = "expert"
    RESOURCE = "resource"
    RELATIONSHIP = "relationship"
    INFORMATION = "information"
    PROCESS = "process"


def assess_behavior_severity(situation: str) -> Tuple[int, str]:
    """
    Assess severity of behavior (1-10 scale).

    Returns:
        (severity_score, explanation)
    """
    # Common severe indicators
    severe_indicators = [
        "policy violation",
        "repeated",
        "multiple teams affected",
        "enterprise risk",
        "compliance",
        "legal",
        "fraud",
        "harassment"
    ]

    # Medium severity indicators
    medium_indicators = [
        "team impact",
        "project delay",
        "trust damage",
        "blame",
        "hoarding",
        "unauthorized"
    ]

    situation_lower = situation.lower()
    score = 5  # Start neutral

    for indicator in severe_indicators:
        if indicator in situation_lower:
            score += 2

    for indicator in medium_indicators:
        if indicator in situation_lower:
            score += 1

    score = min(10, max(1, score))

    if score >= 8:
        explanation = "High severity - significant policy violation or enterprise risk"
    elif score >= 6:
        explanation = "Medium-high severity - clear business impact"
    elif score >= 4:
        explanation = "Medium severity - team or project impact"
    else:
        explanation = "Low severity - may be resolvable through diplomacy"

    return score, explanation


def assess_power_sufficiency(power_sources: List[PowerSource]) -> Tuple[bool, str]:
    """
    Assess if power sources are sufficient for neutralization.

    Returns:
        (is_sufficient, explanation)
    """
    if len(power_sources) == 0:
        return False, "No power sources identified - escalation required"

    if len(power_sources) == 1:
        return False, "Single power source may be insufficient - consider escalation"

    # Strong combinations
    strong_combinations = [
        {PowerSource.POSITIONAL, PowerSource.RESOURCE},
        {PowerSource.POSITIONAL, PowerSource.PROCESS},
        {PowerSource.EXPERT, PowerSource.RELATIONSHIP},
    ]

    power_set = set(power_sources)
    for combo in strong_combinations:
        if combo.issubset(power_set):
            return True, f"Strong power combination: {', '.join(p.value for p in combo)}"

    if len(power_sources) >= 3:
        return True, "Multiple diverse power sources provide sufficient leverage"

    return True, "Moderate power - proceed with caution"


def assess_restoration_readiness(
    angry: bool,
    grudge: bool,
    has_plan: bool
) -> Tuple[bool, List[str]]:
    """
    Assess readiness to restore the relationship.

    Returns:
        (is_ready, reasons)
    """
    ready = True
    reasons = []

    if angry:
        ready = False
        reasons.append("Still acting from anger - wait until calm")

    if grudge:
        ready = False
        reasons.append("Holding a grudge - cannot genuinely restore")

    if not has_plan:
        ready = False
        reasons.append("No restoration plan - required before proceeding")

    if ready:
        reasons.append("Ready to restore - acting on principle with plan")

    return ready, reasons


def assess_collateral_damage(
    team_impact: int,
    project_impact: int,
    relationship_impact: int
) -> Tuple[RiskLevel, str]:
    """
    Assess collateral damage risk (1-10 scale for each dimension).

    Returns:
        (risk_level, explanation)
    """
    total_impact = team_impact + project_impact + relationship_impact
    avg_impact = total_impact / 3

    if avg_impact >= 8:
        return RiskLevel.UNACCEPTABLE, "Unacceptable collateral damage - find alternative"
    elif avg_impact >= 6:
        return RiskLevel.HIGH, "High risk - reconsider or minimize scope"
    elif avg_impact >= 4:
        return RiskLevel.MEDIUM, "Medium risk - proceed with caution and mitigation"
    else:
        return RiskLevel.LOW, "Low risk - acceptable collateral damage"


def make_decision(
    severity: int,
    diplomacy_failed: bool,
    has_power: bool,
    can_restore: bool,
    risk_level: RiskLevel
) -> Tuple[DecisionOutcome, str]:
    """
    Make final decision based on assessments.

    Returns:
        (decision, reasoning)
    """
    # Not severe enough
    if severity < 4:
        return DecisionOutcome.DO_NOT_PROCEED, "Severity too low - monitor situation"

    # Try diplomacy first
    if not diplomacy_failed:
        return DecisionOutcome.DIPLOMACY, "Attempt verbal diplomacy before neutralization"

    # Lack power
    if not has_power:
        return DecisionOutcome.ESCALATE, "Insufficient power - escalate to someone who has it"

    # Cannot restore
    if not can_restore:
        return DecisionOutcome.DO_NOT_PROCEED, "Cannot restore afterward - find alternative approach"

    # Risk too high
    if risk_level == RiskLevel.UNACCEPTABLE:
        return DecisionOutcome.ALTERNATIVE, "Collateral damage too high - use alternative approach"

    # All conditions met
    if risk_level in [RiskLevel.LOW, RiskLevel.MEDIUM]:
        return DecisionOutcome.PROCEED, "Conditions met - proceed with MOAR framework"

    # High risk but may proceed with caution
    return DecisionOutcome.PROCEED, "High risk - proceed with caution and clear mitigation plan"


def generate_recommendation_report(
    situation: str,
    severity: int,
    severity_explanation: str,
    diplomacy_failed: bool,
    power_sources: List[PowerSource],
    has_power: bool,
    power_explanation: str,
    can_restore: bool,
    restoration_reasons: List[str],
    risk_level: RiskLevel,
    risk_explanation: str,
    decision: DecisionOutcome,
    decision_reasoning: str
) -> str:
    """Generate markdown report with recommendation."""

    report_lines = [
        "# Political Attack Neutralization - Decision Support Report",
        "",
        "## Situation",
        "",
        f"**Description:** {situation}",
        "",
        "---",
        "",
        "## Assessment",
        "",
        "### 1. Behavior Severity",
        "",
        f"**Severity Score:** {severity} / 10",
        "",
        f"**Assessment:** {severity_explanation}",
        "",
        "---",
        "",
        "### 2. Diplomacy Status",
        "",
        f"**Diplomacy Attempted:** {'Yes' if diplomacy_failed else 'No'}",
        "",
        f"**Status:** {'Failed - neutralization may be needed' if diplomacy_failed else 'Not yet attempted - try diplomacy first'}",
        "",
        "---",
        "",
        "### 3. Power Assessment",
        "",
        f"**Power Sources Available:** {len(power_sources)}",
        "",
    ]

    if power_sources:
        report_lines.append("**Your Power Sources:**")
        report_lines.append("")
        for ps in power_sources:
            report_lines.append(f"- {ps.value.capitalize()} power")
        report_lines.append("")

    report_lines.extend([
        f"**Sufficient Power:** {'Yes' if has_power else 'No'}",
        "",
        f"**Assessment:** {power_explanation}",
        "",
        "---",
        "",
        "### 4. Restoration Readiness",
        "",
        f"**Ready to Restore:** {'Yes' if can_restore else 'No'}",
        "",
        "**Assessment:**",
        ""
    ])

    for reason in restoration_reasons:
        report_lines.append(f"- {reason}")

    report_lines.extend([
        "",
        "---",
        "",
        "### 5. Collateral Damage Risk",
        "",
        f"**Risk Level:** {risk_level.value.upper()}",
        "",
        f"**Assessment:** {risk_explanation}",
        "",
        "---",
        "",
        "## Recommendation",
        "",
    ])

    # Decision-specific recommendations
    if decision == DecisionOutcome.PROCEED:
        report_lines.extend([
            "### ✅ PROCEED WITH MOAR FRAMEWORK",
            "",
            f"**Reasoning:** {decision_reasoning}",
            "",
            "### Next Steps:",
            "",
            "1. **MESSAGE** - Draft your four-part message",
            "   - NAME the behavior",
            "   - STATE why it's problematic",
            "   - HOLD accountable",
            "   - MAKE consequences clear",
            "",
            "2. **OBSTRUCT** - Identify obstruction tactics",
            "   - Use proportionate force",
            "   - Leverage your power sources",
            "   - Minimize collateral damage",
            "",
            "3. **AGITATE** - Calibrate agitation level",
            "   - Match visibility to severity",
            "   - Private to Enterprise scale",
            "   - Only as much as needed",
            "",
            "4. **RESTORE** - Plan restoration actions",
            "   - Material actions they value",
            "   - Visible partnership",
            "   - Genuine collaboration",
            "",
            "### Required Documents:",
            "",
            "- [ ] Complete Message Formula Template",
            "- [ ] Complete Risk Assessment Checklist",
            "- [ ] Complete Restoration Plan Template",
            "- [ ] Document the situation and evidence",
        ])

    elif decision == DecisionOutcome.DIPLOMACY:
        report_lines.extend([
            "### 💬 USE VERBAL DIPLOMACY FIRST",
            "",
            f"**Reasoning:** {decision_reasoning}",
            "",
            "### Next Steps:",
            "",
            "1. Schedule private conversation",
            "2. Explain the business impact",
            "3. Seek mutual understanding",
            "4. Request specific behavior change",
            "5. Document the conversation",
            "",
            "### If Diplomacy Fails:",
            "",
            "Reassess using this tool and consider neutralization if:",
            "- Pattern continues after clear feedback",
            "- They dismiss or ignore concerns",
            "- Business impact persists or increases",
        ])

    elif decision == DecisionOutcome.ESCALATE:
        report_lines.extend([
            "### ⬆️  ESCALATE TO SUPERIOR",
            "",
            f"**Reasoning:** {decision_reasoning}",
            "",
            "### Next Steps:",
            "",
            "1. **Document thoroughly:**",
            "   - Specific incidents with dates",
            "   - Business impact quantified",
            "   - Evidence and examples",
            "",
            "2. **Prepare escalation:**",
            "   - Clear problem statement",
            "   - Recommended action",
            "   - Supporting documentation",
            "",
            "3. **Present to superior:**",
            "   - Focus on business impact",
            "   - Provide evidence",
            "   - Request specific action",
        ])

    elif decision == DecisionOutcome.ALTERNATIVE:
        report_lines.extend([
            "### 🔄 USE ALTERNATIVE APPROACH",
            "",
            f"**Reasoning:** {decision_reasoning}",
            "",
            "### Alternative Options:",
            "",
            "#### Option 1: Process Changes",
            "- Identify systemic issues",
            "- Implement controls",
            "- Remove opportunities for behavior",
            "",
            "#### Option 2: Mediation",
            "- Engage neutral third party",
            "- Focus on interests",
            "- Seek mutual understanding",
            "",
            "#### Option 3: Accept and Monitor",
            "- Document all incidents",
            "- Set clear boundaries",
            "- Reassess if escalates",
        ])

    else:  # DO_NOT_PROCEED
        report_lines.extend([
            "### ❌ DO NOT PROCEED WITH NEUTRALIZATION",
            "",
            f"**Reasoning:** {decision_reasoning}",
            "",
            "### Why Not to Proceed:",
            "",
        ])

        if severity < 4:
            report_lines.append("- Severity is too low to warrant neutralization")
        if not can_restore:
            report_lines.append("- Cannot genuinely restore afterward - this is critical")
        if risk_level == RiskLevel.UNACCEPTABLE:
            report_lines.append("- Collateral damage outweighs any benefit")

        report_lines.extend([
            "",
            "### What to Do Instead:",
            "",
            "- Monitor the situation",
            "- Document if behavior continues",
            "- Consider process changes",
            "- Reassess if situation changes",
        ])

    report_lines.extend([
        "",
        "---",
        "",
        "## Resources",
        "",
        "- `resources/message-formula-template.md` - Message crafting",
        "- `resources/risk-assessment-checklist.md` - Full risk assessment",
        "- `resources/restoration-plan-template.md` - Restoration planning",
        "- `resources/decision-tree.md` - Visual decision framework",
        "",
        "---",
        "",
        "*This report is for guidance only. Use your judgment and consult with trusted advisors.*"
    ])

    return "\n".join(report_lines)


def quick_check(situation: str) -> str:
    """
    Quick assessment without full interactive mode.

    Returns markdown summary.
    """
    severity, severity_explanation = assess_behavior_severity(situation)

    # Simple heuristics for quick check
    diplomacy_failed = "repeated" in situation.lower() or "continues" in situation.lower()

    # Assume moderate power for quick check
    power_sources = [PowerSource.POSITIONAL, PowerSource.EXPERT]
    has_power, power_explanation = assess_power_sufficiency(power_sources)

    # Assume ready to restore for quick check
    can_restore = True
    restoration_reasons = ["Quick check assumes readiness - verify manually"]

    # Assume medium risk for quick check
    risk_level = RiskLevel.MEDIUM
    risk_explanation = "Quick check assumes medium risk - assess thoroughly"

    decision, decision_reasoning = make_decision(
        severity, diplomacy_failed, has_power, can_restore, risk_level
    )

    return generate_recommendation_report(
        situation,
        severity,
        severity_explanation,
        diplomacy_failed,
        power_sources,
        has_power,
        power_explanation,
        can_restore,
        restoration_reasons,
        risk_level,
        risk_explanation,
        decision,
        decision_reasoning
    )


def interactive_assessment() -> str:
    """Interactive assessment mode."""

    print("# Political Attack Neutralization - Decision Support")
    print()
    print("This tool will guide you through the decision-making process.")
    print()

    # 1. Situation
    print("## 1. Describe the Situation")
    print()
    situation = input("Briefly describe the political attack or behavior: ").strip()

    if not situation:
        print("Error: Situation description required", file=sys.stderr)
        sys.exit(1)

    severity, severity_explanation = assess_behavior_severity(situation)

    print()
    print(f"Severity Assessment: {severity}/10 - {severity_explanation}")
    print()

    # 2. Diplomacy
    print("## 2. Diplomacy Status")
    print()
    diplomacy_response = input("Have you tried verbal diplomacy? (yes/no): ").strip().lower()
    diplomacy_tried = diplomacy_response in ["yes", "y"]

    if diplomacy_tried:
        failed_response = input("Did diplomacy fail to resolve the issue? (yes/no): ").strip().lower()
        diplomacy_failed = failed_response in ["yes", "y"]
    else:
        diplomacy_failed = False
        print("Consider trying verbal diplomacy first before neutralization.")

    print()

    # 3. Power sources
    print("## 3. Power Assessment")
    print()
    print("Select your available power sources (enter numbers separated by spaces):")
    print("1. Positional (role authority)")
    print("2. Expert (technical expertise)")
    print("3. Resource (budget, headcount)")
    print("4. Relationship (network, alliances)")
    print("5. Information (critical data, insights)")
    print("6. Process (workflow control, approvals)")
    print()

    power_response = input("Your power sources (e.g., '1 2 3'): ").strip()

    power_map = {
        "1": PowerSource.POSITIONAL,
        "2": PowerSource.EXPERT,
        "3": PowerSource.RESOURCE,
        "4": PowerSource.RELATIONSHIP,
        "5": PowerSource.INFORMATION,
        "6": PowerSource.PROCESS,
    }

    power_sources = []
    for num in power_response.split():
        if num in power_map:
            power_sources.append(power_map[num])

    has_power, power_explanation = assess_power_sufficiency(power_sources)

    print()
    print(f"Power Assessment: {power_explanation}")
    print()

    # 4. Restoration readiness
    print("## 4. Restoration Readiness")
    print()

    angry_response = input("Are you primarily angry or acting on principle? (angry/principle): ").strip().lower()
    angry = angry_response.startswith("angry")

    grudge_response = input("Will you hold a grudge regardless of their accountability? (yes/no): ").strip().lower()
    grudge = grudge_response in ["yes", "y"]

    plan_response = input("Do you have a concrete restoration plan? (yes/no): ").strip().lower()
    has_plan = plan_response in ["yes", "y"]

    can_restore, restoration_reasons = assess_restoration_readiness(angry, grudge, has_plan)

    print()
    for reason in restoration_reasons:
        print(f"- {reason}")
    print()

    # 5. Collateral damage
    print("## 5. Collateral Damage Assessment")
    print()
    print("Rate potential impact (1-10, where 10 is severe):")

    team_impact = int(input("Team impact: ").strip() or "5")
    project_impact = int(input("Project impact: ").strip() or "5")
    relationship_impact = int(input("Relationship impact: ").strip() or "5")

    risk_level, risk_explanation = assess_collateral_damage(
        team_impact, project_impact, relationship_impact
    )

    print()
    print(f"Risk Assessment: {risk_level.value.upper()} - {risk_explanation}")
    print()

    # Final decision
    decision, decision_reasoning = make_decision(
        severity, diplomacy_failed, has_power, can_restore, risk_level
    )

    # Generate report
    return generate_recommendation_report(
        situation,
        severity,
        severity_explanation,
        diplomacy_failed,
        power_sources,
        has_power,
        power_explanation,
        can_restore,
        restoration_reasons,
        risk_level,
        risk_explanation,
        decision,
        decision_reasoning
    )


def power_inventory() -> str:
    """Generate power source inventory and analysis."""

    report = [
        "# Power Source Inventory",
        "",
        "## Your Power Sources",
        "",
        "Use this worksheet to identify your available power sources.",
        "",
        "---",
        "",
        "### 1. Positional Power",
        "",
        "**Authority from your role:**",
        "",
        "- What decisions can you make unilaterally?",
        "- What can you approve or deny?",
        "- Who reports to you or your team?",
        "- What resources are under your control?",
        "",
        "**Your positional power:**",
        "```",
        "[Write your assessment]",
        "```",
        "",
        "---",
        "",
        "### 2. Expert Power",
        "",
        "**Technical or domain expertise:**",
        "",
        "- What specialized knowledge do you have?",
        "- What technical decisions do others defer to you on?",
        "- What certifications or credentials do you hold?",
        "- What domain expertise gives you credibility?",
        "",
        "**Your expert power:**",
        "```",
        "[Write your assessment]",
        "```",
        "",
        "---",
        "",
        "### 3. Resource Power",
        "",
        "**Control over budget, headcount, or assets:**",
        "",
        "- What budget do you control?",
        "- How much headcount can you allocate?",
        "- What physical or technical assets do you manage?",
        "- What shared resources do you influence?",
        "",
        "**Your resource power:**",
        "```",
        "[Write your assessment]",
        "```",
        "",
        "---",
        "",
        "### 4. Relationship Power",
        "",
        "**Network and alliances:**",
        "",
        "- Who trusts your judgment?",
        "- What executives or senior leaders support you?",
        "- What cross-functional relationships do you have?",
        "- Who would advocate for you?",
        "",
        "**Your relationship power:**",
        "```",
        "[Write your assessment]",
        "```",
        "",
        "---",
        "",
        "### 5. Information Power",
        "",
        "**Access to critical data or insights:**",
        "",
        "- What metrics or data do you control?",
        "- What insights do others depend on you for?",
        "- What strategic information do you have access to?",
        "- What reporting do you provide to leadership?",
        "",
        "**Your information power:**",
        "```",
        "[Write your assessment]",
        "```",
        "",
        "---",
        "",
        "### 6. Process Power",
        "",
        "**Control over workflows or approvals:**",
        "",
        "- What processes do you own?",
        "- What approval gates can you enforce?",
        "- What policies do you implement?",
        "- What workflows depend on your team?",
        "",
        "**Your process power:**",
        "```",
        "[Write your assessment]",
        "```",
        "",
        "---",
        "",
        "## Power Combinations",
        "",
        "**Strongest combinations for neutralization:**",
        "",
        "1. **Positional + Resource** - Direct authority over resources they need",
        "2. **Positional + Process** - Control over workflows and approvals",
        "3. **Expert + Relationship** - Credibility plus network support",
        "4. **Resource + Process** - Control over resources and how they're accessed",
        "5. **Information + Relationship** - Insights valued by leadership",
        "",
        "**Your power combination:**",
        "```",
        "[Identify your strongest power combinations]",
        "```",
        "",
        "---",
        "",
        "## Power Application Strategy",
        "",
        "**For the current situation:**",
        "",
        "**What power sources apply:**",
        "```",
        "[Which of your power sources are relevant?]",
        "```",
        "",
        "**How you'll leverage them:**",
        "```",
        "[Specific ways to apply your power]",
        "```",
        "",
        "**Proportionality check:**",
        "```",
        "[Is this proportionate to the situation?]",
        "```",
        "",
        "---",
        "",
        "*Use this inventory before taking neutralization action*"
    ]

    return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(
        description="Decision support tool for political attack neutralization"
    )

    parser.add_argument(
        "--assess",
        action="store_true",
        help="Interactive assessment mode"
    )

    parser.add_argument(
        "--quick-check",
        action="store_true",
        help="Quick assessment without full interaction"
    )

    parser.add_argument(
        "--situation",
        type=str,
        help="Situation description (for quick-check mode)"
    )

    parser.add_argument(
        "--power-inventory",
        action="store_true",
        help="Generate power source inventory worksheet"
    )

    parser.add_argument(
        "--output",
        type=str,
        help="Output file (default: print to stdout)"
    )

    args = parser.parse_args()

    if args.assess:
        report = interactive_assessment()
    elif args.quick_check:
        if not args.situation:
            print("Error: --situation required for --quick-check", file=sys.stderr)
            sys.exit(1)
        report = quick_check(args.situation)
    elif args.power_inventory:
        report = power_inventory()
    else:
        parser.print_help()
        print("\nError: Choose --assess, --quick-check, or --power-inventory", file=sys.stderr)
        sys.exit(1)

    # Output
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"Report written to {args.output}", file=sys.stderr)
    else:
        print(report)


if __name__ == "__main__":
    main()
