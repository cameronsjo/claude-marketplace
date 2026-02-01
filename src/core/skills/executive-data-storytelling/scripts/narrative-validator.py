#!/usr/bin/env python3
"""
Narrative Validator

Validates an executive narrative for What/Why/Next structure compliance.

Usage:
    python scripts/narrative-validator.py narrative.md
    python scripts/narrative-validator.py narrative.md --strict
    python scripts/narrative-validator.py narrative.md --output validation-report.md

Example:
    python scripts/narrative-validator.py my-executive-narrative.md
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple


def extract_sections(content: str) -> Dict[str, str]:
    """Extract What/Why/Next sections from narrative."""
    sections = {
        'what': '',
        'why': '',
        'next': '',
        'decision_required': '',
    }

    # Look for section headers (case-insensitive)
    what_match = re.search(r'##?\s*WHAT\s*\(.*?\)(.*?)(?=##?\s*WHY|$)', content, re.IGNORECASE | re.DOTALL)
    why_match = re.search(r'##?\s*WHY\s*\(.*?\)(.*?)(?=##?\s*NEXT|$)', content, re.IGNORECASE | re.DOTALL)
    next_match = re.search(r'##?\s*NEXT\s*\(.*?\)(.*?)(?=##?\s*DECISION|##?\s*EMOTIONAL|$)', content, re.IGNORECASE | re.DOTALL)
    decision_match = re.search(r'##?\s*DECISION REQUIRED(.*?)(?=##|$)', content, re.IGNORECASE | re.DOTALL)

    if what_match:
        sections['what'] = what_match.group(1).strip()
    if why_match:
        sections['why'] = why_match.group(1).strip()
    if next_match:
        sections['next'] = next_match.group(1).strip()
    if decision_match:
        sections['decision_required'] = decision_match.group(1).strip()

    return sections


def validate_what_section(content: str) -> List[str]:
    """Validate WHAT section for required elements."""
    issues = []

    if not content:
        issues.append("WHAT section is missing or empty")
        return issues

    # Check for metric/number
    has_number = bool(re.search(r'\d+', content))
    if not has_number:
        issues.append("WHAT section missing specific metrics/numbers")

    # Check for CEO priority mention
    ceo_priorities = ['growth', 'technology', 'workforce', 'financial']
    has_priority = any(priority in content.lower() for priority in ceo_priorities)
    if not has_priority:
        issues.append("WHAT section doesn't connect to CEO priority (Growth/Technology/Workforce/Financial)")

    # Check for target/baseline comparison
    comparison_words = ['target', 'baseline', 'vs', 'compared to', 'ahead', 'behind', 'on track']
    has_comparison = any(word in content.lower() for word in comparison_words)
    if not has_comparison:
        issues.append("WHAT section missing target/baseline comparison")

    return issues


def validate_why_section(content: str) -> List[str]:
    """Validate WHY section for required elements."""
    issues = []

    if not content:
        issues.append("WHY section is missing or empty")
        return issues

    # Check for data/evidence
    has_data = bool(re.search(r'\d+%|\d+x|\$\d+', content))
    if not has_data:
        issues.append("WHY section missing specific data/evidence")

    # Check for depersonalization (avoid "we", "our team", "I")
    personal_pronouns = re.findall(r'\b(we|our|us|my|I)\b', content, re.IGNORECASE)
    if len(personal_pronouns) > 5:
        issues.append(f"WHY section uses personal pronouns {len(personal_pronouns)} times - consider depersonalizing")

    # Check for defensive language
    defensive_phrases = ['struggled', 'couldn\'t', 'didn\'t anticipate', 'tried to', 'failed to']
    found_defensive = [phrase for phrase in defensive_phrases if phrase in content.lower()]
    if found_defensive:
        issues.append(f"WHY section uses defensive language: {', '.join(found_defensive)}")

    return issues


def validate_next_section(content: str) -> List[str]:
    """Validate NEXT section for required elements."""
    issues = []

    if not content:
        issues.append("NEXT section is missing or empty")
        return issues

    # Check for recommendation
    recommendation_words = ['recommend', 'propose', 'suggest', 'should', 'next step']
    has_recommendation = any(word in content.lower() for word in recommendation_words)
    if not has_recommendation:
        issues.append("NEXT section missing clear recommendation")

    # Check for expected outcome
    outcome_words = ['will', 'expect', 'result in', 'achieve', 'deliver', 'outcome']
    has_outcome = any(word in content.lower() for word in outcome_words)
    if not has_outcome:
        issues.append("NEXT section missing expected outcomes")

    # Check for investment/cost
    has_investment = bool(re.search(r'\$\d+|investment|budget|cost|resource', content, re.IGNORECASE))
    if not has_investment:
        issues.append("NEXT section missing investment/resource requirements")

    # Check for timeline
    timeline_patterns = [
        r'\d+\s*(week|month|quarter|year)s?',
        r'Q[1-4]',
        r'\d{4}',
        r'by\s+\w+\s+\d+',
    ]
    has_timeline = any(re.search(pattern, content, re.IGNORECASE) for pattern in timeline_patterns)
    if not has_timeline:
        issues.append("NEXT section missing specific timeline")

    return issues


def validate_decision_section(content: str) -> List[str]:
    """Validate DECISION REQUIRED section."""
    issues = []

    if not content:
        issues.append("DECISION REQUIRED section is missing")
        return issues

    # Check for decision type
    decision_types = ['approval', 'prioritization', 'resource allocation', 'direction', 'awareness']
    has_type = any(dtype in content.lower() for dtype in decision_types)
    if not has_type:
        issues.append("DECISION section missing decision type (approval/prioritization/etc)")

    # Check for specific ask
    has_ask = bool(re.search(r'(ask|need|require):', content, re.IGNORECASE))
    if not has_ask:
        issues.append("DECISION section missing specific ask")

    return issues


def check_overall_structure(content: str, sections: Dict[str, str]) -> List[str]:
    """Check overall narrative structure."""
    issues = []

    # Check section order
    section_positions = {}
    for section_name in ['WHAT', 'WHY', 'NEXT', 'DECISION REQUIRED']:
        match = re.search(rf'##?\s*{section_name}', content, re.IGNORECASE)
        if match:
            section_positions[section_name] = match.start()

    if len(section_positions) >= 3:
        sections_list = sorted(section_positions.items(), key=lambda x: x[1])
        expected_order = ['WHAT', 'WHY', 'NEXT']
        actual_order = [s[0] for s in sections_list if s[0] in expected_order]

        if actual_order != expected_order:
            issues.append(f"Sections out of order: {' → '.join(actual_order)} (expected: WHAT → WHY → NEXT)")

    # Check for jargon/acronyms
    common_jargon = ['MAU', 'DAU', 'MQL', 'SQL', 'LTV', 'CAC', 'TTM', 'CSAT']
    found_jargon = [term for term in common_jargon if term in content]
    if found_jargon:
        issues.append(f"Common jargon found (define or eliminate): {', '.join(found_jargon)}")

    return issues


def generate_validation_report(
    sections: Dict[str, str],
    what_issues: List[str],
    why_issues: List[str],
    next_issues: List[str],
    decision_issues: List[str],
    overall_issues: List[str],
) -> str:
    """Generate validation report."""

    total_issues = len(what_issues) + len(why_issues) + len(next_issues) + len(decision_issues) + len(overall_issues)

    report = []
    report.append("# Narrative Validation Report\n")

    # Summary
    if total_issues == 0:
        report.append("## ✅ Validation Passed\n")
        report.append("Your narrative follows the What/Why/Next structure correctly!\n")
    else:
        report.append(f"## ⚠️  {total_issues} Issues Found\n")

    # Section presence
    report.append("## Structure Check\n")
    for section_name, section_content in sections.items():
        display_name = section_name.replace('_', ' ').title()
        if section_content:
            report.append(f"- ✅ {display_name} section present")
        else:
            report.append(f"- ❌ {display_name} section missing")
    report.append("")

    # Issues by section
    if what_issues:
        report.append("## WHAT Section Issues\n")
        for issue in what_issues:
            report.append(f"- ⚠️  {issue}")
        report.append("")

    if why_issues:
        report.append("## WHY Section Issues\n")
        for issue in why_issues:
            report.append(f"- ⚠️  {issue}")
        report.append("")

    if next_issues:
        report.append("## NEXT Section Issues\n")
        for issue in next_issues:
            report.append(f"- ⚠️  {issue}")
        report.append("")

    if decision_issues:
        report.append("## DECISION REQUIRED Section Issues\n")
        for issue in decision_issues:
            report.append(f"- ⚠️  {issue}")
        report.append("")

    if overall_issues:
        report.append("## Overall Issues\n")
        for issue in overall_issues:
            report.append(f"- ⚠️  {issue}")
        report.append("")

    # Recommendations
    if total_issues > 0:
        report.append("## Recommendations\n")
        report.append("1. Review the Executive Data Storytelling skill documentation")
        report.append("2. Use the narrative template to ensure all required elements are included")
        report.append("3. Run this validator again after making corrections\n")

    report.append("---\n")
    report.append("*Validation powered by Executive Data Storytelling skill*")

    return '\n'.join(report)


def main():
    parser = argparse.ArgumentParser(
        description="Validate executive narrative structure",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python narrative-validator.py narrative.md
    python narrative-validator.py narrative.md --strict
    python narrative-validator.py narrative.md --output report.md
        """
    )

    parser.add_argument(
        'narrative',
        type=Path,
        help='Path to narrative file (.md or .txt)'
    )

    parser.add_argument(
        '--strict',
        action='store_true',
        help='Fail validation if any issues found (default: warn only)'
    )

    parser.add_argument(
        '--output', '-o',
        type=Path,
        help='Save validation report to file'
    )

    args = parser.parse_args()

    # Read narrative
    if not args.narrative.exists():
        print(f"Error: File not found: {args.narrative}", file=sys.stderr)
        sys.exit(2)

    print(f"Validating narrative: {args.narrative.name}")
    print()

    content = args.narrative.read_text()

    # Extract sections
    sections = extract_sections(content)

    # Validate each section
    what_issues = validate_what_section(sections['what'])
    why_issues = validate_why_section(sections['why'])
    next_issues = validate_next_section(sections['next'])
    decision_issues = validate_decision_section(sections['decision_required'])
    overall_issues = check_overall_structure(content, sections)

    # Generate report
    report = generate_validation_report(
        sections,
        what_issues,
        why_issues,
        next_issues,
        decision_issues,
        overall_issues,
    )

    # Output
    if args.output:
        args.output.write_text(report)
        print(f"Report saved to: {args.output}")
        print()

    print(report)

    # Exit code
    total_issues = len(what_issues) + len(why_issues) + len(next_issues) + len(decision_issues) + len(overall_issues)

    if total_issues == 0:
        sys.exit(0)
    elif args.strict:
        sys.exit(1)
    else:
        sys.exit(0)  # Warnings only, not failures


if __name__ == '__main__':
    main()
