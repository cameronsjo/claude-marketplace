#!/usr/bin/env python3
"""
Communication Style Diagnostic Tool

Interactive tool to assess communication styles based on the Social Styles Framework.
Helps identify your own style and diagnose others' styles through behavioral observations.

Usage:
    python scripts/style-diagnostic.py [--self | --other | --stakeholder-analysis]

Examples:
    python scripts/style-diagnostic.py --self
    python scripts/style-diagnostic.py --other
    python scripts/style-diagnostic.py --stakeholder-analysis
"""

import argparse
import sys
from typing import Dict, List, Tuple


class StyleDiagnostic:
    """Communication style diagnostic tool based on Social Styles Framework."""

    STYLES = {
        "AMIABLE": {
            "focus": "People",
            "orientation": "Relationship + Ask",
            "tagline": "Let me discuss this with my team",
            "seeks": "Consensus",
            "decision": "Slow and thoughtful",
            "saves": "Relationships",
            "questions": "Why",
            "stress": "Acquiesce",
        },
        "EXPRESSIVE": {
            "focus": "Ideas",
            "orientation": "Relationship + Tell",
            "tagline": "Here are my ideas about this",
            "seeks": "Recognition",
            "decision": "Fast and spontaneous",
            "saves": "Effort",
            "questions": "Who",
            "stress": "Attack",
        },
        "ANALYTIC": {
            "focus": "Process",
            "orientation": "Task + Ask",
            "tagline": "Let me think how it could work",
            "seeks": "Accuracy",
            "decision": "Slow and systematic",
            "saves": "Face",
            "questions": "How",
            "stress": "Avoid",
        },
        "DRIVER": {
            "focus": "Results",
            "orientation": "Task + Tell",
            "tagline": "Let's take action on this",
            "seeks": "Results",
            "decision": "Decisive and results-focused",
            "saves": "Time",
            "questions": "What",
            "stress": "Autocracy",
        },
    }

    def __init__(self):
        self.scores = {"AMIABLE": 0, "EXPRESSIVE": 0, "ANALYTIC": 0, "DRIVER": 0}

    def print_header(self, title: str) -> None:
        """Print formatted section header."""
        print("\n" + "=" * 70)
        print(f"  {title}")
        print("=" * 70 + "\n")

    def print_framework(self) -> None:
        """Print the Social Styles Framework visual."""
        print("""
                      RELATIONSHIP
                           ↑
                AMIABLE  |  EXPRESSIVE
           (People)      |      (Ideas)
      ASK ←────────────────────────────→ TELL
           (Process)     |     (Results)
                ANALYTIC |    DRIVER
                           ↓
                         TASK
        """)

    def ask_question(
        self, question: str, options: Dict[str, str], instruction: str = ""
    ) -> str:
        """Ask a multiple choice question and return the selected key."""
        print(f"\n{question}")
        if instruction:
            print(f"({instruction})")
        print()

        keys = list(options.keys())
        for i, (key, text) in enumerate(options.items(), 1):
            print(f"{i}. {text}")

        while True:
            try:
                choice = input("\nYour answer (1-{}): ".format(len(keys))).strip()
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(keys):
                    return keys[choice_idx]
                print(f"Please enter a number between 1 and {len(keys)}")
            except (ValueError, KeyboardInterrupt):
                print("\nExiting...")
                sys.exit(0)

    def self_assessment(self) -> None:
        """Run self-assessment questionnaire."""
        self.print_header("Communication Style Self-Assessment")

        print("""
This assessment will help you identify your natural communication style.
Answer based on your DEFAULT preferences (how you naturally act, especially under stress).
There are no right or wrong answers.
        """)

        input("Press Enter to begin...")

        questions = [
            {
                "question": "In meetings, I typically:",
                "options": {
                    "AMIABLE": "Make sure everyone's voice is heard and comfortable",
                    "EXPRESSIVE": "Share ideas and stories enthusiastically",
                    "ANALYTIC": "Ask detailed questions and analyze information",
                    "DRIVER": "Drive toward decisions and action items",
                },
            },
            {
                "question": "When making decisions, I prioritize:",
                "options": {
                    "AMIABLE": "Impact on people and relationships",
                    "EXPRESSIVE": "Excitement and recognition potential",
                    "ANALYTIC": "Accuracy and risk mitigation",
                    "DRIVER": "Results and speed of execution",
                },
            },
            {
                "question": "Under stress, I tend to:",
                "options": {
                    "AMIABLE": "Avoid conflict and agree to keep peace",
                    "EXPRESSIVE": "Become defensive and critical",
                    "ANALYTIC": "Delay decisions and over-analyze",
                    "DRIVER": "Take charge and push harder",
                },
            },
            {
                "question": "In emails, I typically:",
                "options": {
                    "AMIABLE": "Start with personal connection and ask for input",
                    "EXPRESSIVE": "Share exciting ideas and stories",
                    "ANALYTIC": "Provide detailed data and documentation",
                    "DRIVER": "Get straight to the point and action needed",
                },
            },
            {
                "question": "What I want to save most in interactions:",
                "options": {
                    "AMIABLE": "Relationships and harmony",
                    "EXPRESSIVE": "Effort and make things exciting",
                    "ANALYTIC": "Face and avoid being wrong",
                    "DRIVER": "Time and achieve results",
                },
            },
            {
                "question": "My typical reaction to new proposals:",
                "options": {
                    "AMIABLE": "How will this affect the team?",
                    "EXPRESSIVE": "What exciting possibilities does this create?",
                    "ANALYTIC": "What's the data supporting this?",
                    "DRIVER": "What's the bottom-line impact?",
                },
            },
            {
                "question": "In presentations, I prefer to:",
                "options": {
                    "AMIABLE": "Build consensus and ensure everyone's comfortable",
                    "EXPRESSIVE": "Tell compelling stories and create excitement",
                    "ANALYTIC": "Present detailed analysis and methodology",
                    "DRIVER": "Show results and get to decisions quickly",
                },
            },
            {
                "question": "My tagline would be:",
                "options": {
                    "AMIABLE": "Let me discuss this with my team",
                    "EXPRESSIVE": "Here are my ideas about this",
                    "ANALYTIC": "Let me think how it could work",
                    "DRIVER": "Let's take action on this",
                },
            },
        ]

        for i, q in enumerate(questions, 1):
            answer = self.ask_question(
                f"Question {i}/{len(questions)}: {q['question']}",
                q["options"],
                "Choose the option that feels most natural to you",
            )
            self.scores[answer] += 1

        self.display_results(self.scores, is_self=True)

    def other_assessment(self) -> None:
        """Run assessment for diagnosing someone else's style."""
        self.print_header("Assess Someone Else's Communication Style")

        print("""
This tool helps you diagnose someone else's communication style.
Answer based on THEIR observed behaviors.
        """)

        person_name = input(
            "What's the person's name (or role)? "
        ).strip() or "This person"

        print(f"\nThinking about {person_name}...")
        input("Press Enter to begin...")

        # First: Quick diagnostic
        print("\n" + "-" * 70)
        print("QUICK DIAGNOSTIC (20-second method)")
        print("-" * 70)

        dimension1 = self.ask_question(
            f"When {person_name} communicates, they prioritize:",
            {
                "RELATIONSHIP": "Relationships, people, team impact, consensus",
                "TASK": "Tasks, results, data, outcomes",
            },
        )

        dimension2 = self.ask_question(
            f"When {person_name} communicates, they typically:",
            {
                "ASK": "Ask questions, seek input, more reserved",
                "TELL": "Make statements, give opinions, more assertive",
            },
        )

        # Determine style from dimensions
        quick_style = self._determine_style_from_dimensions(dimension1, dimension2)

        print(f"\nBased on quick diagnostic: {person_name} appears to be {quick_style}")
        print(
            f"({self.STYLES[quick_style]['orientation']} - {self.STYLES[quick_style]['focus']}-focused)"
        )

        # Now: Detailed behavioral observations
        print("\n" + "-" * 70)
        print("BEHAVIORAL OBSERVATIONS (for confirmation)")
        print("-" * 70)

        observations = [
            {
                "question": f"In meetings, {person_name} typically:",
                "options": {
                    "AMIABLE": "Starts with 'How is everyone?' and seeks team input",
                    "EXPRESSIVE": "Shares stories, ideas, and speaks with enthusiasm",
                    "ANALYTIC": "Asks detailed questions and takes methodical notes",
                    "DRIVER": "Gets straight to agenda and drives toward decisions",
                },
            },
            {
                "question": f"When making decisions, {person_name}:",
                "options": {
                    "AMIABLE": "Takes time to build consensus and get team buy-in",
                    "EXPRESSIVE": "Makes quick, spontaneous decisions based on excitement",
                    "ANALYTIC": "Systematically analyzes data before deciding",
                    "DRIVER": "Makes fast, decisive calls focused on results",
                },
            },
            {
                "question": f"{person_name}'s emails are typically:",
                "options": {
                    "AMIABLE": "Warm, personal, asking for opinions and input",
                    "EXPRESSIVE": "Enthusiastic, story-driven, lots of exclamation points",
                    "ANALYTIC": "Detailed, data-heavy, precise and thorough",
                    "DRIVER": "Brief, direct, focused on action and decisions",
                },
            },
            {
                "question": f"When stressed, {person_name} tends to:",
                "options": {
                    "AMIABLE": "Agree to things but not commit (acquiesce)",
                    "EXPRESSIVE": "Become defensive and critical (attack)",
                    "ANALYTIC": "Delay decisions and avoid confrontation (avoid)",
                    "DRIVER": "Become dictatorial and pushy (autocracy)",
                },
            },
            {
                "question": f"{person_name} seems most interested in:",
                "options": {
                    "AMIABLE": "Human connection and team relationships",
                    "EXPRESSIVE": "Ideas, possibilities, and recognition",
                    "ANALYTIC": "Facts, data, and accuracy",
                    "DRIVER": "Action, outcomes, and results",
                },
            },
        ]

        for obs in observations:
            answer = self.ask_question(obs["question"], obs["options"])
            self.scores[answer] += 1

        self.display_results(self.scores, is_self=False, person_name=person_name)

    def _determine_style_from_dimensions(
        self, dimension1: str, dimension2: str
    ) -> str:
        """Determine style from two dimensions."""
        if dimension1 == "RELATIONSHIP" and dimension2 == "ASK":
            return "AMIABLE"
        elif dimension1 == "RELATIONSHIP" and dimension2 == "TELL":
            return "EXPRESSIVE"
        elif dimension1 == "TASK" and dimension2 == "ASK":
            return "ANALYTIC"
        else:  # TASK + TELL
            return "DRIVER"

    def display_results(
        self, scores: Dict[str, int], is_self: bool = True, person_name: str = "They"
    ) -> None:
        """Display assessment results with interpretation."""
        self.print_header("Results")

        # Calculate primary and secondary styles
        sorted_styles = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        primary_style = sorted_styles[0][0]
        primary_score = sorted_styles[0][1]
        secondary_style = sorted_styles[1][0] if len(sorted_styles) > 1 else None
        secondary_score = sorted_styles[1][1] if len(sorted_styles) > 1 else 0

        # Display scores
        print("Scores:")
        for style, score in sorted_styles:
            bar = "█" * (score * 5)
            print(f"  {style:12} {bar} ({score})")

        # Display primary style
        print(f"\n{'YOUR' if is_self else person_name.upper()} PRIMARY STYLE: {primary_style}")
        print("-" * 70)

        style_info = self.STYLES[primary_style]
        print(f"Focus:           {style_info['focus']}")
        print(f"Orientation:     {style_info['orientation']}")
        print(f"Tagline:         '{style_info['tagline']}'")
        print(f"Seeks:           {style_info['seeks']}")
        print(f"Decision style:  {style_info['decision']}")
        print(f"Wants to save:   {style_info['saves']}")
        print(f"Asks about:      {style_info['questions']}")
        print(f"Stress response: {style_info['stress']}")

        # Show secondary if close
        if secondary_score > 0 and (primary_score - secondary_score) <= 2:
            print(f"\nSECONDARY INFLUENCE: {secondary_style}")
            print(
                f"You {'show' if is_self else person_name + ' shows'} traits of {secondary_style} as well."
            )
            print(
                f"This suggests flexibility between {primary_style} and {secondary_style} styles."
            )

        # Provide guidance
        self.print_header("Recommendations")

        if is_self:
            self._provide_self_recommendations(
                primary_style, secondary_style if secondary_score > 2 else None
            )
        else:
            self._provide_engagement_recommendations(primary_style, person_name)

    def _provide_self_recommendations(
        self, primary_style: str, secondary_style: str = None
    ) -> None:
        """Provide recommendations based on self-assessment."""
        print(f"As a {primary_style}, you naturally excel at:")

        strengths = {
            "AMIABLE": [
                "Building strong relationships and trust",
                "Creating collaborative environments",
                "Ensuring team buy-in and consensus",
                "Maintaining harmony in groups",
            ],
            "EXPRESSIVE": [
                "Generating creative ideas and possibilities",
                "Building enthusiasm and energy",
                "Storytelling and emotional connection",
                "Inspiring and motivating others",
            ],
            "ANALYTIC": [
                "Detailed analysis and accuracy",
                "Risk identification and mitigation",
                "Systematic problem-solving",
                "Data-driven decision making",
            ],
            "DRIVER": [
                "Getting results efficiently",
                "Making decisive calls",
                "Driving action and accountability",
                "Cutting through complexity",
            ],
        }

        for strength in strengths[primary_style]:
            print(f"  • {strength}")

        print(f"\nTo flex your style more effectively, practice:")

        # Opposite style to practice
        opposite = {
            "AMIABLE": "DRIVER",
            "DRIVER": "AMIABLE",
            "EXPRESSIVE": "ANALYTIC",
            "ANALYTIC": "EXPRESSIVE",
        }

        flex_target = opposite[primary_style]

        flex_practices = {
            "AMIABLE": [
                "Make decisions with clear deadlines (DRIVER flex)",
                "State opinions directly rather than asking (DRIVER flex)",
                "Focus on results over relationships when needed (DRIVER flex)",
            ],
            "EXPRESSIVE": [
                "Back ideas with data and evidence (ANALYTIC flex)",
                "Slow down for systematic analysis (ANALYTIC flex)",
                "Focus on accuracy over excitement (ANALYTIC flex)",
            ],
            "ANALYTIC": [
                "Tell compelling stories to make data relatable (EXPRESSIVE flex)",
                "Make decisions with incomplete data (EXPRESSIVE flex)",
                "Show enthusiasm and emotion (EXPRESSIVE flex)",
            ],
            "DRIVER": [
                "Build relationships before diving into business (AMIABLE flex)",
                "Seek input and consensus (AMIABLE flex)",
                "Give others time to process (AMIABLE flex)",
            ],
        }

        for practice in flex_practices[primary_style]:
            print(f"  • {practice}")

        print(f"\nWhen communicating with {flex_target}s (your opposite style):")
        print(f"  • They may frustrate you most")
        print(f"  • But they bring complementary strengths")
        print(f"  • Practice flexing to their style intentionally")

    def _provide_engagement_recommendations(
        self, primary_style: str, person_name: str
    ) -> None:
        """Provide recommendations for engaging with someone."""
        print(f"To effectively engage with {person_name} ({primary_style}):\n")

        recommendations = {
            "AMIABLE": {
                "DO": [
                    "Connect personally before business",
                    "Ask for their opinions and genuinely listen",
                    "Talk about team impact and holistic concepts",
                    "Give them time to build consensus",
                    "Be warm, supportive, and collaborative",
                ],
                "DONT": [
                    "Rush into business without personal connection",
                    "Be domineering or pushy",
                    "Force quick decisions",
                    "Ignore their team's concerns",
                ],
                "POWER_WORDS": "guarantee, reliable, tested, safety, together, team, support",
                "OPENER": "How are you and your team doing?",
                "CLOSER": "Does this feel right to you and your team?",
            },
            "EXPRESSIVE": {
                "DO": [
                    "Provide warm, friendly environment",
                    "Tell specific stories that evoke emotions",
                    "Use visual, engaging presentations",
                    "Recognize their contributions and ideas",
                    "Make it exciting and innovative",
                ],
                "DONT": [
                    "Be curt, cold, or tight-lipped",
                    "Control the conversation",
                    "Drown them in detailed minutiae",
                    "Be boring or overly formal",
                ],
                "POWER_WORDS": "innovative, exciting, creative, recognize, appreciate, revolutionary",
                "OPENER": "I'm excited to share this with you!",
                "CLOSER": "What ideas do you have to make this even better?",
            },
            "ANALYTIC": {
                "DO": [
                    "Prepare your case with data in advance",
                    "Be accurate, realistic, and precise",
                    "Use detailed models and documentation",
                    "Stick to business",
                    "Give them time to analyze thoroughly",
                ],
                "DONT": [
                    "Be casual, informal, or loud",
                    "Push too hard for quick deadlines",
                    "Be disorganized or messy",
                    "Make claims without evidence",
                ],
                "POWER_WORDS": "research, data, evidence, proven, systematic, methodology, analysis",
                "OPENER": "I've analyzed the data and here's what I found...",
                "CLOSER": "I'll send you the detailed documentation to review.",
            },
            "DRIVER": {
                "DO": [
                    "Be clear, specific, brief, and to the point",
                    "Stick to business",
                    "Use concrete, proven examples",
                    "Focus on results and ROI",
                    "Respect their time above all",
                ],
                "DONT": [
                    "Go off topic or ramble",
                    "Appear disorganized",
                    "Miss deadlines or be late",
                    "Waste time with unnecessary details",
                ],
                "POWER_WORDS": "ROI, results, fast, efficiency, win, best, powerful, first",
                "OPENER": "Bottom line: this will save us $500K.",
                "CLOSER": "What's your decision?",
            },
        }

        rec = recommendations[primary_style]

        print("DO:")
        for item in rec["DO"]:
            print(f"  ✓ {item}")

        print("\nDON'T:")
        for item in rec["DONT"]:
            print(f"  ✗ {item}")

        print(f"\nPOWER WORDS TO USE:")
        print(f"  {rec['POWER_WORDS']}")

        print(f"\nEMAIL/MEETING OPENERS:")
        print(f"  '{rec['OPENER']}'")

        print(f"\nCLOSING STATEMENTS:")
        print(f"  '{rec['CLOSER']}'")

    def stakeholder_analysis(self) -> None:
        """Create stakeholder communication plan."""
        self.print_header("Stakeholder Communication Analysis")

        print("""
This tool helps you create a communication plan for multiple stakeholders
with different communication styles.
        """)

        stakeholders = []

        while True:
            name = input(
                "\nEnter stakeholder name (or press Enter if done): "
            ).strip()
            if not name:
                break

            print(f"\nQuick style diagnostic for {name}:")

            dimension1 = self.ask_question(
                f"{name} prioritizes:",
                {
                    "RELATIONSHIP": "Relationships, people, team",
                    "TASK": "Tasks, results, outcomes",
                },
            )

            dimension2 = self.ask_question(
                f"{name} typically:",
                {
                    "ASK": "Asks questions, seeks input",
                    "TELL": "Makes statements, gives opinions",
                },
            )

            style = self._determine_style_from_dimensions(dimension1, dimension2)

            role = input(f"What's {name}'s role? (optional): ").strip()

            stakeholders.append({"name": name, "role": role, "style": style})

            print(f"✓ Added {name} as {style}")

        if not stakeholders:
            print("\nNo stakeholders added. Exiting.")
            return

        self._generate_communication_plan(stakeholders)

    def _generate_communication_plan(
        self, stakeholders: List[Dict[str, str]]
    ) -> None:
        """Generate communication plan for stakeholders."""
        self.print_header("Communication Plan")

        # Summary
        print("STAKEHOLDER SUMMARY:")
        print(f"{'Name':<20} {'Role':<25} {'Style':<12}")
        print("-" * 60)
        for s in stakeholders:
            print(f"{s['name']:<20} {s['role']:<25} {s['style']:<12}")

        # Style distribution
        print("\nSTYLE DISTRIBUTION:")
        style_counts = {}
        for s in stakeholders:
            style_counts[s["style"]] = style_counts.get(s["style"], 0) + 1

        for style, count in sorted(style_counts.items()):
            bar = "█" * (count * 3)
            print(f"  {style:12} {bar} ({count})")

        # Identify conflicts
        print("\nPOTENTIAL STYLE CONFLICTS:")
        opposites = {
            "AMIABLE": "DRIVER",
            "DRIVER": "AMIABLE",
            "EXPRESSIVE": "ANALYTIC",
            "ANALYTIC": "EXPRESSIVE",
        }

        conflicts_found = False
        for s1 in stakeholders:
            opposite = opposites[s1["style"]]
            for s2 in stakeholders:
                if s2["style"] == opposite and s1["name"] < s2["name"]:
                    conflicts_found = True
                    print(
                        f"  ⚠️  {s1['name']} ({s1['style']}) ↔ {s2['name']} ({s2['style']})"
                    )
                    print(
                        f"     These are opposite styles and may create maximum tension"
                    )

        if not conflicts_found:
            print("  No major style conflicts detected!")

        # Communication recommendations
        self.print_header("Communication Strategy")

        print("INDIVIDUAL ENGAGEMENT PLANS:\n")

        for s in stakeholders:
            print(f"{s['name']} ({s['style']}):")

            if s["style"] == "AMIABLE":
                print("  • Start with personal connection")
                print("  • Ask for their team's input")
                print("  • Give time for consensus building")
                print("  • Use: 'guarantee, reliable, tested'")
            elif s["style"] == "EXPRESSIVE":
                print("  • Share exciting vision and stories")
                print("  • Recognize their ideas publicly")
                print("  • Make it visually engaging")
                print("  • Use: 'innovative, exciting, creative'")
            elif s["style"] == "ANALYTIC":
                print("  • Provide detailed documentation in advance")
                print("  • Be precise and data-driven")
                print("  • Give time to analyze thoroughly")
                print("  • Use: 'research, data, proven'")
            elif s["style"] == "DRIVER":
                print("  • Lead with bottom-line results")
                print("  • Be brief and action-focused")
                print("  • Respect their time")
                print("  • Use: 'ROI, results, fast'")

            print()

        # Group presentation strategy
        print("GROUP PRESENTATION STRATEGY:")
        print("\nUse 4-layer structure to address all styles:")
        print("  1. DRIVER Layer (15 sec): Bottom line, decision needed, key results")
        print("  2. EXPRESSIVE Layer (30 sec): Story, vision, why it matters")
        print("  3. ANALYTIC Layer (2 min): Data, methodology, risk assessment")
        print("  4. AMIABLE Layer (1 min): Team impact, consensus approach")

        # Deliverables by style
        print("\nDELIVERABLES TO PREPARE:")
        if any(s["style"] == "DRIVER" for s in stakeholders):
            print("  • One-pager with executive summary and ROI")
        if any(s["style"] == "EXPRESSIVE" for s in stakeholders):
            print("  • Visual presentation with stories and vision")
        if any(s["style"] == "ANALYTIC" for s in stakeholders):
            print("  • Detailed documentation with data and methodology")
        if any(s["style"] == "AMIABLE" for s in stakeholders):
            print("  • Change management plan showing team involvement")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Communication Style Diagnostic Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --self                    Run self-assessment
  %(prog)s --other                   Assess someone else
  %(prog)s --stakeholder-analysis    Analyze multiple stakeholders
        """,
    )

    parser.add_argument(
        "--self", action="store_true", help="Run self-assessment questionnaire"
    )
    parser.add_argument(
        "--other", action="store_true", help="Assess someone else's style"
    )
    parser.add_argument(
        "--stakeholder-analysis",
        action="store_true",
        help="Create stakeholder communication plan",
    )

    args = parser.parse_args()

    diagnostic = StyleDiagnostic()

    # If no args, show menu
    if not (args.self or args.other or args.stakeholder_analysis):
        diagnostic.print_header("Communication Style Diagnostic Tool")
        diagnostic.print_framework()

        print("What would you like to do?\n")
        print("1. Self-assessment (identify your communication style)")
        print("2. Assess someone else (diagnose another person's style)")
        print("3. Stakeholder analysis (plan communication for multiple people)")
        print("4. Exit")

        while True:
            try:
                choice = input("\nYour choice (1-4): ").strip()
                if choice == "1":
                    diagnostic.self_assessment()
                    break
                elif choice == "2":
                    diagnostic.other_assessment()
                    break
                elif choice == "3":
                    diagnostic.stakeholder_analysis()
                    break
                elif choice == "4":
                    print("Goodbye!")
                    sys.exit(0)
                else:
                    print("Please enter 1, 2, 3, or 4")
            except KeyboardInterrupt:
                print("\nExiting...")
                sys.exit(0)
    else:
        if args.self:
            diagnostic.self_assessment()
        elif args.other:
            diagnostic.other_assessment()
        elif args.stakeholder_analysis:
            diagnostic.stakeholder_analysis()


if __name__ == "__main__":
    main()
