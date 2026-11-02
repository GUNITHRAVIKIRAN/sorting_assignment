
import time, csv
from pathlib import Path
import matplotlib.pyplot as plt

INPUT_FILE = Path("random_numbers.txt")
RESULTS_FILE = Path("sorting_results.csv")
GRAPH_DIR = Path("graphs")
GRAPH_DIR.mkdir(exist_ok=True)

def bubble_sort(a):
    a = a.copy()
    for i in range(len(a)):
        swapped = False
        for j in range(len(a)-i-1):
            if a[j] > a[j+1]:
                a[j], a[j+1] = a[j+1], a[j]
                swapped = True
        if not swapped: break
    return a

def selection_sort(a):
    a = a.copy()
    for i in range(len(a)):
        m = i
        for j in range(i+1, len(a)):
            if a[j] < a[m]: m = j
        a[i], a[m] = a[m], a[i]
    return a

def insertion_sort(a):
    a = a.copy()
    for i in range(1, len(a)):
        key, j = a[i], i-1
        while j >= 0 and a[j] > key:
            a[j+1] = a[j]
            j -= 1
        a[j+1] = key
    return a

def merge_sort(a):
    if len(a) <= 1: return a.copy()
    mid = len(a)//2
    left, right = merge_sort(a[:mid]), merge_sort(a[mid:])
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    return out + left[i:] + right[j:]

def quick_sort(a):
    a = a.copy()
    def sort(lo, hi):
        if lo >= hi: return
        pivot = a[(lo+hi)//2]
        i, j = lo, hi
        while i <= j:
            while a[i] < pivot: i += 1
            while a[j] > pivot: j -= 1
            if i <= j:
                a[i], a[j] = a[j], a[i]
                i += 1; j -= 1
        if lo < j: sort(lo, j)
        if i < hi: sort(i, hi)
    sort(0, len(a)-1)
    return a

def heap_sort(a):
    a = a.copy()
    n = len(a)
    def heapify(size, root):
        largest = root
        left, right = 2*root+1, 2*root+2
        if left < size and a[left] > a[largest]: largest = left
        if right < size and a[right] > a[largest]: largest = right
        if largest != root:
            a[root], a[largest] = a[largest], a[root]
            heapify(size, largest)
    for i in range(n//2-1, -1, -1): heapify(n, i)
    for end in range(n-1, 0, -1):
        a[0], a[end] = a[end], a[0]
        heapify(end, 0)
    return a

def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError("Please make sure the file 'random_numbers.txt' is in the same folder as this script. Without it, the program can't run.")
    numbers = [int(x) for x in INPUT_FILE.read_text(encoding="utf-8").split()]
    if not numbers: raise ValueError("Input file is empty.")

    algorithms = {
        "Bubble Sort": bubble_sort, "Selection Sort": selection_sort,
        "Insertion Sort": insertion_sort, "Merge Sort": merge_sort,
        "Quick Sort": quick_sort, "Heap Sort": heap_sort
    }

    sizes = sorted(set(n for n in [1000, 2000, 5000, 10000, 20000, 50000, len(numbers)] if n <= len(numbers)))
    results = []
    print(f"Loaded {len(numbers):,} numbers.")
    print("Times in seconds:")

    for size in sizes:
        original = numbers[:size]
        expected = sorted(original)
        row = {"Input size": size}
        for name, fn in algorithms.items():
            start = time.perf_counter()
            output = fn(original)
            row[name] = time.perf_counter() - start
            if output != expected: raise RuntimeError(f"{name} returned incorrect output")
        results.append(row)
        print(f"{size:>6} " + " | ".join(f"{name}: {row[name]:.6f}" for name in algorithms))

    with RESULTS_FILE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Input size", *algorithms.keys()])
        writer.writeheader(); writer.writerows(results)

    # Combined graph
    plt.figure(figsize=(10, 6))
    for name in algorithms:
        plt.plot([r["Input size"] for r in results], [r[name] for r in results], marker="o", label=name)
    plt.xlabel("Number of elements"); plt.ylabel("Execution time (seconds)")
    plt.title("Sorting Algorithms: Execution Time Comparison")
    plt.grid(True, alpha=0.3); plt.legend(); plt.tight_layout()
    plt.savefig(GRAPH_DIR / "all_algorithms_comparison.png", dpi=200); plt.close()

    # Individual graph for each algorithm
    for name in algorithms:
        plt.figure(figsize=(8, 5))
        plt.plot([r["Input size"] for r in results], [r[name] for r in results], marker="o")
        plt.xlabel("Number of elements"); plt.ylabel("Execution time (seconds)")
        plt.title(f"{name}: Input Size vs Execution Time")
        plt.grid(True, alpha=0.3); plt.tight_layout()
        plt.savefig(GRAPH_DIR / (name.lower().replace(" ", "_") + ".png"), dpi=200)
        plt.close()

    print(f"\nSaved {RESULTS_FILE}, combined graph, and six individual graphs in {GRAPH_DIR}/")

if __name__ == "__main__":
    main()
