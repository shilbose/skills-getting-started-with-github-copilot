#!/usr/bin/env python3
"""
4-Gram Extraction CLI Tool

A command-line tool to extract 4-grams from sentences.
Can be used standalone or imported as a module.
"""

import sys
import argparse
import json
import re
from typing import List, Dict

def clean_text(text: str) -> str:
    """Clean and normalize text for processing."""
    # Convert to lowercase
    text = text.lower()
    # Remove punctuation except spaces and apostrophes
    text = re.sub(r'[^\w\s\']', ' ', text)
    # Replace multiple spaces with single space
    text = re.sub(r'\s+', ' ', text)
    # Strip leading/trailing whitespace
    return text.strip()

def extract_fourgrams(sentence: str) -> List[str]:
    """
    Extract all 4-grams from a given sentence.
    
    Args:
        sentence (str): Input sentence
        
    Returns:
        List[str]: List of 4-grams found in the sentence
    """
    if not sentence or not sentence.strip():
        return []
    
    # Clean the text
    cleaned_text = clean_text(sentence)
    
    # Split into words
    words = cleaned_text.split()
    
    # If we have fewer than 4 words, no 4-grams possible
    if len(words) < 4:
        return []
    
    # Extract 4-grams
    fourgrams = []
    for i in range(len(words) - 3):
        fourgram = ' '.join(words[i:i+4])
        fourgrams.append(fourgram)
    
    return fourgrams

def get_fourgram_stats(sentence: str) -> Dict:
    """
    Get detailed statistics about 4-grams in the sentence.
    
    Args:
        sentence (str): Input sentence
        
    Returns:
        Dict: Statistics including count, unique count, and frequency
    """
    fourgrams = extract_fourgrams(sentence)
    
    # Count frequency of each 4-gram
    frequency = {}
    for fg in fourgrams:
        frequency[fg] = frequency.get(fg, 0) + 1
    
    return {
        "original_sentence": sentence,
        "cleaned_sentence": clean_text(sentence),
        "word_count": len(clean_text(sentence).split()),
        "fourgrams": fourgrams,
        "total_fourgrams": len(fourgrams),
        "unique_fourgrams": len(set(fourgrams)),
        "frequency": frequency
    }

def print_results(stats: Dict, format_type: str = "text"):
    """Print results in the specified format."""
    if format_type == "json":
        print(json.dumps(stats, indent=2))
        return
    
    # Text format
    print(f"\n📝 Original sentence: {stats['original_sentence']}")
    print(f"🧹 Cleaned sentence: {stats['cleaned_sentence']}")
    print(f"📊 Word count: {stats['word_count']}")
    print(f"🔢 Total 4-grams: {stats['total_fourgrams']}")
    print(f"🎯 Unique 4-grams: {stats['unique_fourgrams']}")
    
    if stats['fourgrams']:
        print(f"\n🔍 4-Grams found:")
        for i, fourgram in enumerate(stats['fourgrams'], 1):
            print(f"  {i:2d}. {fourgram}")
        
        # Show frequency analysis if there are duplicates
        duplicates = {k: v for k, v in stats['frequency'].items() if v > 1}
        if duplicates:
            print(f"\n📈 Frequency analysis (repeated 4-grams):")
            for fourgram, count in sorted(duplicates.items(), key=lambda x: x[1], reverse=True):
                print(f"  '{fourgram}' appears {count} times")
    else:
        print(f"\n❌ No 4-grams found. The sentence needs at least 4 words.")

def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Extract 4-grams from sentences",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python fourgram_cli.py "The quick brown fox jumps over the lazy dog"
  python fourgram_cli.py -f json "Natural language processing is fascinating"
  echo "Machine learning is amazing" | python fourgram_cli.py --stdin
  python fourgram_cli.py --interactive
        """
    )
    
    parser.add_argument(
        'sentence', 
        nargs='?', 
        help='Input sentence to extract 4-grams from'
    )
    
    parser.add_argument(
        '-f', '--format',
        choices=['text', 'json'],
        default='text',
        help='Output format (default: text)'
    )
    
    parser.add_argument(
        '--stdin',
        action='store_true',
        help='Read sentence from stdin'
    )
    
    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='Interactive mode - keep asking for sentences'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='4-Gram Extraction CLI v1.0.0'
    )
    
    args = parser.parse_args()
    
    # Interactive mode
    if args.interactive:
        print("🎯 4-Gram Extraction Tool - Interactive Mode")
        print("Enter sentences to extract 4-grams (Ctrl+C to exit)\n")
        
        try:
            while True:
                sentence = input("Enter sentence: ").strip()
                if not sentence:
                    continue
                
                stats = get_fourgram_stats(sentence)
                print_results(stats, args.format)
                print("-" * 50)
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            sys.exit(0)
    
    # Read from stdin
    elif args.stdin:
        sentence = sys.stdin.read().strip()
        if not sentence:
            print("Error: No input received from stdin", file=sys.stderr)
            sys.exit(1)
        
        stats = get_fourgram_stats(sentence)
        print_results(stats, args.format)
    
    # Use provided sentence
    elif args.sentence:
        stats = get_fourgram_stats(args.sentence)
        print_results(stats, args.format)
    
    # No input provided
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()