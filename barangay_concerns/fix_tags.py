
import re

path = r"c:\Users\kmagh\barangay_concerns\barangay_concerns\templates\concerns\detail_fixed.html"

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace {{ \n var }} with {{ var }}
# Regex: {{ followed by whitespace/newlines, then content, then whitespace/newlines, then }}
# We want to normalize to {{ content }}

def replacer(match):
    inner = match.group(1).strip()
    return f"{{{{ {inner} }}}}"

# Pattern: {{ (capture everything until ) }}
# flags=re.DOTALL to match newlines
content = re.sub(r'\{\{(.*?)\}\}', replacer, content, flags=re.DOTALL)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Tags fixed.")
