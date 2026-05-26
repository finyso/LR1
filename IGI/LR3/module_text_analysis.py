"""
Module for text analysis
Laboratory Work No. 3, Task 4 - Variant 24
Developer: Pavel Finsky
Date: 2026-03-21
"""

import re
from typing import List, Dict, Tuple, Optional, Any
from collections import Counter
from functools import wraps


class TextAnalyzer:
    """Class for analyzing text with specific conditions (Variant 24)"""
    
    def __init__(self):
        self.text: str = ""
        self.words: List[str] = []
    
    def set_text(self, text: str) -> None:
        """Set text for analysis"""
        self.text = text
        # Split text into words (by spaces and commas)
        self.words = [word.strip() for word in re.split(r'[ ,]+', text) if word.strip()]
    
    def count_short_words(self, max_length: int = 7) -> int:
        """
        Count words with length less than max_length
        
        Args:
            max_length: maximum length for counting
            
        Returns:
            number of words with length < max_length
        """
        return sum(1 for word in self.words if len(word) < max_length)
    
    def find_shortest_word_ending_with(self, letter: str = 'a') -> Optional[str]:
        """
        Find the shortest word ending with specified letter
        
        Args:
            letter: letter to check at word end
            
        Returns:
            shortest word ending with letter, or None if not found
        """
        letter = letter.lower()
        matching_words = [word for word in self.words 
                         if word.lower().endswith(letter)]
        
        if not matching_words:
            return None
        
        return min(matching_words, key=len)
    
    def sort_words_by_length(self, descending: bool = True) -> List[str]:
        """
        Sort words by length
        
        Args:
            descending: if True, sort descending; if False, ascending
            
        Returns:
            sorted list of words
        """
        return sorted(self.words, key=len, reverse=descending)
    
    def task4_main(self) -> None:
        """
        Main function for Task 4 - Variant 24 conditions:
        a) count words with length < 7
        b) find shortest word ending with 'a'
        c) display all words in descending order of length
        """
        print("\n" + "=" * 60)
        print("TASK 4: Text Analysis")
        print("Variant 24 Conditions:")
        print("a) Count words with length less than 7")
        print("b) Find shortest word ending with 'a'")
        print("c) Display all words in descending order of length")
        print("=" * 60)
        
        default_text = (
            "So she was considering in her own mind, as well as she could, "
            "for the hot day made her feel very sleepy and stupid, whether "
            "the pleasure of making a daisy-chain would be worth the trouble "
            "of getting up and picking the daisies, when suddenly a White Rabbit "
            "with pink eyes ran close by her."
        )
        
        while True:
            try:
                print("\nDefault text for analysis:")
                print("-" * 40)
                print(default_text)
                print("-" * 40)
                
                use_default = input("Use default text? (y/n): ").strip().lower()
                
                if use_default in ['y', 'yes']:
                    self.set_text(default_text)
                else:
                    text = input("Enter your own text: ").strip()
                    if not text:
                        print("Text cannot be empty")
                        continue
                    self.set_text(text)
                
                print("\n" + "-" * 50)
                print("TEXT ANALYSIS RESULTS")
                print("-" * 50)
                
                print(f"\nOriginal text: {self.text[:200]}..." if len(self.text) > 200 else f"\nOriginal text: {self.text}")
                print(f"Total words: {len(self.words)}")
                
                # Condition a
                short_words_count = self.count_short_words(7)
                print(f"\na) Words with length < 7: {short_words_count}")
                short_words = [w for w in self.words if len(w) < 7]
                if short_words:
                    print(f"   These words: {short_words[:20]}" if len(short_words) > 20 else f"   These words: {short_words}")
                
                # Condition b
                shortest_word_a = self.find_shortest_word_ending_with('a')
                print(f"\nb) Shortest word ending with 'a': {shortest_word_a if shortest_word_a else 'Not found'}")
                
                # Condition c
                sorted_words = self.sort_words_by_length(descending=True)
                print(f"\nc) Words sorted by length (descending):")
                for i, word in enumerate(sorted_words[:30], 1):
                    print(f"   {i:2}. {word} ({len(word)} letters)")
                if len(sorted_words) > 30:
                    print(f"   ... and {len(sorted_words) - 30} more words")
                    
                print("-" * 50)
                
            except Exception as e:
                print(f"Unexpected Error: {e}")
            
            while True:
                repeat = input("\nDo you want to analyze another text? (y/n): ").strip().lower()
                if repeat in ['y', 'yes']:
                    break
                elif repeat in ['n', 'no']:
                    return
                else:
                    print("Please enter 'y' or 'n'")