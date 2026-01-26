
import re

def validate_template(filepath):
    print(f"Reading {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find tags: {% tag ... %}
    # We capture the tag name
    tag_re = re.compile(r'{%\s*(\w+)[^%]*%}')
    
    stack = []
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        line_num = i + 1
        matches = list(tag_re.finditer(line))
        for match in matches:
            tag_name = match.group(1)
            full_tag = match.group(0)
            
            # Helper to print indentation
            indent = "  " * len(stack)
            print(f"{line_num}: {indent}{full_tag}")

            if tag_name in ['if', 'for', 'block', 'with']:
                stack.append((tag_name, line_num))
            elif tag_name in ['endif', 'endfor', 'endblock', 'endwith', 'empty']:
                if tag_name == 'empty':
                    if not stack or stack[-1][0] != 'for':
                        print(f"ERROR: Found 'empty' at line {line_num} but not in for loop. Stack: {stack}")
                    continue

                if not stack:
                    print(f"ERROR: Found {tag_name} at line {line_num} but stack is empty")
                    return
                
                last_tag, last_line = stack[-1]
                expected_end = 'end' + last_tag
                
                if tag_name == expected_end:
                    stack.pop()
                else:
                    print(f"ERROR: Found {tag_name} at line {line_num} but expected {expected_end} (for {last_tag} at line {last_line})")
                    return

    if stack:
        print(f"ERROR: Unclosed tags at end of file: {stack}")
    else:
        print("Template valid.")

validate_template(r'c:\Users\kmagh\barangay_concerns\barangay_concerns\templates\concerns\detail.html')
