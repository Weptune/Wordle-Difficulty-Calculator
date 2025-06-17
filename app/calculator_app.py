import os
import pandas as pd

# Automatically resolve the path to the data file
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'final_difficulty_scores.csv')

# Load the full difficulty score table
try:
    df = pd.read_csv(DATA_PATH)
    df["Word"] = df["Word"].str.upper()
except FileNotFoundError:
    print("❌ Error: final_difficulty_scores.csv not found.")
    exit(1)

def lookup_difficulty(word: str) -> dict:
    word = word.strip().upper()
    match = df[df["Word"] == word]
    if match.empty:
        return None
    return match.iloc[0].to_dict()

if __name__ == "__main__":
    word = input("🔤 Enter a 5-letter Wordle word: ").strip()
    if len(word) != 5 or not word.isalpha():
        print("❌ Please enter a valid 5-letter alphabetical word.")
    else:
        result = lookup_difficulty(word)
        if not result:
            print("❌ Word not found in difficulty database.")
        else:
            print("\n📊 Difficulty Analysis:")
            for key, value in result.items():
                if key == "Word":
                    print(f"{key:>18}: {value}")
                else:
                    print(f"{key:>18}: {round(value, 3) if isinstance(value, float) else value}")