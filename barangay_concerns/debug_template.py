
import re

def validate_template(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find tags
    tag_re = re.compile(r'{%\s*(\w+)[^%]*%}')
    
    stack = []
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        line_num = i + 1
        matches = tag_re.finditer(line)
        for match in matches:
            tag_name = match.group(1)
            
            if tag_name in ['if', 'for', 'block', 'with']:
                stack.append((tag_name, line_num))
                print(f"Line {line_num}: Pushed {tag_name}")
            elif tag_name in ['endif', 'endfor', 'endblock', 'endwith']:
                if not stack:
                    print(f"Error at line {line_num}: Found {tag_name} but stack is empty")
                    return
                
                last_tag, last_line = stack[-1]
                expected_end = 'end' + last_tag
                
                if tag_name == expected_end:
                    stack.pop()
                    print(f"Line {line_num}: Popped {last_tag} (started at {last_line})")
                else:
                    print(f"Error at line {line_num}: Found {tag_name} but expected {expected_end} for {last_tag} at line {last_line}")
                    # Don't return, just continue to see more errors or maybe it's just a mismatched pair
                    return

    if stack:
        print(f"Error: Unclosed tags at end of file: {stack}")

validate_template(r'c:\Users\kmagh\barangay_concerns\barangay_concerns\templates\concerns\detail.html')
