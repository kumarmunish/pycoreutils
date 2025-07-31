#!/usr/bin/env python3
"""
Example usage of pycoreux library.
Demonstrates common shell-like operations in Python.
"""

from pycoreux import FileOps, ProcessUtils, TextUtils


def main():
    """Demonstrate pycoreux functionality."""

    print("=== pycoreux Demo ===\n")

    # Create a sample file for demonstration
    sample_content = """apple
banana
cherry
date
elderberry
fig
grape
honeydew
"""

    with open("sample.txt", "w") as f:
        f.write(sample_content)

    print("1. File Operations:")
    print("   Created sample.txt with fruit names")

    # Cat - read file
    content = FileOps.cat("sample.txt")
    print(f"   Content length: {len(content)} characters")

    # Head - first 3 lines
    first_lines = FileOps.head("sample.txt", 3)
    print(f"   First 3 lines: {first_lines}")

    # Tail - last 3 lines
    last_lines = FileOps.tail("sample.txt", 3)
    print(f"   Last 3 lines: {last_lines}")

    # Word count
    lines, words, chars = FileOps.wc("sample.txt")
    print(f"   Word count: {lines} lines, {words} words, {chars} chars")

    print("\n2. Text Processing:")

    # Grep - find patterns
    berry_matches = TextUtils.grep("berry", "sample.txt")
    print(f"   Lines containing 'berry': {berry_matches}")

    # Line numbering
    numbered = TextUtils.nl("sample.txt")
    print("   Numbered lines:")
    numbered_lines = numbered.split("\n")
    for line in numbered_lines[:3]:  # Show first 3
        print(f"     {line}")

    # Sorting
    all_lines = FileOps.cat("sample.txt").strip().split("\n")
    sorted_output = TextUtils.sort(all_lines)
    sorted_lines = sorted_output.split("\n")
    print(f"   Sorted fruits: {sorted_lines[:3]}...")  # Show first 3

    print("\n3. Process Operations:")

    # Run a simple command
    result = ProcessUtils.run("ls -la *.txt")
    if result.success:
        print(f"   Files found: {len(result.stdout.split())} items")

    # Capture output
    date_output = ProcessUtils.capture("date")
    print(f"   Current date: {date_output.strip()}")

    # Find program location
    python_path = ProcessUtils.which("python3")
    print(f"   Python location: {python_path}")

    print("\n4. Advanced Text Operations:")

    # Replace patterns
    text = "Hello world, hello universe"
    replaced = TextUtils.replace(text, "hello", "hi", ignore_case=True)
    print(f"   Text replacement: '{text}' -> '{replaced}'")

    # Word count analysis
    stats = TextUtils.wc(content)
    print(f"   Text statistics: {stats}")

    # Unique lines
    duplicate_lines = ["apple", "banana", "apple", "cherry", "banana"]
    unique_output = TextUtils.uniq(duplicate_lines)
    unique_lines = unique_output.split("\n")
    print(f"   Unique items: {unique_lines}")

    print("\n5. Chaining Operations (Pipeline-style):")

    # Simulate: cat sample.txt | grep 'e' | wc -l
    lines_with_e = TextUtils.grep("e", "sample.txt")
    count_with_e = len(lines_with_e.split("\n")) if lines_with_e else 0
    print(f"   Lines containing 'e': {count_with_e}")

    # More complex pipeline simulation
    all_fruits = FileOps.cat("sample.txt").strip().split("\n")
    filtered = [fruit for fruit in all_fruits if len(fruit) > 5]
    sorted_filtered_output = TextUtils.sort(filtered)
    sorted_filtered = sorted_filtered_output.split("\n")
    print(f"   Fruits longer than 5 chars (sorted): {sorted_filtered}")

    # Clean up
    FileOps.rm("sample.txt")
    print("\n   Cleaned up sample file")

    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    main()
