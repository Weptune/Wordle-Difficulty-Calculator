import os
import tkinter as tk
from tkinter import messagebox
import pandas as pd

# Load CSV
DATA_PATH = "final_difficulty_scores.csv"
df = pd.read_csv(DATA_PATH)
df['Word'] = df['Word'].str.lower()

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

# Factor Descriptions
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

# ---------------------- GUI ---------------------- #
root = tk.Tk()
root.title("Wordle Difficulty Calculator")
root.geometry("500x580")
root.configure(bg="#f7f7f9")
root.resizable(False, False)

# Fonts
FONT_TITLE = ("Helvetica Neue", 20, "bold")
FONT_LABEL = ("Helvetica Neue", 12)
FONT_GUESS = ("Helvetica Neue", 16, "bold")
FONT_RESULT = ("Courier New", 11)

# Header
tk.Label(root, text="Wordle Difficulty Calculator", font=FONT_TITLE, fg="#2a4d69", bg="#f7f7f9").pack(pady=20)

# Entry Section
entry_frame = tk.Frame(root, bg="#f7f7f9")
entry_frame.pack()

tk.Label(entry_frame, text="Enter a 5-letter word:", font=FONT_LABEL, bg="#f7f7f9").pack()
entry = tk.Entry(entry_frame, font=("Helvetica Neue", 14), justify="center", width=10, bg="#ffffff", relief="solid", borderwidth=1)
entry.pack(pady=8)

# Expected Guesses Display
expected_label = tk.Label(root, text="", font=FONT_GUESS, fg="#d72638", bg="#f7f7f9")
expected_label.pack(pady=10)

# Result Text Box
result_frame = tk.Frame(root, bg="#f7f7f9")
result_frame.pack()

result_text = tk.Text(result_frame, height=12, width=54, font=FONT_RESULT, bg="#f0f0f5", fg="#333333", relief="flat", borderwidth=0)
result_text.pack()

# Show Factor Info
def show_info():
    info_text = "\n".join([f"{k}: {v}" for k, v in FACTOR_DESCRIPTIONS.items()])
    messagebox.showinfo("Factor Descriptions", info_text)

# Check Difficulty Function
def check_word():
    word = entry.get().strip().lower()
    result_text.delete("1.0", tk.END)
    expected_label.config(text="")

    if len(word) != 5 or not word.isalpha():
        messagebox.showerror("Invalid Input", "Please enter a valid 5-letter word.")
        return

    if word not in word_data:
        messagebox.showinfo("Not Found", f"The word '{word.upper()}' was not found in the dataset.")
        return

    data = word_data[word]
    expected_guesses = f"Expected Guesses: {data['ExpectedGuesses']:.2f}"
    expected_label.config(text=expected_guesses)

    detailed_result = (
        f"WORD: {word.upper()}\n\n"
        f"LFS : {data['LFS']:.3f}\n"
        f"PLFS: {data['PLFS']:.3f}\n"
        f"RLP : {data['RLP']:.3f}\n"
        f"HLT : {data['HLT']:.3f}\n"
        f"WSA : {data['WSA']:.3f}\n"
        f"OS  : {data['OS']:.3f}\n"
        f"ODS : {data['ODS']:.3f}\n"
    )
    result_text.insert(tk.END, detailed_result)

# Button Bar
button_frame = tk.Frame(root, bg="#f7f7f9")
button_frame.pack(pady=15)

check_btn = tk.Button(button_frame, text="Check Difficulty", command=check_word,
                      font=FONT_LABEL, bg="#2a9d8f", fg="white", relief="flat", padx=12, pady=6)
check_btn.grid(row=0, column=0, padx=10)

info_btn = tk.Button(button_frame, text="What's this?", command=show_info,
                     font=FONT_LABEL, bg="#8e44ad", fg="white", relief="flat", padx=12, pady=6)
info_btn.grid(row=0, column=1, padx=10)

# Main loop
root.mainloop()
