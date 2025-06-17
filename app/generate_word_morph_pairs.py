import pandas as pd
import random
import json
from collections import defaultdict, deque
import os

# Load the dataset
DATA_PATH = os.path.join("data", "final_difficulty_scores.csv")

df = pd.read_csv(DATA_PATH)
df['Word'] = df['Word'].str.lower()

# Filter words with OS < 0.5
filtered_words = set(df[df["OS"] < 0.5]["Word"])

# Build adjacency graph (words that differ by one letter)
def build_graph(words):
    graph = defaultdict(set)
    buckets = defaultdict(list)

    for word in words:
        for i in range(5):
            pattern = word[:i] + "_" + word[i+1:]
            buckets[pattern].append(word)

    for group in buckets.values():
        for i in range(len(group)):
            for j in range(i+1, len(group)):
                w1, w2 = group[i], group[j]
                graph[w1].add(w2)
                graph[w2].add(w1)

    return graph

# BFS to find the shortest path from start to end
def bfs_path(start, end, graph):
    visited = {start}
    queue = deque([[start]])

    while queue:
        path = queue.popleft()
        current = path[-1]
        if current == end:
            return path
        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])
    return None

# Generate valid morph chains
def generate_morph_pairs(words, graph, count=100, min_len=4, max_len=10):
    words_list = list(words)
    random.shuffle(words_list)
    pairs = []
    seen = set()

    attempts = 0
    while len(pairs) < count and attempts < 5000:
        w1, w2 = random.sample(words_list, 2)
        key = tuple(sorted((w1, w2)))
        if key in seen:
            continue
        seen.add(key)

        path = bfs_path(w1, w2, graph)
        if path and min_len <= len(path) <= max_len:
            pairs.append(path)
        attempts += 1

    return pairs

# Main execution
if __name__ == "__main__":
    graph = build_graph(filtered_words)
    morph_pairs = generate_morph_pairs(filtered_words, graph, count=100, min_len=4, max_len=10)

    # Save to file
    output_path = os.path.join("data", "morph_pairs.json")
    with open(output_path, "w") as f:
        json.dump(morph_pairs, f, indent=2)

    print(f"✅ Generated {len(morph_pairs)} word morph chains and saved to {output_path}")
