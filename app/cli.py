import argparse
from app.calculator import calculate_difficulty

parser = argparse.ArgumentParser(description="Wordle Difficulty Calculator")
parser.add_argument("word", type=str, help="A 5-letter word to evaluate")

args = parser.parse_args()
result = calculate_difficulty(args.word)

print("\n📊 Difficulty Analysis:")
for k, v in result.items():
    print(f"{k:>16}: {v}")
