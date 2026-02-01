#!/usr/bin/env python3
"""
Brand Keywords Generator - Generate distinctive brand language variations

This script helps generate distinctive brand language by:
- Suggesting alternatives to generic descriptors
- Creating variations of brand promise statements
- Testing distinctiveness of brand language
- Providing role-specific brand keyword suggestions

Usage:
    python scripts/brand-keywords-generator.py --input "technical leader"
    python scripts/brand-keywords-generator.py --role cio --capability "strategic thinking"
    python scripts/brand-keywords-generator.py --test "dependable technologist"

Examples:
    python scripts/brand-keywords-generator.py --input "strategic thinker"
    # Output: Alternatives like "business outcome architect", "future-state planner"

    python scripts/brand-keywords-generator.py --role cio
    # Output: CIO-specific brand keywords and combinations
"""

import argparse
import sys
from typing import Dict, List, Tuple


# Brand language database: generic -> distinctive alternatives
BRAND_TRANSFORMATIONS = {
    # Strategic descriptors
    "strategic thinker": [
        "business outcome architect",
        "future-state planner",
        "strategic roadmap curator",
        "long-term value creator"
    ],
    "strategic": [
        "outcome-focused",
        "future-oriented",
        "value-driving",
        "transformation-minded"
    ],
    "strategic leader": [
        "transformation catalyst",
        "strategic direction setter",
        "value-creation leader",
        "business outcome driver"
    ],

    # Communication descriptors
    "good communicator": [
        "technical translator",
        "executive storyteller",
        "cross-functional bridge builder",
        "message clarity champion"
    ],
    "communicator": [
        "storyteller",
        "translator",
        "message architect",
        "narrative builder"
    ],

    # Collaboration descriptors
    "team player": [
        "cross-functional catalyst",
        "collaboration multiplier",
        "partnership builder",
        "alliance strategist"
    ],
    "collaborative": [
        "partnership-driven",
        "alliance-building",
        "integration-focused",
        "bridge-building"
    ],

    # Execution descriptors
    "results-oriented": [
        "bias-to-action leader",
        "outcome-obsessed",
        "delivery-focused",
        "impact-driven executor"
    ],
    "gets things done": [
        "execution champion",
        "delivery accelerator",
        "results multiplier",
        "completion catalyst"
    ],

    # Innovation descriptors
    "innovative": [
        "experimentation champion",
        "innovation catalyst",
        "breakthrough creator",
        "disruption enabler"
    ],
    "creative": [
        "solution architect",
        "novel approach designer",
        "perspective synthesizer",
        "pattern innovator"
    ],

    # Technical descriptors
    "technical expert": [
        "architecture simplification advocate",
        "technical excellence driver",
        "engineering quality champion",
        "systems thinking practitioner"
    ],
    "technical": [
        "engineering-excellence",
        "architecture-minded",
        "systems-thinking",
        "quality-driven"
    ],

    # Customer descriptors
    "customer-focused": [
        "customer obsession champion",
        "user experience advocate",
        "customer journey optimizer",
        "value delivery accelerator"
    ],

    # Quality descriptors
    "detail-oriented": [
        "quality systems architect",
        "precision advocate",
        "excellence enforcer",
        "standards champion"
    ],

    # Leadership descriptors
    "leader": [
        "catalyst",
        "multiplier",
        "architect",
        "champion"
    ],
    "manager": [
        "orchestrator",
        "enabler",
        "coach",
        "developer"
    ]
}


# Role-specific brand keyword suggestions
ROLE_SPECIFIC_KEYWORDS = {
    "cio": {
        "distinctive_approaches": [
            "Digital transformation",
            "Business-technology partnership",
            "Platform thinking",
            "Data-driven decision",
            "Innovation portfolio",
            "Technical debt elimination",
            "Developer experience",
            "Security-by-design"
        ],
        "value_delivered": [
            "catalyst",
            "enabler",
            "co-creator",
            "strategist",
            "advocate",
            "champion",
            "architect",
            "evangelist"
        ],
        "examples": [
            "Digital transformation catalyst",
            "Business-technology partner",
            "Innovation portfolio curator",
            "Technical debt eliminator",
            "Platform thinking evangelist"
        ]
    },
    "cto": {
        "distinctive_approaches": [
            "Platform architecture",
            "Engineering excellence",
            "Technical vision",
            "Architecture simplification",
            "Developer productivity",
            "Technical standards",
            "Innovation acceleration"
        ],
        "value_delivered": [
            "architect",
            "champion",
            "practitioner",
            "advocate",
            "driver",
            "enabler",
            "multiplier"
        ],
        "examples": [
            "Platform thinking architect",
            "Engineering excellence champion",
            "Architecture simplification advocate",
            "Developer productivity multiplier"
        ]
    },
    "product": {
        "distinctive_approaches": [
            "Customer journey",
            "Experimentation-driven",
            "Outcome obsession",
            "Product-market fit",
            "User experience",
            "Data-informed decision",
            "Strategic roadmap"
        ],
        "value_delivered": [
            "optimizer",
            "champion",
            "architect",
            "evangelist",
            "maker",
            "hunter",
            "storyteller"
        ],
        "examples": [
            "Customer journey optimizer",
            "Experimentation evangelist",
            "Outcome obsession leader",
            "Product-market fit architect"
        ]
    },
    "engineering": {
        "distinctive_approaches": [
            "Developer experience",
            "Engineering velocity",
            "Code quality",
            "Technical mentorship",
            "Architecture clarity",
            "Operational excellence"
        ],
        "value_delivered": [
            "champion",
            "multiplier",
            "architect",
            "advocate",
            "driver",
            "enabler"
        ],
        "examples": [
            "Developer experience champion",
            "Engineering velocity multiplier",
            "Technical mentorship advocate",
            "Architecture clarity driver"
        ]
    }
}


def find_alternatives(input_text: str) -> List[str]:
    """Find distinctive alternatives for generic brand language."""
    input_lower = input_text.lower().strip()

    # Direct match
    if input_lower in BRAND_TRANSFORMATIONS:
        return BRAND_TRANSFORMATIONS[input_lower]

    # Partial match
    alternatives = []
    for generic, distinctive in BRAND_TRANSFORMATIONS.items():
        if generic in input_lower or input_lower in generic:
            alternatives.extend(distinctive)

    # Remove duplicates while preserving order
    seen = set()
    return [x for x in alternatives if not (x in seen or seen.add(x))]


def test_distinctiveness(brand_text: str) -> Tuple[int, List[str]]:
    """
    Test how distinctive brand language is.

    Returns:
        (score, suggestions) where score is 1-5:
        5 = highly distinctive
        1 = very generic
    """
    score = 5
    suggestions = []

    # Check for generic words
    generic_indicators = [
        "good", "great", "excellent", "skilled", "talented",
        "team player", "strategic", "innovative", "results-oriented",
        "dependable", "reliable", "experienced"
    ]

    for indicator in generic_indicators:
        if indicator in brand_text.lower():
            score -= 1
            suggestions.append(f"'{indicator}' is generic - consider more specific language")

    # Check for vague qualifiers
    vague_qualifiers = ["very", "highly", "extremely", "quite"]
    for qualifier in vague_qualifiers:
        if qualifier in brand_text.lower():
            score -= 0.5
            suggestions.append(f"Remove vague qualifier '{qualifier}'")

    # Check for role descriptors
    role_descriptors = ["leader", "manager", "executive", "professional"]
    for descriptor in role_descriptors:
        if brand_text.lower().endswith(descriptor):
            score -= 1
            suggestions.append(f"Ending with '{descriptor}' is generic")

    score = max(1, min(5, int(score)))

    return score, suggestions


def generate_combinations(role: str) -> List[str]:
    """Generate brand promise combinations for a role."""
    if role.lower() not in ROLE_SPECIFIC_KEYWORDS:
        return []

    role_data = ROLE_SPECIFIC_KEYWORDS[role.lower()]
    combinations = []

    for approach in role_data["distinctive_approaches"]:
        for value in role_data["value_delivered"]:
            combinations.append(f"{approach} {value}")

    return combinations


def generate_report(
    input_text: str = None,
    role: str = None,
    test_mode: bool = False
) -> str:
    """Generate markdown report with brand keyword suggestions."""
    report = ["# Brand Keywords Generator Report", ""]

    if input_text:
        report.extend([
            "## Input Analysis",
            "",
            f"**Input:** {input_text}",
            ""
        ])

        # Find alternatives
        alternatives = find_alternatives(input_text)

        if alternatives:
            report.extend([
                "### Distinctive Alternatives",
                "",
                "Consider these more distinctive alternatives:",
                ""
            ])
            for alt in alternatives:
                report.append(f"- **{alt}**")
        else:
            report.extend([
                "### No Direct Alternatives Found",
                "",
                "Your language may already be distinctive, or we don't have",
                "alternatives for this specific phrase.",
                ""
            ])

        # Test distinctiveness
        if test_mode:
            score, suggestions = test_distinctiveness(input_text)
            report.extend([
                "",
                "### Distinctiveness Test",
                "",
                f"**Distinctiveness Score:** {score} / 5",
                ""
            ])

            if score >= 4:
                report.append("✅ This language is distinctive!")
            elif score == 3:
                report.append("⚠️ This language could be more distinctive.")
            else:
                report.append("❌ This language is too generic.")

            if suggestions:
                report.extend(["", "**Suggestions:**", ""])
                for suggestion in suggestions:
                    report.append(f"- {suggestion}")

    if role:
        role_lower = role.lower()

        if role_lower in ROLE_SPECIFIC_KEYWORDS:
            role_data = ROLE_SPECIFIC_KEYWORDS[role_lower]

            report.extend([
                "",
                f"## {role.upper()} Brand Keywords",
                "",
                "### Distinctive Approaches",
                ""
            ])

            for approach in role_data["distinctive_approaches"]:
                report.append(f"- {approach}")

            report.extend([
                "",
                "### Value Descriptors",
                ""
            ])

            for value in role_data["value_delivered"]:
                report.append(f"- {value}")

            report.extend([
                "",
                "### Example Brand Promises",
                ""
            ])

            for example in role_data["examples"]:
                report.append(f"- **{example}**")

            # Generate some combinations
            report.extend([
                "",
                "### Additional Combinations",
                "",
                "Here are some other combinations to consider:",
                ""
            ])

            combinations = generate_combinations(role)
            for combo in combinations[:15]:  # Limit to 15
                report.append(f"- {combo}")

        else:
            report.extend([
                "",
                f"## Role '{role}' Not Found",
                "",
                "Available roles:",
                ""
            ])
            for available_role in ROLE_SPECIFIC_KEYWORDS.keys():
                report.append(f"- {available_role}")

    report.extend([
        "",
        "---",
        "",
        "## Tips for Distinctive Brand Language",
        "",
        "1. **Be specific, not generic** - 'Digital transformation catalyst' > 'Strategic leader'",
        "2. **Use action words** - 'Architect', 'Champion', 'Multiplier' > 'Manager', 'Leader'",
        "3. **Communicate value** - What does your market receive or experience?",
        "4. **Avoid vague qualifiers** - Remove 'very', 'highly', 'extremely'",
        "5. **Focus on distinction** - What makes YOU unique, not just good?",
        "",
        "---",
        "",
        "*Generated by brand-keywords-generator.py*"
    ])

    return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(
        description="Generate distinctive brand keywords and test brand language"
    )
    parser.add_argument(
        "--input",
        type=str,
        help="Generic brand language to transform"
    )
    parser.add_argument(
        "--role",
        type=str,
        choices=list(ROLE_SPECIFIC_KEYWORDS.keys()),
        help="Generate role-specific brand keywords"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Test distinctiveness of input language"
    )
    parser.add_argument(
        "--list-roles",
        action="store_true",
        help="List available roles"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output markdown file (default: print to stdout)"
    )

    args = parser.parse_args()

    if args.list_roles:
        print("Available roles:")
        for role in ROLE_SPECIFIC_KEYWORDS.keys():
            print(f"  - {role}")
        sys.exit(0)

    if not args.input and not args.role:
        parser.print_help()
        print("\nError: Provide --input and/or --role", file=sys.stderr)
        sys.exit(1)

    # Generate report
    report = generate_report(
        input_text=args.input,
        role=args.role,
        test_mode=args.test
    )

    # Output
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"Report written to {args.output}", file=sys.stderr)
    else:
        print(report)


if __name__ == "__main__":
    main()
