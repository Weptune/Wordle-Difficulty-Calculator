import os
import sys
import tkinter as tk
from tkinter import messagebox
import pandas as pd
import webbrowser
from scipy.stats import percentileofscore
from random import choice, sample
import re
from tkinter import ttk

# ---------- Resource Path for PyInstaller bundling ---------- #
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# ---------- Load Datasets ---------- #
DATA_PATH = resource_path(os.path.join("data", "final_difficulty_scores.csv"))
WORDS_PATH = resource_path(os.path.join("data", "actual_words.txt"))
MORPH_PATH = resource_path(os.path.join("data", "morph_pairs.json"))

df = pd.read_csv(DATA_PATH)
df['Word'] = df['Word'].str.lower()

with open(WORDS_PATH, 'r') as f:
    text = f.read().lower()
    actual_word_list = re.findall(r"\b[a-z]{5}\b", text)

word_data = {
    row['Word']: {
        "LFS": row["LFS"],
        "PLFS": row["PLFS"],
        "RLP": row["RLP"],
        "HLT": row["HLT"],
        "WSA": row["WSA"],
        "OS": row["OS"],
        "ODS": row["ODS"],
        "ExpectedGuesses": row["ExpectedGuesses"]
    }
    for _, row in df.iterrows()
}

actual_ods_scores = [
    word_data[w]["ODS"] for w in actual_word_list if w in word_data
]

# ---------- Tkinter GUI Setup ---------- #
root = tk.Tk()
root.title("Wordle Difficulty Calculator")
root.geometry("900x900")
root.minsize(700, 700)
root.configure(bg="#1e272e")
root.resizable(True, True)

notebook = ttk.Notebook(root)
# Centering tabs: wrap the notebook in a frame with stretch space
tab_wrapper = tk.Frame(root, bg="#1e272e")
tab_wrapper.pack(fill='x')

left_spacer = tk.Frame(tab_wrapper, width=100, bg="#1e272e")
left_spacer.pack(side="left", fill='y')

notebook = ttk.Notebook(tab_wrapper)
notebook.pack(side="left", expand=False)

right_spacer = tk.Frame(tab_wrapper, width=100, bg="#1e272e")
right_spacer.pack(side="left", fill='y')


style = ttk.Style()
style.theme_use('default')
style.configure('TNotebook', background="#1e272e", borderwidth=0)
style.configure('TNotebook.Tab', background="#34495e", foreground="white", padding=(10, 5))
style.map("TNotebook.Tab", background=[("selected", "#2ecc71")])

# ---------- GitHub Link Widget ---------- #
def add_github_link(parent):
    github_url = "https://github.com/Weptune/Wordle-Difficulty-Calculator"
    github_frame = tk.Frame(parent, bg="#1e272e")
    github_frame.pack(pady=5)
    github_label = tk.Label(github_frame, text="🔗 View on GitHub", font=("Segoe UI", 11, "underline"),
                             fg="#3498db", bg="#1e272e", cursor="hand2")
    github_label.pack()
    github_label.bind("<Button-1>", lambda e: webbrowser.open_new(github_url))

# ---------- Fonts ---------- #
FONT_TITLE = ("Segoe UI", 22, "bold")
FONT_LABEL = ("Segoe UI", 12)
FONT_MONO = ("Courier New", 11)
FONT_GUESS = ("Segoe UI", 18, "bold")

# ---------- Tab 1: Difficulty Checker ---------- #
difficulty_tab = tk.Frame(notebook, bg="#1e272e")
notebook.add(difficulty_tab, text="🔍 Difficulty Checker")

FACTOR_DESCRIPTIONS = {
    "LFS": "Letter Frequency Score - Commonness of letters.",
    "PLFS": "Positional Letter Frequency Score - Frequency of letters in specific positions.",
    "RLP": "Repeated Letter Penalty - Penalizes repeated letters.",
    "HLT": "Hard Letter Transitions - Difficulty based on uncommon bigrams.",
    "WSA": "Word Structure Advantage - Estimated value as an opener.",
    "OS": "Obscurity Score - How uncommon the word is.",
    "ODS": "Overall Difficulty Score - Weighted combo of all factors.",
    "ExpectedGuesses": "Predicted number of guesses needed."
}

show_descriptions = False

def toggle_descriptions():
    global show_descriptions
    show_descriptions = not show_descriptions
    if entry.get():
        check_word()

def check_word():
    word = entry.get().strip().lower()
    result_text.delete("1.0", tk.END)
    expected_label.config(text="")
    percentile_label.config(text="")
    similar_label.config(text="")

    if len(word) != 5 or not word.isalpha():
        messagebox.showerror("Invalid Input", "Please enter a valid 5-letter word.")
        return

    if word not in word_data:
        messagebox.showinfo("Not Found", f"The word '{word.upper()}' was not found in the dataset.")
        return

    data = word_data[word]
    expected_label.config(text=f"Expected Guesses: {data['ExpectedGuesses']:.2f}")

    percentile = percentileofscore(actual_ods_scores, data["ODS"])
    percentile_label.config(text=f"This word is harder than {percentile:.1f}% of Wordles")

    similar_candidates = [(w, abs(word_data[w]["ODS"] - data["ODS"])) for w in actual_word_list if w != word and w in word_data]
    similar_sorted = sorted(similar_candidates, key=lambda x: x[1])[:5]
    similar_words = ", ".join(w for w, _ in similar_sorted)
    similar_label.config(text=f"Words with similar difficulty: {similar_words}")

    detailed_result = f"WORD:  {word.upper()}\n\n"
    for key in ["LFS", "PLFS", "RLP", "HLT", "WSA", "OS", "ODS"]:
        detailed_result += f"{key} : {data[key]:.3f}"
        if show_descriptions:
            detailed_result += f"\n    → {FACTOR_DESCRIPTIONS[key]}"
        detailed_result += "\n\n"

    if show_descriptions:
        detailed_result += f"Expected Guesses: {data['ExpectedGuesses']:.2f}\n"
        detailed_result += f"    → {FACTOR_DESCRIPTIONS['ExpectedGuesses']}\n"

    result_text.insert(tk.END, detailed_result)

# Widgets for Difficulty Tab
tk.Label(difficulty_tab, text="🔍Wordle Difficulty Calculator", font=FONT_TITLE,
         fg="#ecf0f1", bg="#1e272e").pack(pady=20)
entry_frame = tk.Frame(difficulty_tab, bg="#1e272e")
entry_frame.pack()
tk.Label(entry_frame, text="Enter a 5-letter word:", font=FONT_LABEL, bg="#1e272e", fg="#dcdde1").pack()
entry = tk.Entry(entry_frame, font=("Segoe UI", 14), justify="center", width=12, relief="solid", bd=1, bg="#ffffff")
entry.pack(pady=10)
expected_label = tk.Label(difficulty_tab, text="", font=FONT_GUESS, fg="#e74c3c", bg="#1e272e")
expected_label.pack(pady=5)
percentile_label = tk.Label(difficulty_tab, text="", font=("Segoe UI", 14), fg="#f39c12", bg="#1e272e")
percentile_label.pack(pady=2)
similar_label = tk.Label(difficulty_tab, text="", font=("Segoe UI", 12), fg="#7ed6df", bg="#1e272e")
similar_label.pack(pady=2)
card_frame = tk.Frame(difficulty_tab, bg="#2c3e50", bd=2, relief="flat", highlightbackground="#34495e", highlightthickness=1)
card_frame.pack(pady=10, padx=30, fill="both", expand=True)
result_text = tk.Text(card_frame, height=18, font=FONT_MONO, bg="#2c3e50", fg="#ecf0f1", relief="flat", wrap="word", insertbackground="white")
result_text.pack(padx=16, pady=16, fill="both", expand=True)
button_frame = tk.Frame(difficulty_tab, bg="#1e272e")
button_frame.pack(pady=10)
check_btn = tk.Button(button_frame, text="Check Difficulty", command=check_word, font=FONT_LABEL, bg="#2ecc71", fg="white", relief="flat", activebackground="#27ae60", padx=16, pady=8)
check_btn.grid(row=0, column=0, padx=12)
desc_btn = tk.Button(button_frame, text="Factor Descriptions", command=toggle_descriptions, font=FONT_LABEL, bg="#9b59b6", fg="white", relief="flat", activebackground="#8e44ad", padx=16, pady=8)
desc_btn.grid(row=0, column=1, padx=12)
add_github_link(difficulty_tab)

# ---------- Tab 2: Guess the Difficulty ---------- #
guess_tab = tk.Frame(notebook, bg="#1e272e")
notebook.add(guess_tab, text="🎯 Guess Difficulty")

score = {"correct": 0, "total": 0}
current_game_word = [None]

def launch_game():
    current_game_word[0] = choice(actual_word_list)
    word_display_label.config(
        text=f"What % of words do you think '{current_game_word[0]}' is harder than?")
    guess_entry.delete(0, tk.END)
    game_result_label.config(text="")

def submit_guess():
    if current_game_word[0] is None:
        return
    guess_text = guess_entry.get().strip()
    if not guess_text.isdigit() or not (0 <= int(guess_text) <= 100):
        messagebox.showwarning("Invalid", "Enter a number between 0 and 100.")
        return
    guess = int(guess_text)
    word = current_game_word[0]
    current_game_word[0] = None
    if word not in word_data:
        game_result_label.config(text="Word not found in dataset.")
        return
    actual_percentile = percentileofscore(actual_ods_scores, word_data[word]["ODS"])
    diff = abs(actual_percentile - guess)
    score["total"] += 1
    if diff <= 10:
        score["correct"] += 1
        game_result_label.config(text=f"✅ Correct! Actual: {actual_percentile:.1f}%", fg="#2ecc71")
    else:
        game_result_label.config(text=f"❌ Off by {diff:.1f}%. Actual: {actual_percentile:.1f}%", fg="#e74c3c")
    score_label.config(text=f"Score: {score['correct']} / {score['total']} ({100*score['correct']/score['total']:.1f}%)")
    root.after(3000, launch_game)

tk.Label(guess_tab, text="🎯 Guess the Wordle Difficulty", font=("Segoe UI", 18, "bold"), fg="#f1c40f", bg="#1e272e").pack(pady=10)
word_display_label = tk.Label(guess_tab, text="", font=("Segoe UI", 13), bg="#1e272e", fg="#f1c40f", wraplength=600, justify="center")
word_display_label.pack(pady=4)
guess_entry = tk.Entry(guess_tab, font=("Segoe UI", 14), justify="center", width=8, relief="solid", bd=1, bg="#ffffff")
guess_entry.pack(pady=4)
tk.Button(guess_tab, text="➡️ Submit Guess", command=submit_guess, font=FONT_LABEL, bg="#2980b9", fg="white", relief="flat", activebackground="#2471a3", padx=12, pady=6).pack(pady=4)
game_result_label = tk.Label(guess_tab, text="", font=("Segoe UI", 12), fg="white", bg="#1e272e", wraplength=600)
game_result_label.pack(pady=4)
score_label = tk.Label(guess_tab, text="", font=("Segoe UI", 11), fg="#bdc3c7", bg="#1e272e")
score_label.pack(pady=2)
tk.Button(guess_tab, text="🎯 Play: Guess the Difficulty", command=launch_game, font=FONT_LABEL, bg="#f39c12", fg="white", relief="flat", activebackground="#d35400", padx=16, pady=8).pack(pady=12)
instructions_frame = tk.Frame(guess_tab, bg="#1e272e")
instructions_frame.pack(pady=(15, 5))

tk.Label(instructions_frame, text="📘 How to Play", font=("Segoe UI", 13, "bold"),
         fg="#74b9ff", bg="#1e272e").pack()

instruction_text = (
    "A 5-letter word will be shown.\n"
    "Your task is to estimate how difficult it is —\n"
    "specifically, what percentage of actual Wordle words it is harder than.\n\n"
    "🔢 Enter a number from 0 to 100.\n"
    "✅ If your guess is within ±10% of the true difficulty percentile, it's correct!\n"
    "🎯 Try to keep your score streak going!"
)

tk.Label(instructions_frame, text=instruction_text, font=("Segoe UI", 11),
         fg="#dfe6e9", bg="#1e272e", justify="center", wraplength=600).pack()

add_github_link(guess_tab)

# ---------- Tab 3: Rank by Difficulty (new game) ---------- #
rank_tab = tk.Frame(notebook, bg="#1e272e")
notebook.add(rank_tab, text="📊 Rank Difficulty")

tk.Label(rank_tab, text="📊 Rank Words by Difficulty (Easiest → Hardest)", font=("Segoe UI", 16, "bold"), fg="#00cec9", bg="#1e272e").pack(pady=10)

ranking_words = []
word_buttons = []

ranking_frame = tk.Frame(rank_tab, bg="#1e272e")
ranking_frame.pack(pady=5)

ranking_output = tk.Label(rank_tab, text="", font=("Segoe UI", 12), fg="white", bg="#1e272e")
ranking_output.pack(pady=5)

def setup_ranking_game():
    global ranking_words
    for btn in word_buttons:
        btn.destroy()
    word_buttons.clear()
    ranking_output.config(text="")

    ranking_words = sample([w for w in actual_word_list if w in word_data], 4)
    ranking_words.sort()  # Display alphabetically first

    for w in ranking_words:
        btn = tk.Button(ranking_frame, text=w.upper(), font=("Segoe UI", 14), width=10,
                        command=lambda word=w: move_word(word), bg="#34495e", fg="white")
        btn.pack(pady=4)
        word_buttons.append(btn)

    confirm_btn.pack(pady=8)

selected_order = []

selected_frame = tk.Frame(rank_tab, bg="#1e272e")
selected_frame.pack()

confirm_btn = tk.Button(rank_tab, text="➡️ Submit Order", font=FONT_LABEL,
                        bg="#27ae60", fg="white", relief="flat",
                        activebackground="#229954", padx=14, pady=6)


def move_word(word):
    if word in selected_order:
        return
    lbl = tk.Label(selected_frame, text=word.upper(), font=("Segoe UI", 13), bg="#2d3436", fg="white", width=10)
    lbl.pack(pady=2)
    selected_order.append(word)
    if len(selected_order) == 4:
        confirm_btn.config(command=submit_ranking)

def submit_ranking():
    correct_order = sorted(ranking_words, key=lambda w: word_data[w]["ODS"])
    if selected_order == correct_order:
        ranking_output.config(text="✅ Correct ranking!", fg="#2ecc71")
    else:
        correct_display = " → ".join(w.upper() for w in correct_order)
        ranking_output.config(text=f"❌ Incorrect. Correct: {correct_display}", fg="#e74c3c")
    selected_order.clear()
    for widget in selected_frame.winfo_children():
        widget.destroy()
    root.after(7000, setup_ranking_game)

setup_ranking_game()
# Instructions for Rank by Difficulty
rank_instructions_frame = tk.Frame(rank_tab, bg="#1e272e")
rank_instructions_frame.pack(pady=(15, 5))

tk.Label(rank_instructions_frame, text="📘 How to Play", font=("Segoe UI", 13, "bold"),
         fg="#74b9ff", bg="#1e272e").pack()

rank_instruction_text = (
    "You will be given 4 five-letter words.\n"
    "Your task is to **rank them from easiest to hardest** based on Wordle difficulty.\n\n"
    "🔁 Click the words in your desired order (Easiest → Hardest).\n"
    "📊 After selecting all 4, click 'Submit Order'.\n"
    "✅ You'll see if you got the order right!"
)

tk.Label(rank_instructions_frame, text=rank_instruction_text, font=("Segoe UI", 11),
         fg="#dfe6e9", bg="#1e272e", justify="center", wraplength=600).pack()

add_github_link(rank_tab)

# ---------- Tab 4: Difficulty Duel ---------- #
duel_tab = tk.Frame(notebook, bg="#1e272e")
notebook.add(duel_tab, text="⚔️ Difficulty Duel")
tk.Label(duel_tab, text="⚔️ Difficulty Duel: Which Word is Tougher?",
         font=("Segoe UI", 16, "bold"), fg="#fd79a8", bg="#1e272e").pack(pady=14)

duel_frame = tk.Frame(duel_tab, bg="#1e272e")
duel_frame.pack()

duel_words = [None, None]  # word_a, word_b
duel_score = {"correct": 0, "total": 0}

def generate_duel():
    candidates = sample([w for w in actual_word_list if w in word_data], 2)
    duel_words[0], duel_words[1] = candidates
    duel_result_label.config(text="", fg="white")
    duel_a_btn.config(text=duel_words[0].upper(), state="normal")
    duel_b_btn.config(text=duel_words[1].upper(), state="normal")

def make_duel_guess(choice):
    word_a, word_b = duel_words
    harder = word_a if word_data[word_a]["ODS"] > word_data[word_b]["ODS"] else word_b
    correct = (choice == harder)

    duel_score["total"] += 1
    if correct:
        duel_score["correct"] += 1
        duel_result_label.config(text="✅ Correct!", fg="#2ecc71")
    else:
        duel_result_label.config(text=f"❌ Wrong! Tougher word was: {harder.upper()}", fg="#e74c3c")

    duel_score_label.config(
        text=f"Score: {duel_score['correct']} / {duel_score['total']} ({100*duel_score['correct']/duel_score['total']:.1f}%)"
    )
    duel_a_btn.config(state="disabled")
    duel_b_btn.config(state="disabled")
    root.after(2000, generate_duel)

duel_btn_frame = tk.Frame(duel_frame, bg="#1e272e")
duel_btn_frame.pack(pady=6)

duel_a_btn = tk.Button(duel_btn_frame, text="", font=("Segoe UI", 14, "bold"),
                       width=12, bg="#34495e", fg="white", command=lambda: make_duel_guess(duel_words[0]))
duel_a_btn.grid(row=0, column=0, padx=20)

duel_b_btn = tk.Button(duel_btn_frame, text="", font=("Segoe UI", 14, "bold"),
                       width=12, bg="#34495e", fg="white", command=lambda: make_duel_guess(duel_words[1]))
duel_b_btn.grid(row=0, column=1, padx=20)

tk.Button(duel_tab, text="🔄 Start Duel", command=generate_duel,
          font=FONT_LABEL, bg="#e84393", fg="white", relief="flat",
          activebackground="#d63072", padx=16, pady=6).pack(pady=8)

duel_result_label = tk.Label(duel_tab, text="", font=("Segoe UI", 13),
                             fg="white", bg="#1e272e")
duel_result_label.pack()

duel_score_label = tk.Label(duel_tab, text="", font=("Segoe UI", 11),
                            fg="#bdc3c7", bg="#1e272e")
duel_score_label.pack(pady=3)
# Instructions for Difficulty Duel
duel_instructions_frame = tk.Frame(duel_tab, bg="#1e272e")
duel_instructions_frame.pack(pady=(15, 5))

tk.Label(duel_instructions_frame, text="📘 How to Play", font=("Segoe UI", 13, "bold"),
         fg="#74b9ff", bg="#1e272e").pack()

duel_instruction_text = (
    "You’ll be shown **two 5-letter words**.\n"
    "Your task is to choose the one that’s **harder to guess** in Wordle.\n\n"
    "🔍 Click the word you think is harder.\n"
    "✅ Get it right to earn a point!\n"
    "🔁 The next duel starts automatically after a short delay."
)

tk.Label(duel_instructions_frame, text=duel_instruction_text, font=("Segoe UI", 11),
         fg="#dfe6e9", bg="#1e272e", justify="center", wraplength=600).pack()

add_github_link(duel_tab)

# ---------- Tab 5: Odd One Out ---------- #
fakeout_tab = tk.Frame(notebook, bg="#1e272e")
notebook.add(fakeout_tab, text="🕵️ Odd One Out")

tk.Label(fakeout_tab, text="🕵️ Spot the Fake Word!", font=("Segoe UI", 16, "bold"),
         fg="#fab1a0", bg="#1e272e").pack(pady=14)

fakeout_frame = tk.Frame(fakeout_tab, bg="#1e272e")
fakeout_frame.pack(pady=10)

fakeout_result_label = tk.Label(fakeout_tab, text="", font=("Segoe UI", 12),
                                fg="white", bg="#1e272e")
fakeout_result_label.pack(pady=5)

fakeout_score_label = tk.Label(fakeout_tab, text="", font=("Segoe UI", 11),
                               fg="#bdc3c7", bg="#1e272e")
fakeout_score_label.pack()

# Prepare real obscure words
real_obscure_words = [w for w in word_data if word_data[w]["OS"] == 1.0]

# Train 2-letter n-gram model on those
from collections import defaultdict
import random

ngram_counts = defaultdict(list)
for word in real_obscure_words:
    for i in range(len(word)-2):
        prefix = word[i:i+2]
        next_letter = word[i+2]
        ngram_counts[prefix].append(next_letter)

def generate_fake_word():
    while True:
        word = random.choice(real_obscure_words)
        base = word[:2]
        result = base
        while len(result) < 5:
            options = ngram_counts.get(result[-2:], [])
            if not options:
                break
            result += random.choice(options)
        if result not in word_data and len(result) == 5:
            return result.lower()

# Game logic
fakeout_words = []
fakeout_answer = None
fakeout_buttons = []

def setup_fakeout_round():
    global fakeout_words, fakeout_answer

    # Reset
    for btn in fakeout_buttons:
        btn.destroy()
    fakeout_buttons.clear()
    fakeout_result_label.config(text="")

    real_choices = random.sample(real_obscure_words, 3)
    fake = generate_fake_word()
    fakeout_words = real_choices + [fake]
    random.shuffle(fakeout_words)
    fakeout_answer = fake

    for w in fakeout_words:
        btn = tk.Button(fakeout_frame, text=w.upper(), font=("Segoe UI", 14),
                        width=10, bg="#34495e", fg="white",
                        command=lambda word=w: handle_fakeout_guess(word))
        btn.pack(pady=6)
        fakeout_buttons.append(btn)

fakeout_score = {"correct": 0, "total": 0}

def handle_fakeout_guess(selected):
    global fakeout_answer
    for btn in fakeout_buttons:
        btn.config(state="disabled")

    fakeout_score["total"] += 1
    if selected == fakeout_answer:
        fakeout_score["correct"] += 1
        fakeout_result_label.config(text="✅ Correct! That was the fake.", fg="#2ecc71")
    else:
        fakeout_result_label.config(text=f"❌ Nope! The fake was: {fakeout_answer.upper()}", fg="#e74c3c")

    fakeout_score_label.config(
        text=f"Score: {fakeout_score['correct']} / {fakeout_score['total']} ({100*fakeout_score['correct']/fakeout_score['total']:.1f}%)"
    )

    root.after(3000, setup_fakeout_round)

# Launch first round
setup_fakeout_round()

# Instructions for One Fake Out
fakeout_instructions_frame = tk.Frame(fakeout_tab, bg="#1e272e")
fakeout_instructions_frame.pack(pady=(15, 5))

tk.Label(fakeout_instructions_frame, text="📘 How to Play", font=("Segoe UI", 13, "bold"),
         fg="#74b9ff", bg="#1e272e").pack()

fakeout_instruction_text = (
    "You’ll be shown **four 5-letter words**.\n"
    "But **only three are real Wordle words** — one is a cleverly disguised fake!\n\n"
    "🕵️‍♂️ Your goal: **Spot the fake word**.\n"
    "💡 The fake will look plausible but doesn't exist in Wordle.\n"
    "Click the word you think is fake to see if you're right!"
)

tk.Label(fakeout_instructions_frame, text=fakeout_instruction_text, font=("Segoe UI", 11),
         fg="#dfe6e9", bg="#1e272e", justify="center", wraplength=600).pack()

# Add GitHub link
add_github_link(fakeout_tab)

# ---------- Tab 6: Difficulty Ladder ---------- #
difficulty_ladder_tab = tk.Frame(notebook, bg="#1e272e")
notebook.add(difficulty_ladder_tab, text="🌿 Difficulty Ladder")

tk.Label(difficulty_ladder_tab, text="🌿 Difficulty Ladder: Easier or Harder?",
         font=("Segoe UI", 16, "bold"), fg="#55efc4", bg="#1e272e").pack(pady=14)

ladder_word_label = tk.Label(difficulty_ladder_tab, text="", font=("Segoe UI", 16, "bold"),
                              fg="#f1c40f", bg="#1e272e")
ladder_word_label.pack(pady=10)

ladder_feedback_label = tk.Label(difficulty_ladder_tab, text="", font=("Segoe UI", 13),
                                 fg="white", bg="#1e272e")
ladder_feedback_label.pack(pady=4)

ladder_score = {"correct": 0, "total": 0}
ladder_current_word = [None]

ladder_button_frame = tk.Frame(difficulty_ladder_tab, bg="#1e272e")
ladder_button_frame.pack(pady=8)

def start_ladder_game():
    ladder_current_word[0] = choice([w for w in actual_word_list if w in word_data])
    ladder_word_label.config(text=f"Current Word: {ladder_current_word[0].upper()}", fg="#f1c40f")
    ladder_feedback_label.config(text="")
    ladder_score_label.config(text=f"Score: {ladder_score['correct']} / {ladder_score['total']}")

def guess_harder():
    evaluate_ladder_guess(guess="harder")

def guess_easier():
    evaluate_ladder_guess(guess="easier")

def evaluate_ladder_guess(guess):
    old_word = ladder_current_word[0]
    new_word = choice([w for w in actual_word_list if w in word_data and w != old_word])
    ladder_current_word[0] = new_word

    old_diff = word_data[old_word]["ODS"]
    new_diff = word_data[new_word]["ODS"]

    correct = (new_diff > old_diff and guess == "harder") or (new_diff < old_diff and guess == "easier")

    ladder_score["total"] += 1
    if correct:
        ladder_score["correct"] += 1
        ladder_feedback_label.config(text=f"✅ Correct! New word: {new_word.upper()} ({new_diff:.3f})", fg="#2ecc71")
    else:
        ladder_feedback_label.config(text=f"❌ Wrong! New word: {new_word.upper()} ({new_diff:.3f})", fg="#e74c3c")

    ladder_word_label.config(text=f"Current Word: {new_word.upper()}")
    ladder_score_label.config(
        text=f"Score: {ladder_score['correct']} / {ladder_score['total']} ({100*ladder_score['correct']/ladder_score['total']:.1f}%)")

ladder_harder_btn = tk.Button(ladder_button_frame, text="🔼 HARDER", command=guess_harder,
                              font=FONT_LABEL, bg="#e17055", fg="white", relief="flat",
                              activebackground="#d35400", padx=16, pady=8)
ladder_harder_btn.grid(row=0, column=0, padx=10)

ladder_easier_btn = tk.Button(ladder_button_frame, text="🔽 EASIER", command=guess_easier,
                              font=FONT_LABEL, bg="#0984e3", fg="white", relief="flat",
                              activebackground="#0652DD", padx=16, pady=8)
ladder_easier_btn.grid(row=0, column=1, padx=10)

ladder_score_label = tk.Label(difficulty_ladder_tab, text="", font=("Segoe UI", 12),
                              fg="#bdc3c7", bg="#1e272e")
ladder_score_label.pack(pady=4)

tk.Button(difficulty_ladder_tab, text="🔄 Start Game", command=start_ladder_game,
          font=FONT_LABEL, bg="#00cec9", fg="white", relief="flat",
          activebackground="#00b894", padx=16, pady=8).pack(pady=6)

# Instructions for Difficulty Ladder
ladder_instructions_frame = tk.Frame(difficulty_ladder_tab, bg="#1e272e")
ladder_instructions_frame.pack(pady=(15, 5))

tk.Label(ladder_instructions_frame, text="📘 How to Play", font=("Segoe UI", 13, "bold"),
         fg="#74b9ff", bg="#1e272e").pack()

ladder_instruction_text = (
    "Start with a random Wordle word.\n"
    "Each round, you'll be shown a new word.\n"
    "Your task: decide if it's **EASIER or HARDER** than the previous word.\n\n"
    "🔼 Click **HARDER** if you think it's more difficult.\n"
    "🔽 Click **EASIER** if it's simpler.\n"
    "🏆 Try to build the longest streak!"
)

tk.Label(ladder_instructions_frame, text=ladder_instruction_text, font=("Segoe UI", 11),
         fg="#dfe6e9", bg="#1e272e", justify="center", wraplength=600).pack()


add_github_link(difficulty_ladder_tab)

# ---------- Tab 7: Word Builder Blitz ---------- #
builder_tab = tk.Frame(notebook, bg="#1e272e")
notebook.add(builder_tab, text="🧱 Word Builder Blitz")

tk.Label(builder_tab, text="🧱 Word Builder Blitz", font=("Segoe UI", 16, "bold"),
         fg="#fab1a0", bg="#1e272e").pack(pady=10)

tk.Label(builder_tab, text="Form valid 5-letter words using the given letters!\n(60 seconds per round)",
         font=("Segoe UI", 11), fg="#dfe6e9", bg="#1e272e").pack()

builder_letters_label = tk.Label(builder_tab, text="", font=("Courier New", 22, "bold"),
                                 fg="#ffeaa7", bg="#1e272e")
builder_letters_label.pack(pady=10)

builder_timer_label = tk.Label(builder_tab, text="", font=("Segoe UI", 12),
                               fg="#fab1a0", bg="#1e272e")
builder_timer_label.pack(pady=2)

builder_entry = tk.Entry(builder_tab, font=("Segoe UI", 14), justify="center", width=10)
builder_entry.pack(pady=4)
builder_entry.bind("<Return>", lambda e: check_builder_word())

builder_feedback = tk.Label(builder_tab, text="", font=("Segoe UI", 12),
                            fg="white", bg="#1e272e")
builder_feedback.pack()

builder_score_label = tk.Label(builder_tab, text="", font=("Segoe UI", 12),
                               fg="#81ecec", bg="#1e272e")
builder_score_label.pack(pady=2)

builder_high_score_label = tk.Label(builder_tab, text="", font=("Segoe UI", 11),
                                    fg="#55efc4", bg="#1e272e")
builder_high_score_label.pack()

builder_answers_label = tk.Label(builder_tab, text="", font=("Segoe UI", 10),
                                 fg="#dfe6e9", bg="#1e272e", wraplength=700, justify="center")
builder_answers_label.pack(pady=6)

builder_used_words = set()
builder_letters = []
builder_score = 0
builder_high_score = 0
builder_timer_id = None
builder_time_left = 60
builder_word_set = set(df['Word'].tolist())
current_valid_words = []

def generate_letter_pool():
    vowels = 'aeiou'
    all_letters = 'abcdefghijklmnopqrstuvwxyz'
    pool = sample(vowels, 2) + sample(all_letters, 6)
    return sample(pool, 8)

def find_valid_words():
    valid = []
    for word in builder_word_set:
        if len(word) == 5 and all(word.count(c) <= builder_letters.count(c) for c in set(word)):
            valid.append(word)
    return valid

def start_builder_round():
    global builder_letters, builder_used_words, builder_score, builder_timer_id, builder_time_left, current_valid_words
    if builder_timer_id:
        builder_tab.after_cancel(builder_timer_id)

    builder_letters = generate_letter_pool()
    builder_used_words.clear()
    builder_score = 0
    builder_time_left = 60
    current_valid_words = find_valid_words()

    builder_letters_label.config(text=" ".join(l.upper() for l in builder_letters))
    builder_feedback.config(text="")
    builder_answers_label.config(text="")
    builder_entry.delete(0, tk.END)
    update_builder_scores()
    update_builder_timer()

def update_builder_timer():
    global builder_time_left, builder_timer_id

    builder_timer_label.config(text=f"⏳ Time left: {builder_time_left}s")
    if builder_time_left > 0:
        builder_time_left -= 1
        builder_timer_id = builder_tab.after(1000, update_builder_timer)
    else:
        end_builder_round()

def end_builder_round():
    global builder_score, current_valid_words

    builder_feedback.config(text="⏰ Time's up! Showing valid answers.", fg="#ffeaa7")
    valid_text = "✔ Valid words:\n" + ", ".join(sorted(current_valid_words))
    builder_answers_label.config(text=valid_text)

    if builder_score > builder_high_score:
        builder_high_score = builder_score
    update_builder_scores()

    builder_tab.after(5000, start_builder_round)

def check_builder_word():
    global builder_score, builder_high_score

    word = builder_entry.get().strip().lower()
    builder_entry.delete(0, tk.END)

    if len(word) != 5 or not word.isalpha():
        builder_feedback.config(text="❌ Enter a valid 5-letter word", fg="#fab1a0")
        return

    if word in builder_used_words:
        builder_feedback.config(text="⚠️ Already used!", fg="#ffeaa7")
        return

    if word not in builder_word_set:
        builder_feedback.config(text="❌ Not in word list!", fg="#ff7675")
        return

    if all(word.count(c) <= builder_letters.count(c) for c in set(word)):
        builder_used_words.add(word)
        builder_score += 1
        builder_feedback.config(text="✅ Good word!", fg="#00cec9")
        if builder_score > builder_high_score:
            builder_high_score = builder_score
        update_builder_scores()
    else:
        builder_feedback.config(text="❌ Invalid letters!", fg="#d63031")

def update_builder_scores():
    builder_score_label.config(text=f"Score this round: {builder_score}")
    builder_high_score_label.config(text=f"🏆 High Score: {builder_high_score}")

tk.Button(builder_tab, text="➡️ Submit Word", command=check_builder_word,
          font=FONT_LABEL, bg="#6c5ce7", fg="white", relief="flat",
          activebackground="#341f97", padx=14, pady=6).pack(pady=6)

tk.Button(builder_tab, text="🔁 Start / Refresh Game", command=start_builder_round,
          font=FONT_LABEL, bg="#fd79a8", fg="white", relief="flat",
          activebackground="#e84393", padx=14, pady=6).pack(pady=8)

add_github_link(builder_tab)

# ---------- Tab 8: Word Morph ---------- #
import json

# Load morph pairs from JSON
with open(MORPH_PATH, 'r') as f:
    morph_pairs = json.load(f)

word_morph_tab = tk.Frame(notebook, bg="#1e272e")
notebook.add(word_morph_tab, text="🔁 Word Morph")

tk.Label(word_morph_tab, text="🔁 Word Morph Challenge", font=("Segoe UI", 16, "bold"),
         fg="#81ecec", bg="#1e272e").pack(pady=14)

instructions = (
    "Change one letter at a time to go from the START word to the END word.\n"
    "Each step must be a valid word. Can you complete the path?"
)
tk.Label(word_morph_tab, text=instructions, font=("Segoe UI", 11),
         fg="#dfe6e9", bg="#1e272e", justify="center").pack(pady=6)

morph_game_frame = tk.Frame(word_morph_tab, bg="#1e272e")
morph_game_frame.pack(pady=10)

morph_labels = []
morph_entries = []
morph_path = []
current_morph_pair = {}

morph_answer_label = tk.Label(word_morph_tab, text="", font=("Segoe UI", 11),
                              fg="#dfe6e9", bg="#1e272e")
morph_answer_label.pack(pady=6)

def new_morph_challenge():
    for widget in morph_game_frame.winfo_children():
        widget.destroy()
    morph_labels.clear()
    morph_entries.clear()
    morph_answer_label.config(text="")

    pair = choice(morph_pairs)
    morph_path.clear()
    morph_path.extend(pair)
    current_morph_pair["start"] = pair[0]
    current_morph_pair["end"] = pair[-1]
    current_morph_pair["path"] = pair

    tk.Label(morph_game_frame, text=f"START: {pair[0].upper()}",
             font=("Segoe UI", 14), fg="#00cec9", bg="#1e272e").pack(pady=4)

    for _ in range(len(pair) - 2):
        entry = tk.Entry(morph_game_frame, font=("Segoe UI", 14), justify="center", width=10)
        entry.pack(pady=3)
        morph_entries.append(entry)

    tk.Label(morph_game_frame, text=f"END: {pair[-1].upper()}",
             font=("Segoe UI", 14), fg="#fdcb6e", bg="#1e272e").pack(pady=4)

    tk.Button(morph_game_frame, text="Submit", command=check_morph_attempt,
              font=FONT_LABEL, bg="#6c5ce7", fg="white", relief="flat",
              activebackground="#341f97", padx=12, pady=6).pack(pady=6)

def check_morph_attempt():
    guess_path = [morph_path[0]] + [e.get().strip().lower() for e in morph_entries] + [morph_path[-1]]
    if guess_path == morph_path:
        result = "✅ Correct! You solved the morph chain!"
        color = "#00b894"
    else:
        result = "❌ Incorrect. Try again or reveal the answer."
        color = "#d63031"

    tk.Label(morph_game_frame, text=result, font=("Segoe UI", 12, "bold"),
             fg=color, bg="#1e272e").pack(pady=4)

def reveal_solution():
    if "path" in current_morph_pair:
        sol_str = " → ".join(w.upper() for w in current_morph_pair["path"])
        morph_answer_label.config(text=f"✅ Path: {sol_str}")

tk.Button(word_morph_tab, text="🔄 New Morph Puzzle", command=new_morph_challenge,
          font=FONT_LABEL, bg="#00cec9", fg="white", relief="flat",
          activebackground="#00b894", padx=16, pady=8).pack(pady=6)

tk.Button(word_morph_tab, text="🧠 Show Answer", command=reveal_solution,
          font=FONT_LABEL, bg="#636e72", fg="white", relief="flat",
          activebackground="#2d3436", padx=12, pady=6).pack(pady=2)

add_github_link(word_morph_tab)

# ---------- Tab 9: Reverse Wordle ---------- #
import json

GRID_PATH = resource_path(os.path.join("data", "grid_puzzles.json"))
with open(GRID_PATH, 'r') as f:
    raw_grid_puzzles = json.load(f)

# Filter to only include puzzles whose solution has OS < 0.5
grid_puzzles = [
    p for p in raw_grid_puzzles
    if p['solution'] in word_data and word_data[p['solution']]['OS'] < 0.5
]

random.shuffle(grid_puzzles)
grid_index = [0]
grid_score = {"solved": 0, "total": 0}
timer_id = [None]

grid_tab = tk.Frame(notebook, bg="#1e272e")
notebook.add(grid_tab, text="🔲 Reverse Wordle")

tk.Label(grid_tab, text="🔲 Reverse Wordle Challenge", font=("Segoe UI", 16, "bold"),
         fg="#74b9ff", bg="#1e272e").pack(pady=14)

tk.Label(grid_tab, text="Recreate the original Wordle path to the solution. You have 30 seconds!\n There is only one answer per puzzle",
         font=("Segoe UI", 11), fg="#dfe6e9", bg="#1e272e").pack(pady=4)

grid_frame = tk.Frame(grid_tab, bg="#1e272e")
grid_frame.pack(pady=10)

feedback_colors = {"G": "#2ecc71", "Y": "#f1c40f", "B": "#636e72"}
countdown_label = tk.Label(grid_tab, text="", font=("Segoe UI", 12), fg="#fab1a0", bg="#1e272e")
countdown_label.pack()

feedback_label = tk.Label(grid_tab, text="", font=("Segoe UI", 12), fg="white", bg="#1e272e")
feedback_label.pack(pady=4)

score_label = tk.Label(grid_tab, text="", font=("Segoe UI", 11), fg="#bdc3c7", bg="#1e272e")
score_label.pack()

def render_grid_puzzle():
    for widget in grid_frame.winfo_children():
        widget.destroy()
    if timer_id[0]:
        root.after_cancel(timer_id[0])

    puzzle = grid_puzzles[grid_index[0]]
    for guess, feedback in puzzle['guesses'][:-1]:
        row = tk.Frame(grid_frame, bg="#1e272e")
        row.pack(pady=2)
        for i, letter in enumerate(guess):
            bg = feedback_colors.get(feedback[i], "#bdc3c7")
            tk.Label(row, text=letter.upper(), font=("Courier", 18, "bold"),
                     bg=bg, fg="white", width=2, height=1).pack(side="left", padx=2)

    tk.Label(grid_frame, text="Your Guess:", font=FONT_LABEL, bg="#1e272e", fg="white").pack(pady=(10, 4))
    guess_entry = tk.Entry(grid_frame, font=("Segoe UI", 14), justify="center", width=8)
    guess_entry.pack()
    guess_entry.bind("<Return>", lambda event: submit_grid_guess())


    submit_btn = tk.Button(grid_frame, text="Submit", font=FONT_LABEL,
                           bg="#6c5ce7", fg="white", relief="flat",
                           activebackground="#341f97", padx=12, pady=6)
    submit_btn.pack(pady=6)

    def submit_grid_guess():
        if timer_id[0]:
            root.after_cancel(timer_id[0])
        user_guess = guess_entry.get().strip().lower()
        solution = puzzle['solution']
        grid_score["total"] += 1

        if user_guess == solution:
            grid_score["solved"] += 1
            feedback_label.config(text="✅ Correct!", fg="#2ecc71")
        else:
            feedback_label.config(text=f"❌ Wrong! Answer: {solution.upper()}", fg="#e74c3c")

        score_label.config(text=f"Solved: {grid_score['solved']} / {grid_score['total']}")
        grid_index[0] += 1
        if grid_index[0] >= len(grid_puzzles):
            grid_index[0] = 0
            random.shuffle(grid_puzzles)

        root.after(2500, render_grid_puzzle)

    def time_expired():
        feedback_label.config(text=f"⏰ Time's up! Answer: {puzzle['solution'].upper()}", fg="#e74c3c")
        grid_score["total"] += 1
        score_label.config(text=f"Solved: {grid_score['solved']} / {grid_score['total']}")
        grid_index[0] += 1
        if grid_index[0] >= len(grid_puzzles):
            grid_index[0] = 0
            random.shuffle(grid_puzzles)
        root.after(2500, render_grid_puzzle)

    def countdown(t=30):
        countdown_label.config(text=f"⏳ {t} seconds")
        if t > 0:
            timer_id[0] = root.after(1000, lambda: countdown(t - 1))
        else:
            submit_btn.config(state="disabled")
            time_expired()

    submit_btn.config(command=submit_grid_guess)
    countdown()

# "Start Puzzle" button
tk.Button(grid_tab, text="▶️ Start Puzzle", command=render_grid_puzzle,
          font=FONT_LABEL, bg="#55efc4", fg="black", relief="flat",
          activebackground="#00cec9", padx=14, pady=8).pack(pady=10)

add_github_link(grid_tab)

# ---------- Tab 10: Letter Leak ---------- #
import time

word_decay_tab = tk.Frame(notebook, bg="#1e272e")
notebook.add(word_decay_tab, text="⌛ Letter Leak")

tk.Label(word_decay_tab, text="⌛ Letter Leak Challenge", font=("Segoe UI", 16, "bold"),
         fg="#fab1a0", bg="#1e272e").pack(pady=14)

tk.Label(word_decay_tab, text="A scrambled 5-letter word will be shown.\nOne letter is revealed every 2 seconds.\nTry to guess the word as quickly as possible!",
         font=("Segoe UI", 11), fg="#dfe6e9", bg="#1e272e", justify="center").pack(pady=6)

decay_frame = tk.Frame(word_decay_tab, bg="#1e272e")
decay_frame.pack(pady=10)

decay_word_label = tk.Label(decay_frame, text="", font=("Courier", 24, "bold"),
                            fg="white", bg="#1e272e")
decay_word_label.pack(pady=8)

decay_entry = tk.Entry(decay_frame, font=("Segoe UI", 14), justify="center", width=10)
decay_entry.pack(pady=4)

decay_entry.bind("<Return>", lambda event: submit_decay_guess())


decay_feedback = tk.Label(decay_frame, text="", font=("Segoe UI", 12),
                          fg="white", bg="#1e272e")
decay_feedback.pack(pady=4)

decay_score_label = tk.Label(decay_frame, text="", font=("Segoe UI", 11),
                             fg="#bdc3c7", bg="#1e272e")
decay_score_label.pack()

decay_start_btn = tk.Button(word_decay_tab, text="🌟Start Word Decay", font=FONT_LABEL,
                            bg="#e17055", fg="white", relief="flat", activebackground="#d35400",
                            padx=16, pady=8)
decay_start_btn.pack(pady=8)

# --- Decay Logic --- #
decay_word_list = [w for w in actual_word_list if w in word_data and len(w) == 5]
decay_score = {"total": 0, "time_sum": 0.0}
decay_reveal_timer = [None]
decay_start_time = [None]
decay_current_word = [None]
decay_reveal_index = [0]

def scramble_with_reveals(word, revealed):
    """Reveal first `revealed` letters; scramble the rest"""
    fixed = list(word[:revealed])
    remaining = list(word[revealed:])
    random.shuffle(remaining)
    return "".join(fixed + remaining)

def reveal_next_letter():
    if decay_reveal_index[0] < 5:
        decay_reveal_index[0] += 1
        scrambled = scramble_with_reveals(decay_current_word[0], decay_reveal_index[0])
        decay_word_label.config(text=scrambled.upper())
        decay_reveal_timer[0] = root.after(2000, reveal_next_letter)

def start_decay_round():
    decay_feedback.config(text="")
    decay_entry.delete(0, tk.END)
    decay_current_word[0] = random.choice(decay_word_list)
    decay_reveal_index[0] = 0
    decay_start_time[0] = time.time()
    scrambled = scramble_with_reveals(decay_current_word[0], 0)
    decay_word_label.config(text=scrambled.upper())

    # Start revealing
    if decay_reveal_timer[0]:
        root.after_cancel(decay_reveal_timer[0])
    decay_reveal_timer[0] = root.after(2000, reveal_next_letter)

def submit_decay_guess():
    user_guess = decay_entry.get().strip().lower()
    true_word = decay_current_word[0]
    time_taken = round(time.time() - decay_start_time[0], 2)

    if decay_reveal_timer[0]:
        root.after_cancel(decay_reveal_timer[0])

    decay_score["total"] += 1

    if user_guess == true_word:
        decay_feedback.config(text=f"✅ Correct! Time: {time_taken:.2f}s", fg="#2ecc71")
        decay_score["time_sum"] += time_taken
    else:
        decay_feedback.config(text=f"❌ Wrong! It was {true_word.upper()}. Time penalty: 10.00s", fg="#e74c3c")
        decay_score["time_sum"] += 10.0

    avg = decay_score["time_sum"] / decay_score["total"]
    decay_score_label.config(text=f"📊 Avg Time: {avg:.2f}s over {decay_score['total']} word(s)")

    # Queue next word
    root.after(3000, start_decay_round)

tk.Button(decay_frame, text="➡️ Submit", command=submit_decay_guess,
          font=FONT_LABEL, bg="#6c5ce7", fg="white", relief="flat",
          activebackground="#341f97", padx=12, pady=6).pack(pady=4)

decay_start_btn.config(command=start_decay_round)

add_github_link(word_decay_tab)

# ---------- Run ---------- #
root.mainloop()
