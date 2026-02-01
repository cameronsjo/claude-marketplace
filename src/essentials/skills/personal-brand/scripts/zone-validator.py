#!/usr/bin/env python3
"""
Zone of Distinction Validator - Test if your zone of distinction is sufficiently specific

This script validates your zone of distinction by testing:
- Specificity (is it unique or generic?)
- Clarity (is it understandable?)
- Market alignment (does it address market needs?)
- Authenticity (can you sustain it?)
- Evidence (can you prove it?)

Usage:
    python scripts/zone-validator.py --zone "Digital transformation catalyst"
    python scripts/zone-validator.py --interactive
    python scripts/zone-validator.py --zone "Strategic leader" --verbose

Examples:
    python scripts/zone-validator.py --zone "Technical debt eliminator"
    # Output: Validation report with specificity score and recommendations

    python scripts/zone-validator.py --interactive
    # Guided interview-style validation
"""

import argparse
import sys
from typing import Dict, List, Tuple

# Generic indicators that reduce distinctiveness
GENERIC_TERMS = [
    "strategic",
    "innovative",
    "results-oriented",
    "dependable",
    "reliable",
    "experienced",
    "skilled",
    "talented",
    "team player",
    "collaborative",
    "effective",
    "efficient",
    "great",
    "good",
    "excellent",
    "strong",
    "leader",
    "manager",
    "executive",
    "professional",
]

# Role-specific generic terms (these are expected for certain roles)
ROLE_GENERIC_TERMS = {
    "cio": ["it leader", "technology leader", "cio"],
    "cto": ["cto", "technology officer", "technical leader"],
    "product": ["product manager", "product leader"],
    "engineering": ["engineering manager", "engineering leader"],
}

# Distinctive characteristics to look for
DISTINCTIVE_INDICATORS = [
    "catalyst",
    "architect",
    "multiplier",
    "champion",
    "evangelist",
    "eliminator",
    "optimizer",
    "curator",
    "accelerator",
    "translator",
    "enabler",
    "strategist",
    "co-creator",
    "driver",
    "advocate",
]

# Market-aligned themes (high-value topics)
MARKET_THEMES = [
    "digital transformation",
    "business partnership",
    "customer experience",
    "innovation",
    "platform",
    "data-driven",
    "security",
    "developer experience",
    "technical debt",
    "cloud",
    "agile",
    "devops",
    "ai/ml",
    "automation",
    "cost optimization",
    "risk management",
]


def count_generic_terms(zone: str) -> Tuple[int, List[str]]:
    """Count how many generic terms are in the zone of distinction."""
    zone_lower = zone.lower()
    found_generic = []

    for term in GENERIC_TERMS:
        if term in zone_lower:
            found_generic.append(term)

    return len(found_generic), found_generic


def count_distinctive_terms(zone: str) -> Tuple[int, List[str]]:
    """Count how many distinctive terms are in the zone of distinction."""
    zone_lower = zone.lower()
    found_distinctive = []

    for term in DISTINCTIVE_INDICATORS:
        if term in zone_lower:
            found_distinctive.append(term)

    return len(found_distinctive), found_distinctive


def check_market_alignment(zone: str) -> Tuple[int, List[str]]:
    """Check if zone of distinction aligns with market themes."""
    zone_lower = zone.lower()
    found_themes = []

    for theme in MARKET_THEMES:
        if theme in zone_lower:
            found_themes.append(theme)

    return len(found_themes), found_themes


def calculate_specificity_score(zone: str) -> Tuple[int, Dict[str, any]]:
    """
    Calculate specificity score for zone of distinction.

    Returns:
        (score, details) where score is 1-10:
        10 = highly specific and distinctive
        1 = very generic
    """
    score = 5  # Start neutral
    details = {}

    # Word count (optimal is 2-4 words)
    word_count = len(zone.split())
    details["word_count"] = word_count

    if word_count < 2:
        score -= 2
        details["word_count_feedback"] = "Too short - need more specificity"
    elif word_count > 6:
        score -= 1
        details["word_count_feedback"] = "Too long - may be unfocused"
    else:
        score += 1
        details["word_count_feedback"] = "Good length"

    # Generic terms (each reduces score)
    generic_count, generic_terms = count_generic_terms(zone)
    details["generic_count"] = generic_count
    details["generic_terms"] = generic_terms

    score -= generic_count * 2
    if generic_count == 0:
        details["generic_feedback"] = "No generic terms - excellent!"
    elif generic_count == 1:
        details["generic_feedback"] = "One generic term - consider replacing"
    else:
        details["generic_feedback"] = f"{generic_count} generic terms - too generic"

    # Distinctive terms (each increases score)
    distinctive_count, distinctive_terms = count_distinctive_terms(zone)
    details["distinctive_count"] = distinctive_count
    details["distinctive_terms"] = distinctive_terms

    score += distinctive_count * 2
    if distinctive_count == 0:
        details["distinctive_feedback"] = "No distinctive terms - add action words"
    elif distinctive_count == 1:
        details["distinctive_feedback"] = "Good use of distinctive language"
    else:
        details["distinctive_feedback"] = "Excellent distinctive language"

    # Market alignment (each theme adds score)
    theme_count, themes = check_market_alignment(zone)
    details["theme_count"] = theme_count
    details["themes"] = themes

    score += theme_count
    if theme_count == 0:
        details["theme_feedback"] = "No clear market theme - add context"
    elif theme_count == 1:
        details["theme_feedback"] = "Good market alignment"
    else:
        details["theme_feedback"] = "Strong market alignment"

    # Ensure score is in valid range
    score = max(1, min(10, score))
    details["final_score"] = score

    return score, details


def validate_five_tests(zone: str) -> Dict[str, str]:
    """
    Run the five validation tests from the framework.

    Returns dictionary of test results (pass/fail/uncertain)
    """
    results = {}

    print("\n" + "=" * 60)
    print("ZONE OF DISTINCTION VALIDATION TESTS")
    print("=" * 60)
    print(f"\nYour Zone of Distinction: {zone}")
    print("\nPlease answer the following questions honestly:")
    print("-" * 60)

    # Test 1: Distinction Test
    print("\n1. DISTINCTION TEST")
    print("   Could this zone of distinction apply to any of your peers,")
    print("   or is it uniquely yours?")
    response = input("   Answer (unique/peers/uncertain): ").strip().lower()
    results["distinction"] = response
    if response == "peers":
        print("   ⚠️  Consider adding more specific elements")

    # Test 2: Value Test
    print("\n2. VALUE TEST")
    print("   Does this communicate what your market will experience")
    print("   or receive from you?")
    response = input("   Answer (yes/no/uncertain): ").strip().lower()
    results["value"] = response
    if response == "no":
        print("   ⚠️  Reframe to emphasize market value")

    # Test 3: Authenticity Test
    print("\n3. AUTHENTICITY TEST")
    print("   Can you sustain this zone consistently over time")
    print("   without burning out?")
    response = input("   Answer (yes/no/uncertain): ").strip().lower()
    results["authenticity"] = response
    if response == "no":
        print("   ⚠️  Ensure alignment with your core values")

    # Test 4: Evidence Test
    print("\n4. EVIDENCE TEST")
    print("   Do you have proof points from your track record")
    print("   for this positioning?")
    response = input("   Answer (yes/no/uncertain): ").strip().lower()
    results["evidence"] = response
    if response == "no":
        print("   ⚠️  Build credibility before claiming this zone")

    # Test 5: Market Test
    print("\n5. MARKET TEST")
    print("   Is this what your market actually needs right now?")
    response = input("   Answer (yes/no/uncertain): ").strip().lower()
    results["market"] = response
    if response == "no":
        print("   ⚠️  Realign with current market priorities")

    return results


def generate_recommendations(score: int, details: Dict, zone: str) -> List[str]:
    """Generate actionable recommendations based on validation results."""
    recommendations = []

    if score >= 8:
        recommendations.append(
            "✅ Your zone of distinction is highly specific and distinctive!"
        )
    elif score >= 6:
        recommendations.append(
            "⚠️ Your zone of distinction is good but could be more distinctive"
        )
    else:
        recommendations.append(
            "❌ Your zone of distinction is too generic - significant revision needed"
        )

    # Generic terms
    if details["generic_count"] > 0:
        recommendations.append(
            f"\n**Remove generic terms:** {', '.join(details['generic_terms'])}"
        )
        recommendations.append(
            "  These terms are forgettable and don't differentiate you."
        )

    # Distinctive terms
    if details["distinctive_count"] == 0:
        recommendations.append(
            "\n**Add distinctive action words:** catalyst, architect, multiplier, "
            "champion, evangelist, eliminator, optimizer, curator"
        )

    # Market themes
    if details["theme_count"] == 0:
        recommendations.append(
            "\n**Add market context:** Reference what your enterprise needs "
            "(e.g., digital transformation, business partnership, innovation)"
        )

    # Word count
    if details["word_count"] < 2:
        recommendations.append(
            "\n**Add more specificity:** Your zone is too short. "
            "Aim for 2-4 words that communicate unique value."
        )
    elif details["word_count"] > 6:
        recommendations.append(
            "\n**Simplify:** Your zone is too long. Distill to 2-4 powerful words."
        )

    # Examples based on issues
    if score < 7:
        recommendations.append("\n**Example transformations:**")
        recommendations.append("  Generic: 'Strategic IT leader'")
        recommendations.append("  Distinctive: 'Digital transformation catalyst'")
        recommendations.append("")
        recommendations.append("  Generic: 'Innovative problem solver'")
        recommendations.append("  Distinctive: 'Technical debt eliminator'")
        recommendations.append("")
        recommendations.append("  Generic: 'Experienced technology executive'")
        recommendations.append("  Distinctive: 'Platform thinking evangelist'")

    return recommendations


def generate_report(
    zone: str,
    score: int,
    details: Dict,
    validation_results: Dict = None,
    verbose: bool = False,
) -> str:
    """Generate markdown validation report."""
    report = [
        "# Zone of Distinction Validation Report",
        "",
        f"**Zone Being Validated:** {zone}",
        "",
        "---",
        "",
        "## Specificity Score",
        "",
        f"**Score:** {score} / 10",
        "",
    ]

    # Score interpretation
    if score >= 8:
        report.append(
            "✅ **Highly Distinctive** - Your zone of distinction is specific and memorable"
        )
    elif score >= 6:
        report.append(
            "⚠️ **Good But Improvable** - Your zone is decent but could be more distinctive"
        )
    elif score >= 4:
        report.append(
            "⚠️ **Needs Work** - Your zone is too generic and needs refinement"
        )
    else:
        report.append(
            "❌ **Too Generic** - Your zone of distinction needs significant revision"
        )

    report.extend(["", "---", "", "## Analysis Details", ""])

    # Word count
    report.extend(
        [
            f"**Word Count:** {details['word_count']} words",
            f"- {details['word_count_feedback']}",
            "",
        ]
    )

    # Generic terms
    report.extend(
        [
            f"**Generic Terms Found:** {details['generic_count']}",
        ]
    )
    if details["generic_terms"]:
        for term in details["generic_terms"]:
            report.append(f"- ❌ '{term}'")
    else:
        report.append("- ✅ None found")
    report.extend([f"- {details['generic_feedback']}", ""])

    # Distinctive terms
    report.extend(
        [
            f"**Distinctive Terms Found:** {details['distinctive_count']}",
        ]
    )
    if details["distinctive_terms"]:
        for term in details["distinctive_terms"]:
            report.append(f"- ✅ '{term}'")
    else:
        report.append("- ❌ None found")
    report.extend([f"- {details['distinctive_feedback']}", ""])

    # Market themes
    report.extend(
        [
            f"**Market Themes Identified:** {details['theme_count']}",
        ]
    )
    if details["themes"]:
        for theme in details["themes"]:
            report.append(f"- ✅ '{theme}'")
    else:
        report.append("- ⚠️ None found")
    report.extend([f"- {details['theme_feedback']}", ""])

    # Validation test results
    if validation_results:
        report.extend(["---", "", "## Five Validation Tests", ""])

        test_names = {
            "distinction": "Distinction Test (Uniquely yours?)",
            "value": "Value Test (Market value clear?)",
            "authenticity": "Authenticity Test (Sustainable?)",
            "evidence": "Evidence Test (Proven track record?)",
            "market": "Market Test (Current market need?)",
        }

        passed = 0
        for key, name in test_names.items():
            result = validation_results.get(key, "uncertain")
            if result in ["yes", "unique"]:
                report.append(f"- ✅ **{name}** - PASS")
                passed += 1
            elif result == "no" or result == "peers":
                report.append(f"- ❌ **{name}** - FAIL")
            else:
                report.append(f"- ⚠️ **{name}** - UNCERTAIN")

        report.extend(["", f"**Tests Passed:** {passed} / 5", ""])

        if passed == 5:
            report.append("✅ Your zone of distinction passes all five tests!")
        elif passed >= 3:
            report.append("⚠️ Your zone passes some tests but needs refinement")
        else:
            report.append(
                "❌ Your zone needs significant work to pass validation tests"
            )

    # Recommendations
    recommendations = generate_recommendations(score, details, zone)
    report.extend(["", "---", "", "## Recommendations", ""])
    report.extend(recommendations)

    # Examples section
    report.extend(
        [
            "",
            "---",
            "",
            "## Examples of Strong Zones of Distinction",
            "",
            "**For CIOs and Technology Leaders:**",
            "- Digital transformation catalyst",
            "- Business-technology partner",
            "- Technical debt eliminator",
            "- Platform thinking evangelist",
            "- Innovation portfolio curator",
            "",
            "**For Product Leaders:**",
            "- Customer journey optimizer",
            "- Experimentation evangelist",
            "- Product-market fit architect",
            "- Outcome obsession champion",
            "",
            "**For Engineering Leaders:**",
            "- Developer experience champion",
            "- Engineering velocity multiplier",
            "- Architecture clarity driver",
            "- Technical mentorship advocate",
            "",
            "---",
            "",
            "## Next Steps",
            "",
            "1. **If score < 7:** Revise your zone of distinction using recommendations above",
            "2. **If score >= 7:** Test with trusted advisors - do they find it memorable and distinctive?",
            "3. **Validate alignment:** Ensure zone intersects Market Need + Your Values + Your Market Value",
            "4. **Create brand promise:** Distill zone into 2-3 word brand promise statement",
            "5. **Develop aspirational brand list:** Build out supporting characteristics",
            "",
            "---",
            "",
            "*Generated by zone-validator.py*",
        ]
    )

    return "\n".join(report)


def interactive_mode():
    """Run interactive validation session."""
    print("\n" + "=" * 60)
    print("INTERACTIVE ZONE OF DISTINCTION VALIDATOR")
    print("=" * 60)
    print("\nThis tool will help you validate your zone of distinction")
    print("through specificity analysis and the five validation tests.")
    print()

    zone = input("Enter your zone of distinction: ").strip()

    if not zone:
        print("Error: Zone of distinction cannot be empty", file=sys.stderr)
        sys.exit(1)

    print(f"\nAnalyzing: {zone}")
    print("=" * 60)

    # Calculate specificity score
    score, details = calculate_specificity_score(zone)

    print(f"\nSpecificity Score: {score} / 10")

    if score >= 8:
        print("✅ Highly distinctive!")
    elif score >= 6:
        print("⚠️ Good but could be better")
    elif score >= 4:
        print("⚠️ Needs improvement")
    else:
        print("❌ Too generic")

    print("\nDetails:")
    print(f"  Word count: {details['word_count']} - {details['word_count_feedback']}")
    print(
        f"  Generic terms: {details['generic_count']} - {details['generic_feedback']}"
    )
    print(
        f"  Distinctive terms: {details['distinctive_count']} - {details['distinctive_feedback']}"
    )
    print(f"  Market themes: {details['theme_count']} - {details['theme_feedback']}")

    # Ask if user wants to run validation tests
    print("\n" + "-" * 60)
    response = input("\nRun the five validation tests? (y/n): ").strip().lower()

    validation_results = None
    if response in ["y", "yes"]:
        validation_results = validate_five_tests(zone)

    # Ask if user wants full report
    print("\n" + "-" * 60)
    response = input("\nGenerate full markdown report? (y/n): ").strip().lower()

    if response in ["y", "yes"]:
        output_file = input(
            "Output filename (default: zone-validation-report.md): "
        ).strip()
        if not output_file:
            output_file = "zone-validation-report.md"

        report = generate_report(zone, score, details, validation_results, verbose=True)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(report)

        print(f"\n✅ Report written to {output_file}")
    else:
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print(f"\nYour zone of distinction: {zone}")
        print(f"Specificity score: {score} / 10")

        if validation_results:
            passed = sum(
                1 for v in validation_results.values() if v in ["yes", "unique"]
            )
            print(f"Validation tests passed: {passed} / 5")

        print("\nRecommendations:")
        recommendations = generate_recommendations(score, details, zone)
        for rec in recommendations[:3]:  # Show top 3
            print(f"  {rec}")


def main():
    parser = argparse.ArgumentParser(
        description="Validate zone of distinction specificity and distinctiveness"
    )
    parser.add_argument("--zone", type=str, help="Zone of distinction to validate")
    parser.add_argument(
        "--interactive", action="store_true", help="Run interactive validation session"
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Include detailed analysis in output"
    )
    parser.add_argument(
        "--output", type=str, help="Output markdown file (default: print to stdout)"
    )
    parser.add_argument(
        "--skip-tests",
        action="store_true",
        help="Skip the five validation tests (only run specificity analysis)",
    )

    args = parser.parse_args()

    if args.interactive:
        interactive_mode()
        sys.exit(0)

    if not args.zone:
        parser.print_help()
        print("\nError: Provide --zone or use --interactive mode", file=sys.stderr)
        sys.exit(1)

    # Calculate specificity score
    score, details = calculate_specificity_score(args.zone)

    # Run validation tests if not skipped
    validation_results = None
    if not args.skip_tests:
        validation_results = validate_five_tests(args.zone)

    # Generate report
    report = generate_report(
        args.zone, score, details, validation_results, verbose=args.verbose
    )

    # Output
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"Report written to {args.output}", file=sys.stderr)
    else:
        print(report)


if __name__ == "__main__":
    main()
