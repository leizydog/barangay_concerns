from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
css_file = BASE_DIR / 'static' / 'css' / 'style.css'

print("=" * 60)
print("CHECKING YOUR CURRENT CSS FILE")
print("=" * 60)

if css_file.exists():
    content = css_file.read_text(encoding='utf-8')
    
    print(f"\nFile location: {css_file}")
    print(f"File size: {len(content):,} characters")
    print(f"Number of lines: {len(content.splitlines())}")
    
    # Check for new design markers
    has_glassmorphism = 'glassmorphism' in content.lower()
    has_backdrop = 'backdrop-filter' in content
    has_gradient = '--primary-gradient' in content
    has_animations = '@keyframes fadeInUp' in content
    has_dark_theme = '--bg-primary: #0f172a' in content
    
    print("\n" + "=" * 60)
    print("DESIGN CHECK:")
    print("=" * 60)
    
    checks = [
        ("Glassmorphism effects", has_glassmorphism),
        ("Backdrop filter", has_backdrop),
        ("Gradient variables", has_gradient),
        ("Modern animations", has_animations),
        ("Dark theme", has_dark_theme),
    ]
    
    all_good = True
    for check_name, result in checks:
        status = "✓" if result else "✗"
        print(f"{status} {check_name}: {'Found' if result else 'MISSING'}")
        if not result:
            all_good = False
    
    print("\n" + "=" * 60)
    if all_good:
        print("✓ NEW DESIGN DETECTED!")
        print("=" * 60)
        print("""
Your CSS file has been updated with the new design!

If you're not seeing changes:
1. Hard refresh: Ctrl + Shift + R
2. Clear browser cache
3. Try incognito mode
4. Restart Django server
        """)
    else:
        print("✗ OLD DESIGN DETECTED!")
        print("=" * 60)
        print("""
The CSS file hasn't been updated properly.

Your CSS file is missing new design elements.
File size should be around 25,000+ characters.
Current size: """ + f"{len(content):,} characters")
        
        if len(content) < 20000:
            print("""
⚠ FILE IS TOO SMALL!

You need to copy BOTH CSS artifacts:
1. "style.css - Ultra Modern High-End Design"
2. "style.css Part 2 - Concerns & Responsive"

Both should be combined into one file!
            """)
    
    print("\n" + "=" * 60)
    print("FIRST 500 CHARACTERS OF YOUR CSS:")
    print("=" * 60)
    print(content[:500])
    print("...")
    
else:
    print(f"\n✗ CSS file not found at: {css_file}")
    print("\nMake sure the path is correct!")

print("\n" + "=" * 60)