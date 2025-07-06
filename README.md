# 🧠 Wordle Difficulty Calculator & Game Suite

An all-in-one interactive Wordle toolkit that analyzes word difficulty, hosts a growing suite of creative Wordle-style mini-games, and lets you explore linguistic patterns in fun, challenging ways (only available on Windows so far).

## 🎯 Features

### 🔍 Difficulty Analyzer
- Enter any 5-letter word to analyze its difficulty.
- Uses a weighted model of six linguistic factors:
  - **LFS** – Letter Frequency Score
  - **PLFS** – Positional Letter Frequency
  - **RLP** – Repeated Letter Penalty
  - **HLT** – Hard Letter Transitions
  - **WSA** – Word Structure Advantage
  - **OS** – Obscurity Score
- Displays expected number of guesses and difficulty percentile.


![image](https://github.com/user-attachments/assets/7735bd08-15e0-486e-9955-231a12013a2e)

---

## 🕹️ Mini-Games

### 1. 🎯 **Guess the Difficulty**
Estimate what percentage of Wordle words a given word is harder than.


![image](https://github.com/user-attachments/assets/e5cd3ee5-d0db-4b8e-8722-c794f0aa79a9)


### 2. 📊 **Rank the Words**
Drag-and-drop or click-select to rank 4 words from easiest to hardest.


![image](https://github.com/user-attachments/assets/33b01610-a18a-480c-9178-8be99875107a)


### 3. ⚔️ **Difficulty Duel**
Pick which of two words is harder. Quick and intuitive!


![image](https://github.com/user-attachments/assets/e17d8b96-fda3-4b19-b066-208196a5d783)


### 4. 🕵️ **Odd One Out**
Find the fake among four obscure-looking words. Only one is made up!


![image](https://github.com/user-attachments/assets/7856388e-0546-4159-a374-734139b0279b)


### 5. ⛓ **Wordlocked**
You’re locked into a set of rules — find a word that breaks out.


![image](https://github.com/user-attachments/assets/a7e1a31f-bab2-4918-a690-426c27e7b550)


### 6. 🧱 **Word Builder Blitz**
Create as many 5-letter words as possible in 60 seconds from a random 8-letter pool (with at least 2 vowels).


![image](https://github.com/user-attachments/assets/68a98be8-3fc8-4eeb-9ece-7ddf6a196c03)


### 7. 🔁 **Word Morph**
Connect a start and end word by changing one letter at a time. Every step must be a valid word.


![image](https://github.com/user-attachments/assets/04f062bf-08fb-40b3-874b-cfeabb0a6c2a)


### 8. 🔲 **Reverse Wordle**
You're given 4 feedback rows. Can you deduce the secret word that produced them?


![image](https://github.com/user-attachments/assets/05b93ec9-94e2-4e6f-8bdc-cd00318a1958)


### 9. 🧠 **Letter Leak**
Each second reveals a new letter of a scrambled word. The faster you guess it, the better!


![image](https://github.com/user-attachments/assets/79032b62-6fcd-4b1c-8e1d-bf81d856a3a4)


---

## 💡 Tech Stack

- **Python 3.9+**
- **Tkinter** for GUI
- **Pandas** for word data processing
- **Scipy** for percentile ranking
- **JSON/CSV** for word data
- Designed to be bundled via **PyInstaller** (one-file app build)

---

## 📊 Dataset Info
This app uses a curated CSV with over 13,000+ 5-letter words scored across multiple difficulty dimensions based on linguistic frequency, structure, and obscurity.

---

## 🧠 Project Goals
Create an intuitive way to measure word difficulty.

Build engaging, educational games inspired by Wordle mechanics.

Help players improve their pattern recognition, vocabulary, and estimation skills.

