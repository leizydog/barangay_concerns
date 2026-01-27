import os

file_path = r"C:\Users\karlk\barangay_concerns\barangay_concerns\templates\concerns\detail.html"

with open(file_path, 'rb') as f:
    content = f.read()

# Look for "concern.location"
target = b"concern.location"
index = content.find(target)

if index != -1:
    print(f"Found target at {index}")
    # Print surrounding bytes
    start = max(0, index - 20)
    end = min(len(content), index + 20)
    snippet = content[start:end]
    print(f"Snippet: {snippet}")
    print(f"Hex: {snippet.hex()}")
    
    # Check for braces
    preceding = content[max(0, index-10):index]
    print(f"Preceding: {preceding}")
    print(f"Preceding Hex: {preceding.hex()}")
else:
    print("Target not found.")
