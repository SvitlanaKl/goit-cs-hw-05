from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt
import re
from pathlib import Path

# Функція для завантаження тексту з локального файлу
def fetch_text_from_file(file_path: str) -> str:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return ""

# Map-функція для підрахунку слів у частині тексту
def map_function(chunk: str) -> Counter:
    words = re.findall(r'\b\w+\b', chunk.lower())  # Тільки слова
    return Counter(words)

# Reduce-функція для об'єднання результатів
def reduce_function(counters: list[Counter]) -> Counter:
    total_counter = Counter()
    for counter in counters:
        total_counter.update(counter)
    return total_counter

# Функція для аналізу частоти слів за допомогою MapReduce
def mapreduce_word_frequency(text: str, chunk_size: int = 1000) -> Counter:
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    with ThreadPoolExecutor() as executor:
        mapped = list(executor.map(map_function, chunks))
    return reduce_function(mapped)

# Функція для візуалізації топ-слів
def visualize_top_words(word_counts: Counter, top_n: int = 10):
    top_words = word_counts.most_common(top_n)
    words, counts = zip(*top_words)

    plt.figure(figsize=(10, 6))
    plt.bar(words, counts)
    plt.xlabel("Words")
    plt.ylabel("Frequency")
    plt.title("Top Words by Frequency")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def main():
    # Задайте шлях до локального файлу
    file_path = r"C:\Users\WORK\Desktop\GoIT\Repository\Computer_Systems\goit-cs-hw-05\Files_to_sort\text2.txt"
    
    # Завантаження тексту
    text = fetch_text_from_file(file_path)
    if not text:
        print("Failed to read text from file. Exiting.")
        return

    # Аналіз частоти слів
    word_counts = mapreduce_word_frequency(text)

    # Візуалізація топ-10 слів
    visualize_top_words(word_counts, top_n=10)

if __name__ == "__main__":
    main()
