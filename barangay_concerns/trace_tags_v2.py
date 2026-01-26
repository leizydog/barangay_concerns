
import re

def trace_template_tags(file_path, output_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    stack = []
    # Regex for start/end tags
    tag_pattern = re.compile(r'{%\s*(if|for|block|with|while)\s+.*?%}|{%\s*(endif|endfor|endblock|endwith|endwhile)\s*%}')

    with open(output_path, 'w', encoding='utf-8') as out:
        for i, line in enumerate(lines):
            line_num = i + 1
            matches = tag_pattern.finditer(line)
            
            for match in matches:
                tag_text = match.group(0)
                clean_tag = tag_text.replace('{%', '').replace('%}', '').strip().split()[0]
                is_end = clean_tag.startswith('end')
                
                if is_end:
                    expected_start = clean_tag.replace('end', '')
                    if not stack:
                        out.write(f"Line {line_num}: ERROR Unexpected {clean_tag} (Stack empty)\n")
                    else:
                        last_start_tag, last_start_line = stack.pop()
                        if last_start_tag != expected_start:
                             out.write(f"Line {line_num}: ERROR Mismatched {clean_tag}, expected end{last_start_tag} (Start {last_start_line})\n")
                        else:
                             out.write(f"Line {line_num}: Close {clean_tag} (Matches {last_start_line})\n")
                else:
                    if clean_tag in ['elif', 'else', 'empty']:
                        out.write(f"Line {line_num}: Intermediate {clean_tag}\n")
                        continue
                    
                    stack.append((clean_tag, line_num))
                    out.write(f"Line {line_num}: Open {clean_tag}\n")

        if stack:
            out.write("\nUnclosed tags:\n")
            for tag, line in stack:
                out.write(f"  {tag} (Line {line})\n")
        else:
            out.write("\nBalanced.\n")

trace_template_tags(r"c:\Users\kmagh\barangay_concerns\barangay_concerns\templates\concerns\detail.html", "tag_trace_v2.log")
