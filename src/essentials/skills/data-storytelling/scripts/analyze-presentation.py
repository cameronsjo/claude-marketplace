#!/usr/bin/env python3
"""
Analyze Executive Presentation

Analyzes a presentation deck for common issues:
- Bullet count per slide
- Jargon and acronym usage
- Readability metrics
- Slide structure compliance

Usage:
    python scripts/analyze-presentation.py presentation.pptx
    python scripts/analyze-presentation.py presentation.pptx --verbose
    python scripts/analyze-presentation.py presentation.pptx --output report.md

Example:
    python scripts/analyze-presentation.py Executive_Q2_Review.pptx
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple


def analyze_text_complexity(text: str) -> Dict[str, any]:
    """Analyze text for readability and complexity."""
    words = text.split()
    sentences = re.split(r'[.!?]+', text)

    # Count syllables (simplified)
    def count_syllables(word: str) -> int:
        word = word.lower()
        count = 0
        vowels = 'aeiouy'
        prev_was_vowel = False
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not prev_was_vowel:
                count += 1
            prev_was_vowel = is_vowel
        # Adjust for silent e
        if word.endswith('e'):
            count -= 1
        return max(1, count)

    syllable_count = sum(count_syllables(word) for word in words)

    # Flesch Reading Ease (higher = easier to read)
    # 90-100: Very easy (5th grade)
    # 60-70: Standard (8th-9th grade)
    # 30-50: Difficult (college)
    # 0-30: Very difficult (college graduate)
    if len(sentences) > 0 and len(words) > 0:
        avg_sentence_length = len(words) / len(sentences)
        avg_syllables_per_word = syllable_count / len(words)
        flesch_score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
        flesch_score = max(0, min(100, flesch_score))
    else:
        flesch_score = 100

    return {
        'word_count': len(words),
        'sentence_count': len(sentences),
        'syllable_count': syllable_count,
        'avg_words_per_sentence': len(words) / max(1, len(sentences)),
        'avg_syllables_per_word': syllable_count / max(1, len(words)),
        'flesch_reading_ease': flesch_score,
    }


def find_acronyms(text: str) -> List[str]:
    """Find potential acronyms (2+ consecutive capital letters)."""
    # Find words with 2+ consecutive capitals
    acronym_pattern = r'\b[A-Z]{2,}\b'
    acronyms = re.findall(acronym_pattern, text)

    # Filter out common words and roman numerals
    common_words = {'US', 'USA', 'UK', 'CEO', 'CFO', 'CTO', 'CIO', 'COO', 'VP', 'SVP', 'EVP', 'Q1', 'Q2', 'Q3', 'Q4'}
    roman_numerals = {'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X'}

    filtered = [a for a in acronyms if a not in common_words and a not in roman_numerals]
    return list(set(filtered))


def find_jargon(text: str) -> List[str]:
    """Find potential jargon terms (common business/tech jargon)."""
    jargon_terms = [
        # Business jargon
        'synergy', 'leverage', 'paradigm', 'bandwidth', 'circle back',
        'low-hanging fruit', 'move the needle', 'drill down', 'take offline',
        'touch base', 'run it up the flagpole', 'boil the ocean',

        # Tech jargon
        'kubernetes', 'microservices', 'serverless', 'containerization',
        'CI/CD', 'API gateway', 'event-driven', 'lambda', 'docker',

        # Metrics jargon
        'MAU', 'DAU', 'CSAT', 'NPS', 'ARR', 'MRR', 'LTV', 'CAC', 'MQL', 'SQL',
        'TTM', 'EBITDA', 'KPI', 'OKR', 'SLA', 'SLO',
    ]

    text_lower = text.lower()
    found = []
    for term in jargon_terms:
        if term.lower() in text_lower:
            found.append(term)

    return found


def count_bullets(text: str) -> int:
    """Count bullet points in text."""
    # Common bullet indicators
    bullet_pattern = r'^[\s]*[•\-\*\◦\▪\–]'
    lines = text.split('\n')
    bullet_count = sum(1 for line in lines if re.match(bullet_pattern, line))
    return bullet_count


def analyze_presentation_text(presentation_path: Path) -> Dict:
    """
    Analyze a presentation file.

    This is a simplified version that works with plain text.
    For PowerPoint files, you would use python-pptx library.
    """
    # For demo purposes, this reads text files
    # In production, use python-pptx for .pptx files

    if not presentation_path.exists():
        raise FileNotFoundError(f"Presentation not found: {presentation_path}")

    # Read text (for .txt or .md files)
    if presentation_path.suffix in ['.txt', '.md']:
        content = presentation_path.read_text()
    else:
        print(f"Note: For .pptx files, install python-pptx library")
        print(f"Treating {presentation_path.name} as text file for demo")
        try:
            content = presentation_path.read_text()
        except Exception as e:
            print(f"Error reading file: {e}")
            sys.exit(1)

    # Split into slides (assuming blank lines separate slides)
    slides = content.split('\n\n\n')

    results = {
        'total_slides': len(slides),
        'slides': [],
        'overall': {
            'total_words': 0,
            'total_bullets': 0,
            'all_acronyms': set(),
            'all_jargon': set(),
        },
        'issues': [],
    }

    for i, slide_text in enumerate(slides, 1):
        if not slide_text.strip():
            continue

        complexity = analyze_text_complexity(slide_text)
        acronyms = find_acronyms(slide_text)
        jargon = find_jargon(slide_text)
        bullets = count_bullets(slide_text)

        slide_analysis = {
            'slide_number': i,
            'word_count': complexity['word_count'],
            'bullet_count': bullets,
            'acronyms': acronyms,
            'jargon': jargon,
            'readability': complexity['flesch_reading_ease'],
            'preview': slide_text[:100].replace('\n', ' '),
        }

        results['slides'].append(slide_analysis)
        results['overall']['total_words'] += complexity['word_count']
        results['overall']['total_bullets'] += bullets
        results['overall']['all_acronyms'].update(acronyms)
        results['overall']['all_jargon'].update(jargon)

        # Check for issues
        if bullets > 5:
            results['issues'].append(f"Slide {i}: Too many bullets ({bullets}). Limit to 3-5.")

        if complexity['word_count'] > 100:
            results['issues'].append(f"Slide {i}: Too many words ({complexity['word_count']}). Keep under 75.")

        if complexity['flesch_reading_ease'] < 50:
            results['issues'].append(f"Slide {i}: Low readability score ({complexity['flesch_reading_ease']:.0f}). Simplify language.")

        if len(acronyms) > 3:
            results['issues'].append(f"Slide {i}: Many acronyms ({len(acronyms)}). Define or eliminate: {', '.join(acronyms)}")

    return results


def generate_report(results: Dict, verbose: bool = False) -> str:
    """Generate a markdown report of analysis results."""
    report = []
    report.append("# Executive Presentation Analysis Report\n")

    # Summary
    report.append("## Summary\n")
    report.append(f"- **Total Slides:** {results['total_slides']}")
    report.append(f"- **Total Words:** {results['overall']['total_words']}")
    report.append(f"- **Average Words per Slide:** {results['overall']['total_words'] / max(1, results['total_slides']):.0f}")
    report.append(f"- **Total Bullet Points:** {results['overall']['total_bullets']}")
    report.append(f"- **Unique Acronyms Found:** {len(results['overall']['all_acronyms'])}")
    report.append(f"- **Jargon Terms Found:** {len(results['overall']['all_jargon'])}\n")

    # Issues
    if results['issues']:
        report.append("## Issues Found\n")
        report.append(f"**{len(results['issues'])} issues detected:**\n")
        for issue in results['issues']:
            report.append(f"- ⚠️  {issue}")
        report.append("")
    else:
        report.append("## Issues Found\n")
        report.append("✅ No major issues detected!\n")

    # Acronyms
    if results['overall']['all_acronyms']:
        report.append("## Acronyms to Define or Eliminate\n")
        for acronym in sorted(results['overall']['all_acronyms']):
            report.append(f"- {acronym}")
        report.append("")

    # Jargon
    if results['overall']['all_jargon']:
        report.append("## Jargon to Review\n")
        for term in sorted(results['overall']['all_jargon']):
            report.append(f"- {term}")
        report.append("")

    # Slide-by-slide (if verbose)
    if verbose:
        report.append("## Slide-by-Slide Analysis\n")
        for slide in results['slides']:
            report.append(f"### Slide {slide['slide_number']}\n")
            report.append(f"- **Words:** {slide['word_count']}")
            report.append(f"- **Bullets:** {slide['bullet_count']}")
            report.append(f"- **Readability:** {slide['readability']:.0f} (Flesch Reading Ease)")

            if slide['acronyms']:
                report.append(f"- **Acronyms:** {', '.join(slide['acronyms'])}")

            if slide['jargon']:
                report.append(f"- **Jargon:** {', '.join(slide['jargon'])}")

            report.append(f"- **Preview:** {slide['preview']}...")
            report.append("")

    # Recommendations
    report.append("## Recommendations\n")

    avg_words = results['overall']['total_words'] / max(1, results['total_slides'])
    if avg_words > 75:
        report.append(f"- 📝 **Reduce word count**: Average {avg_words:.0f} words per slide. Target 50-75 words.")

    if results['overall']['total_bullets'] / max(1, results['total_slides']) > 5:
        report.append(f"- 🔢 **Reduce bullets**: Average {results['overall']['total_bullets'] / results['total_slides']:.1f} bullets per slide. Target 3-5 maximum.")

    if len(results['overall']['all_acronyms']) > 5:
        report.append(f"- 🔤 **Define acronyms**: {len(results['overall']['all_acronyms'])} unique acronyms found. Define on first use or eliminate.")

    if len(results['overall']['all_jargon']) > 0:
        report.append(f"- 💬 **Simplify language**: {len(results['overall']['all_jargon'])} jargon terms found. Use plain language for executive audience.")

    report.append("\n---\n")
    report.append("*Analysis powered by Executive Data Storytelling skill*")

    return '\n'.join(report)


def main():
    parser = argparse.ArgumentParser(
        description="Analyze executive presentation for common issues",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python analyze-presentation.py deck.pptx
    python analyze-presentation.py deck.pptx --verbose
    python analyze-presentation.py deck.pptx --output report.md
        """
    )

    parser.add_argument(
        'presentation',
        type=Path,
        help='Path to presentation file (.pptx, .txt, or .md)'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Include slide-by-slide analysis in report'
    )

    parser.add_argument(
        '--output', '-o',
        type=Path,
        help='Save report to file (markdown format)'
    )

    args = parser.parse_args()

    # Analyze presentation
    print(f"Analyzing presentation: {args.presentation.name}")
    print()

    try:
        results = analyze_presentation_text(args.presentation)
        report = generate_report(results, verbose=args.verbose)

        # Output report
        if args.output:
            args.output.write_text(report)
            print(f"Report saved to: {args.output}")
            print()

        print(report)

        # Exit code based on issues
        if results['issues']:
            sys.exit(1)
        else:
            sys.exit(0)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == '__main__':
    main()
