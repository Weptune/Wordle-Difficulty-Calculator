import os
from collections import Counter

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data')

with open(os.path.join(DATA_PATH, 'words.txt'), 'r') as f:
    WORD_LIST = [w.strip().upper() for w in f if len(w.strip()) == 5]

STARTERS = ["STARE", "CRANE", "SLATE", "AUDIO", "RAISE", "TRACE", "ARISE", "CARTE", "SALET", "REACT"]

def get_feedback(solution, guess):
    feedback = ['B'] * 5
    s_count = Counter(solution)

    for i in range(5):
        if guess[i] == solution[i]:
            feedback[i] = 'G'
            s_count[guess[i]] -= 1

    for i in range(5):
        if feedback[i] == 'B' and s_count[guess[i]] > 0:
            feedback[i] = 'Y'
            s_count[guess[i]] -= 1

    return ''.join(feedback)

def matches(word, guess, feedback):
    return get_feedback(word, guess) == feedback

def compute_true_wsa(word: str, wordlist=WORD_LIST, starters=STARTERS) -> float:
    word = word.upper()
    match_counts = []

    for starter in starters:
        fb = get_feedback(word, starter)
        remaining = sum(1 for w in wordlist if matches(w, starter, fb))
        match_counts.append(remaining)

    avg_remaining = sum(match_counts) / len(match_counts)
    return round(avg_remaining, 3)
