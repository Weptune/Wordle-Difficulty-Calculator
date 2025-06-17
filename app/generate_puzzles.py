import random
import json
from collections import Counter

# Load word list from final_difficulty_scores.csv
with open("data/final_difficulty_scores.csv") as f:
    rows = [line.strip().split(",") for line in f.readlines()]
    header = rows[0]
    all_rows = rows[1:]
    word_list = [row[0].lower() for row in all_rows if len(row[0]) == 5]
    word_os = {row[0].lower(): float(row[6]) for row in all_rows if len(row) > 6 and row[6]}

# Use full dictionary from CSV (not actual_words.txt)
dictionary = set(word_list)

# Optional: load actual_words just to help diversify guesses
with open("data/actual_words.txt") as f:
    actual_words = [w.strip().lower() for w in f if len(w.strip()) == 5]

# Debug: Show some low OS words
low_os_words = [w for w in word_list if word_os.get(w, 1.0) < 0.5]
print(f"Words with OS < 0.5: {len(low_os_words)}")
print("Examples:", low_os_words[:10])

# Candidate puzzle solutions
candidate_solutions = [w for w in word_list if word_os.get(w, 1.0) < 0.9]
print(f"Candidate solutions (OS < 0.9): {len(candidate_solutions)}")

# Wordle feedback simulation
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

STARTERS = ["slate", "crane", "stare", "arise", "trace", "reast", "glint", "blame", "pride"]

puzzles = []
random.shuffle(candidate_solutions)

for target in candidate_solutions:
    used = set()
    guesses = []
    attempts = 0

    while len(guesses) < 4 and attempts < 100:
        guess = random.choice(STARTERS + actual_words)
        if guess in used or guess == target:
            attempts += 1
            continue
        fb = get_feedback(target, guess)
        guesses.append([guess, fb])
        used.add(guess)
        attempts += 1

    guesses.append([target, "GGGGG"])

    # Check if it's a uniquely solvable path
    compatible = [w for w in dictionary if all(matches(w, g, f) for g, f in guesses)]
    if len(compatible) == 1:
        puzzles.append({"solution": target, "guesses": guesses})

    if len(puzzles) >= 200:
        break

# Save to file
with open("data/grid_puzzles.json", "w") as f:
    json.dump(puzzles, f, indent=2)

print(f"✅ Generated {len(puzzles)} unique puzzles.")
