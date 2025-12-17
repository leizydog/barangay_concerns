from pathlib import Path
import re

BASE_DIR = Path(__file__).resolve().parent

print("=" * 80)
print("🔍 FINDING ALL CSS FILES AND THEIR USAGE")
print("=" * 80)

# Find all CSS files
print("\n1. LISTING ALL CSS FILES:")
print("-" * 80)

css_dir = BASE_DIR / 'static' / 'css'
if css_dir.exists():
    css_files = list(css_dir.glob('*.css'))
    for css_file in css_files:
        size = css_file.stat().st_size
        print(f"\n📄 {css_file.name}")
        print(f"   Path: {css_file}")
        print(f"   Size: {size:,} bytes ({size / 1024:.1f} KB)")
        
        # Show first few lines
        try:
            content = css_file.read_text(encoding='utf-8')
            lines = content.split('\n')[:5]
            print(f"   First lines:")
            for line in lines:
                if line.strip():
                    print(f"      {line[:70]}")
        except:
            print("   (Could not read file)")
else:
    print(f"❌ CSS directory not found: {css_dir}")

# Find all HTML templates
print("\n\n2. CHECKING WHICH CSS FILES ARE LOADED IN TEMPLATES:")
print("-" * 80)

template_dirs = [
    BASE_DIR / 'templates',
    BASE_DIR / 'apps' / 'security_management' / 'templates',
    BASE_DIR / 'apps' / 'concerns' / 'templates',
]

css_references = {}

for template_dir in template_dirs:
    if template_dir.exists():
        for html_file in template_dir.rglob('*.html'):
            try:
                content = html_file.read_text(encoding='utf-8')
                
                # Look for CSS references
                # Pattern 1: <link rel="stylesheet" href="...">
                link_pattern = r'<link[^>]*href=["\']([^"\']*\.css)["\']'
                # Pattern 2: {% static 'css/...' %}
                static_pattern = r'{%\s*static\s+["\']([^"\']*\.css)["\']'
                
                matches = re.findall(link_pattern, content) + re.findall(static_pattern, content)
                
                if matches:
                    relative_path = html_file.relative_to(BASE_DIR)
                    for match in matches:
                        if match not in css_references:
                            css_references[match] = []
                        css_references[match].append(str(relative_path))
                        
            except Exception as e:
                pass

if css_references:
    for css_ref, templates in css_references.items():
        print(f"\n📌 CSS Referenced: {css_ref}")
        print(f"   Used in {len(templates)} template(s):")
        for template in templates:
            print(f"      • {template}")
else:
    print("\n❌ No CSS references found in templates!")

# Check base.html specifically
print("\n\n3. CHECKING base.html (THE MOST IMPORTANT):")
print("-" * 80)

base_template = BASE_DIR / 'templates' / 'base.html'
if base_template.exists():
    print(f"\n✓ Found: {base_template}")
    content = base_template.read_text(encoding='utf-8')
    
    # Find the head section
    head_match = re.search(r'<head>(.*?)</head>', content, re.DOTALL)
    if head_match:
        head_content = head_match.group(1)
        print("\n📋 <head> section of base.html:")
        print("-" * 80)
        for line in head_content.split('\n'):
            if line.strip():
                print(f"   {line}")
        
        # Check for CSS
        if 'stylesheet' in head_content or '.css' in head_content:
            print("\n✓ CSS is being loaded in base.html")
        else:
            print("\n❌ WARNING: No CSS link found in base.html!")
    else:
        print("\n❌ Could not find <head> section")
else:
    print(f"\n❌ base.html not found at: {base_template}")

print("\n\n4. RECOMMENDATIONS:")
print("-" * 80)

print("""
Your templates should load CSS from base.html like this:

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Your Site{% endblock %}</title>
    {% load static %}
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>

The file structure should be:
    static/
    └── css/
        └── style.css  ← This is the ONE file you need to update!

If you have multiple CSS files:
    • Combine them into one file (style.css)
    • Or make sure base.html only loads style.css
    • Delete any unused CSS files to avoid confusion
""")

print("\n" + "=" * 80)
print("💡 TIP: Only ONE CSS file should be loaded (style.css)")
print("=" * 80)