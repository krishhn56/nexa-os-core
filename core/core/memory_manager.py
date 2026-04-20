import json
import os
import time

MEMORY_FILE = "memory.json"


# Load memory from file
def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []

    with open(MEMORY_FILE, "r") as f:
        try:
            return json.load(f)
        except:
            return []


# Save memory to file
def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)


# Store new memory
def store(user_input, output):
    memory = load_memory()

    memory.append({
        "input": user_input,
        "output": output,
        "time": time.time()
    })

    save_memory(memory)


# Simple search (keyword based)
def search(keyword):
    memory = load_memory()
    results = []

    for item in memory:
        score = 0

        if keyword.lower() in item["input"].lower():
            score += 2

        if keyword.lower() in item["output"].lower():
            score += 1

        if score > 0:
            item["score"] = score
            results.append(item)

    # sort by best match
    results.sort(key=lambda x: x["score"], reverse=True)

    return results


# Retrieve memory (smart)
def retrieve(user_input):
    results = search(user_input)

    if results:
        return results[:5]  # top matches

    # fallback: last 5 memories
    memory = load_memory()
    return memory[-5:]
