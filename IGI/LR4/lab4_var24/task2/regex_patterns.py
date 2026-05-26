"""
Lab 4, Task 2, Variant 24
Regex patterns and common text analysis tasks.
Developer: Finsky Pavel
Date: 30.04.2026
Version: 1.0
"""
import re

# Individual task patterns
def find_lowercase_words_and_punctuation(text: str) -> list:
    """Finds all words starting with a lowercase letter and all punctuation marks."""
    pattern = r'\b[a-z][a-zA-Z]*\b|[.,!?;:()\[\]{}"\'\\/]'
    return re.findall(pattern, text)

def is_valid_mac(text: str) -> bool:
    """Checks if a string is a valid MAC address."""
    pattern = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
    return bool(re.match(pattern, text))

# General text analysis tasks
def count_sentences(text: str) -> int:
    """Counts sentences in the text."""
    return len(re.findall(r'[.!?]+', text))

def count_sentence_types(text: str) -> dict:
    """Counts declarative, interrogative, and exclamatory sentences."""
    declarative = len(re.findall(r'(?<![.!?])\b[^.!?]*\.', text))
    interrogative = len(re.findall(r'(?<![.!?])\b[^.!?]*\?', text))
    exclamatory = len(re.findall(r'(?<![.!?])\b[^.!?]*!', text))
    return {"declarative": declarative, "interrogative": interrogative, "exclamatory": exclamatory}

def average_sentence_length(text: str) -> float:
    """Calculates average sentence length in characters (words only)."""
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    if not sentences: return 0
    word_counts = [len(re.findall(r'\b\w+\b', s)) for s in sentences]
    return sum(word_counts) / len(sentences)

def average_word_length(text: str) -> float:
    """Calculates average word length in characters."""
    words = re.findall(r'\b\w+\b', text)
    if not words: return 0
    return sum(len(w) for w in words) / len(words)

def count_smileys(text: str) -> int:
    """Counts smileys based on the given definition."""
    pattern = r'[;:]-*[\(\)\[\]]+'
    smileys = re.findall(pattern, text)
    valid_smileys = []
    for s in smileys:
        # The last part must consist of identical brackets
        if re.match(r'[;:]-*(\(+\)+|\)+\(+|\[+\]+|\]+\[+)', s): continue
        if re.match(r'[;:]-*([\(\)\[\]])\1*$', s):
            valid_smileys.append(s)
    return len(valid_smileys)