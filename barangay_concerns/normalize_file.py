
import os

path = r"c:\Users\kmagh\barangay_concerns\barangay_concerns\templates\concerns\detail.html"

with open(path, 'rb') as f:
    raw = f.read()

# Decode as utf-8
content = raw.decode('utf-8')

# Replace NBSP
content = content.replace('\xa0', ' ')

# Normalize line endings
content = content.replace('\r\n', '\n')

# Re-write
with open(path, 'wb') as f:
    f.write(content.encode('utf-8'))

print("Normalized.")
