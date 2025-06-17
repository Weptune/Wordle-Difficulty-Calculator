import tkinter as tk
from tkinter import ttk, messagebox
from app.calculator import calculate_difficulty

def launch_gui():
    def evaluate_word():
        word = entry.get().strip().upper()
        if len(word) != 5 or not word.isalpha():
            messagebox.showerror("Invalid Input", "Please enter a valid 5-letter word.")
            return

        try:
            result = calculate_difficulty(word)
            output_text.configure(state="normal")
            output_text.delete(1.0, tk.END)

            output_text.insert(tk.END, f"📊 Difficulty Analysis for '{word}':\n\n")
            for key, value in result.items():
                output_text.insert(tk.END, f"{key:>18}: {value}\n")

            output_text.configure(state="disabled")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    root = tk.Tk()
    root.title("Wordle Difficulty Checker")
    root.geometry("500x400")
    root.resizable(False, False)

    style = ttk.Style()
    style.theme_use("clam")

    frame = ttk.Frame(root, padding=20)
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text="Enter a 5-letter Wordle word:").grid(row=0, column=0, sticky="w")
    entry = ttk.Entry(frame, width=20)
    entry.grid(row=0, column=1, padx=5)

    ttk.Button(frame, text="Evaluate", command=evaluate_word).grid(row=0, column=2, padx=5)

    output_text = tk.Text(frame, height=15, wrap="word", state="disabled")
    output_text.grid(row=1, column=0, columnspan=3, pady=15, sticky="nsew")

    scrollbar = ttk.Scrollbar(frame, command=output_text.yview)
    scrollbar.grid(row=1, column=3, sticky='ns')
    output_text['yscrollcommand'] = scrollbar.set

    root.mainloop()
