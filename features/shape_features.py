from collections import Counter

def get_feedback(solution: str, guess: str) -> str:
    """Return Wordle-style feedback string for a guess (G, Y, B)."""
    feedback = ["B"] * 5
    sc = Counter(solution)
    for i in range(5):
        if guess[i] == solution[i]:
            feedback[i] = "G"
            sc[guess[i]] -= 1
    for i in range(5):
        if feedback[i] == "B" and sc[guess[i]] > 0:
            feedback[i] = "Y"
            sc[guess[i]] -= 1
    return "".join(feedback)

def matches(word: str, guess: str, feedback: str) -> bool:
    return get_feedback(word, guess) == feedback

def compute_shape_features(word: str, all_words: list, starter_words: list) -> dict:
    total_elim = 0
    match_reduction = 0
    greens, yellows, grays = 0, 0, 0

    for guess in starter_words:
        fb = get_feedback(word, guess)
        remaining = [w for w in all_words if matches(w, guess, fb)]
        total_elim += len(all_words) - len(remaining)
        match_reduction += len(all_words) / max(1, len(remaining))

        greens += fb.count("G")
        yellows += fb.count("Y")
        grays += fb.count("B")

    n = len(starter_words)
    return {
        "MatchReduction": round(match_reduction / n, 3),
        "AvgElimination": round(total_elim / n, 3),
        "FeedbackGreen": round(greens / (5 * n), 3),
        "FeedbackYellow": round(yellows / (5 * n), 3),
        "FeedbackGray": round(grays / (5 * n), 3),
    }
