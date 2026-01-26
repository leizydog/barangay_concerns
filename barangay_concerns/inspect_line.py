
path = r"c:\Users\kmagh\barangay_concerns\barangay_concerns\templates\concerns\detail.html"
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

target = 230  # 0-indexed, so line 231
print(f"Line {target+1} repr: {repr(lines[target])}")

# Check surrounding lines
print(f"Line {target} repr: {repr(lines[target-1])}")
print(f"Line {target+2} repr: {repr(lines[target+1])}")
