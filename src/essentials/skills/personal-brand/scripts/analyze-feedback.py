#!/usr/bin/env python3
"""
Analyze Feedback - Extract themes from performance reviews and feedback documents

This script processes text files containing performance reviews, 360-degree feedback,
or brand discovery conversation notes to extract common themes and patterns.

Usage:
    python scripts/analyze-feedback.py feedback.txt
    python scripts/analyze-feedback.py reviews/*.txt --output themes.md

Features:
- Word frequency analysis
- N-gram (phrase) extraction
- Sentiment categorization (positive/developmental/neutral)
- Theme clustering
- Markdown output for integration with worksheets

Requirements:
    pip install nltk
"""

import argparse
import sys
from collections import Counter
from pathlib import Path
from typing import Dict, List, Tuple

try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import sent_tokenize, word_tokenize
    from nltk.util import ngrams
except ImportError:
    print("Error: nltk library required. Install with: pip install nltk")
    sys.exit(1)


def download_nltk_data():
    """Download required NLTK data if not present."""
    try:
        nltk.data.find("tokenizers/punkt")
        nltk.data.find("corpora/stopwords")
    except LookupError:
        print("Downloading required NLTK data...")
        nltk.download("punkt", quiet=True)
        nltk.download("stopwords", quiet=True)


def load_feedback_files(file_paths: List[Path]) -> str:
    """Load and combine text from multiple feedback files."""
    combined_text = []

    for file_path in file_paths:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
                combined_text.append(f"--- From {file_path.name} ---\n{text}\n")
        except Exception as e:
            print(f"Warning: Could not read {file_path}: {e}", file=sys.stderr)

    return "\n".join(combined_text)


def extract_keywords(text: str, top_n: int = 20) -> List[Tuple[str, int]]:
    """Extract most common keywords, excluding stopwords."""
    # Tokenize and clean
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words("english"))

    # Add domain-specific stopwords
    custom_stop_words = {
        "could",
        "would",
        "one",
        "two",
        "also",
        "well",
        "make",
        "get",
        "like",
        "really",
        "think",
        "see",
        "know",
        "good",
        "better",
    }
    stop_words.update(custom_stop_words)

    # Filter tokens
    keywords = [
        token
        for token in tokens
        if token.isalpha() and len(token) > 3 and token not in stop_words
    ]

    # Count and return top N
    counter = Counter(keywords)
    return counter.most_common(top_n)


def extract_phrases(text: str, n: int = 2, top_n: int = 15) -> List[Tuple[str, int]]:
    """Extract common n-grams (phrases)."""
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words("english"))

    # Filter tokens
    filtered_tokens = [
        token for token in tokens if token.isalpha() and token not in stop_words
    ]

    # Generate n-grams
    n_grams = ngrams(filtered_tokens, n)
    phrase_list = [" ".join(gram) for gram in n_grams]

    # Count and return top N
    counter = Counter(phrase_list)
    return counter.most_common(top_n)


def categorize_sentiment(text: str) -> Dict[str, List[str]]:
    """
    Categorize sentences by sentiment (positive, developmental, neutral).

    This is a simple heuristic-based approach. For production, consider using
    a proper sentiment analysis library.
    """
    sentences = sent_tokenize(text)

    # Sentiment indicators
    positive_words = {
        "excellent",
        "strong",
        "outstanding",
        "effective",
        "successful",
        "great",
        "impressive",
        "exceptional",
        "skilled",
        "talented",
        "proactive",
        "innovative",
        "strategic",
        "collaborative",
        "leader",
    }

    developmental_words = {
        "improve",
        "develop",
        "opportunity",
        "challenge",
        "struggle",
        "difficulty",
        "could",
        "should",
        "need",
        "work on",
        "gap",
        "weakness",
        "concern",
        "issue",
        "problem",
        "inconsistent",
    }

    categorized = {"positive": [], "developmental": [], "neutral": []}

    for sentence in sentences:
        sentence_lower = sentence.lower()

        # Count sentiment indicators
        positive_count = sum(1 for word in positive_words if word in sentence_lower)
        developmental_count = sum(
            1 for word in developmental_words if word in sentence_lower
        )

        # Categorize
        if positive_count > developmental_count:
            categorized["positive"].append(sentence.strip())
        elif developmental_count > positive_count:
            categorized["developmental"].append(sentence.strip())
        else:
            categorized["neutral"].append(sentence.strip())

    return categorized


def generate_markdown_report(
    file_paths: List[Path],
    keywords: List[Tuple[str, int]],
    bigrams: List[Tuple[str, int]],
    trigrams: List[Tuple[str, int]],
    sentiment: Dict[str, List[str]],
) -> str:
    """Generate markdown report from analysis."""

    report = [
        "# Feedback Analysis Report",
        "",
        f"**Analysis Date:** {Path(__file__).stat().st_mtime}",
        f"**Files Analyzed:** {len(file_paths)}",
        "",
        "## Files Included",
        "",
    ]

    for file_path in file_paths:
        report.append(f"- `{file_path.name}`")

    report.extend(
        [
            "",
            "---",
            "",
            "## Top Keywords",
            "",
            "Most frequently mentioned words (excluding common stopwords):",
            "",
            "| Rank | Keyword | Frequency |",
            "|------|---------|-----------|",
        ]
    )

    for idx, (keyword, count) in enumerate(keywords, 1):
        report.append(f"| {idx} | **{keyword}** | {count} |")

    report.extend(
        [
            "",
            "---",
            "",
            "## Common Phrases",
            "",
            "### Two-Word Phrases (Bigrams)",
            "",
            "| Rank | Phrase | Frequency |",
            "|------|--------|-----------|",
        ]
    )

    for idx, (phrase, count) in enumerate(bigrams, 1):
        report.append(f"| {idx} | {phrase} | {count} |")

    report.extend(
        [
            "",
            "### Three-Word Phrases (Trigrams)",
            "",
            "| Rank | Phrase | Frequency |",
            "|------|--------|-----------|",
        ]
    )

    for idx, (phrase, count) in enumerate(trigrams, 1):
        report.append(f"| {idx} | {phrase} | {count} |")

    report.extend(
        [
            "",
            "---",
            "",
            "## Sentiment Analysis",
            "",
            "### Positive Feedback Themes",
            "",
            f"Found {len(sentiment['positive'])} positive statements.",
            "",
        ]
    )

    for sentence in sentiment["positive"][:10]:  # Top 10
        report.append(f"- {sentence}")

    report.extend(
        [
            "",
            "### Developmental Areas",
            "",
            f"Found {len(sentiment['developmental'])} developmental statements.",
            "",
        ]
    )

    for sentence in sentiment["developmental"][:10]:  # Top 10
        report.append(f"- {sentence}")

    report.extend(
        [
            "",
            "---",
            "",
            "## Suggested Next Steps",
            "",
            "Based on this analysis:",
            "",
            "1. **Review top keywords** - Do these reflect your intended brand?",
            "2. **Analyze common phrases** - What themes emerge from repeated phrases?",
            "3. **Examine sentiment distribution** - What's the balance of positive vs. developmental feedback?",
            "4. **Identify patterns** - Look for themes that appear across multiple files",
            "5. **Update brand discovery synthesis** - Incorporate these findings",
            "",
            "---",
            "",
            "*Generated by analyze-feedback.py*",
        ]
    )

    return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(
        description="Analyze feedback text files to extract themes and patterns"
    )
    parser.add_argument(
        "files", nargs="+", type=Path, help="Feedback text files to analyze"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output markdown file (default: print to stdout)",
    )
    parser.add_argument(
        "--top-keywords",
        type=int,
        default=20,
        help="Number of top keywords to extract (default: 20)",
    )
    parser.add_argument(
        "--top-phrases",
        type=int,
        default=15,
        help="Number of top phrases to extract (default: 15)",
    )

    args = parser.parse_args()

    # Download NLTK data if needed
    download_nltk_data()

    # Validate files
    file_paths = []
    for file_path in args.files:
        if file_path.exists() and file_path.is_file():
            file_paths.append(file_path)
        else:
            print(
                f"Warning: {file_path} does not exist or is not a file", file=sys.stderr
            )

    if not file_paths:
        print("Error: No valid files to analyze", file=sys.stderr)
        sys.exit(1)

    # Load feedback
    print(f"Analyzing {len(file_paths)} file(s)...", file=sys.stderr)
    text = load_feedback_files(file_paths)

    # Extract insights
    print("Extracting keywords...", file=sys.stderr)
    keywords = extract_keywords(text, args.top_keywords)

    print("Extracting phrases...", file=sys.stderr)
    bigrams = extract_phrases(text, n=2, top_n=args.top_phrases)
    trigrams = extract_phrases(text, n=3, top_n=args.top_phrases)

    print("Analyzing sentiment...", file=sys.stderr)
    sentiment = categorize_sentiment(text)

    # Generate report
    print("Generating report...", file=sys.stderr)
    report = generate_markdown_report(
        file_paths, keywords, bigrams, trigrams, sentiment
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
