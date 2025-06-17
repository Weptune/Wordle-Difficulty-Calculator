# features/wordle_logic.py

from collections import Counter

def get_feedback(solution: str, guess: str) -> str:
    """
    Returns Wordle-style feedback string: 'G', 'Y', or 'B' for each letter.
    """
    solution = solution.upper()
    guess = guess.upper()
    feedback = ["B"] * 5
    counter = Counter(solution)

    # Green pass
    for i in range(5):
        if guess[i] == solution[i]:
            feedback[i] = "G"
            counter[guess[i]] -= 1

    # Yellow pass
    for i in range(5):
        if feedback[i] == "B" and counter[guess[i]] > 0:
            feedback[i] = "Y"
            counter[guess[i]] -= 1

    return "".join(feedback)

def matches(candidate: str, guess: str, feedback: str) -> bool:
    return get_feedback(candidate, guess) == feedback
