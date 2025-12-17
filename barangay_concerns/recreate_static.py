from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

print("=" * 80)
print("🔧 RECREATING STATIC DIRECTORY AND FILES")
print("=" * 80)

# Create static directory structure
static_dir = BASE_DIR / 'static'
css_dir = static_dir / 'css'
js_dir = static_dir / 'js'
images_dir = static_dir / 'images'

print("\n1. Creating directories...")
for directory in [static_dir, css_dir, js_dir, images_dir]:
    directory.mkdir(parents=True, exist_ok=True)
    print(f"   ✓ Created: {directory}")

# Modern CSS - COMPLETE VERSION
modern_css = '''/* ========================================
   ULTRA MODERN BARANGAY CONCERNS
   Complete CSS in ONE file
   ======================================== */

:root {
    --primary: #6366f1;
    --primary-dark: #4f46e5;
    --primary-light: #818cf8;
    --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    
    --glass-bg: rgba(255, 255, 255, 0.1);
    --glass-border: rgba(255, 255, 255, 0.18);
    
    --bg-primary: #0f172a;
    --bg-secondary: #1e293b;
    --bg-tertiary: #334155;
    --bg-card: rgba(30, 41, 59, 0.8);
    
    --text-primary: #f8fafc;
    --text-secondary: #cbd5e1;
    --text-tertiary: #94a3b8;
    
    --accent-blue: #3b82f6;
    --accent-purple: #a855f7;
    --accent-pink: #ec4899;
    --accent-green: #10b981;
    --accent-orange: #f59e0b;
    
    --border-radius: 16px;
    --border-radius-lg: 24px;
    --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.15);
    --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.2);
    --shadow-glow: 0 0 20px rgba(99, 102, 241, 0.3);
    --transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    line-height: 1.6;
    color: var(--text-primary);
    background: var(--bg-primary);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

body::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: 
        radial-gradient(circle at 20% 50%, rgba(99, 102, 241, 0.1) 0%, transparent 50%),
        radial-gradient(circle at 80% 80%, rgba(168, 85, 247, 0.1) 0%, transparent 50%);
    animation: backgroundShift 20s ease infinite;
    pointer-events: none;
    z-index: -1;
}

@keyframes backgroundShift {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.8; }
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes scaleIn {
    from {
        opacity: 0;
        transform: scale(0.9);
    }
    to {
        opacity: 1;
        transform: scale(1);
    }
}

h1, h2, h3, h4, h5, h6 {
    font-weight: 700;
    line-height: 1.2;
    margin-bottom: 1rem;
    background: linear-gradient(135deg, var(--text-primary) 0%, var(--text-secondary) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

h1 { font-size: 3rem; }
h2 { font-size: 2.5rem; }
h3 { font-size: 2rem; }

a {
    color: var(--primary-light);
    text-decoration: none;
    transition: var(--transition);
}

.container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 2rem;
}

/* Navbar */
.navbar {
    background: var(--glass-bg);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-bottom: 1px solid var(--glass-border);
    padding: 1rem 0;
    position: sticky;
    top: 0;
    z-index: 1000;
    box-shadow: var(--shadow-md);
}

.navbar-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.navbar-brand {
    font-size: 1.75rem;
    font-weight: 800;
    background: var(--primary-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.navbar-menu {
    display: flex;
    align-items: center;
    gap: 2rem;
}

.nav-link {
    color: var(--text-secondary);
    font-weight: 500;
    padding: 0.75rem 1.5rem;
    border-radius: var(--border-radius);
    transition: var(--transition);
}

.nav-link:hover {
    color: var(--text-primary);
    background: var(--glass-bg);
}

.navbar-user {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.75rem 1.5rem;
    background: var(--glass-bg);
    backdrop-filter: blur(10px);
    border-radius: var(--border-radius-lg);
    border: 1px solid var(--glass-border);
}

.user-name {
    font-weight: 600;
    color: var(--text-primary);
}

.user-role {
    font-size: 0.75rem;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-weight: 600;
}

.navbar-toggle {
    display: none;
    flex-direction: column;
    gap: 4px;
    background: none;
    border: none;
    cursor: pointer;
}

.navbar-toggle span {
    width: 25px;
    height: 3px;
    background: var(--text-primary);
    border-radius: 2px;
}

/* Buttons */
.btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 0.875rem 2rem;
    font-size: 1rem;
    font-weight: 600;
    border: none;
    border-radius: var(--border-radius);
    cursor: pointer;
    transition: var(--transition);
    text-decoration: none;
}

.btn-primary {
    background: var(--primary-gradient);
    color: white;
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
}

.btn-primary:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(99, 102, 241, 0.6);
    color: white;
}

.btn-outline {
    background: transparent;
    border: 2px solid var(--primary);
    color: var(--primary-light);
}

.btn-outline:hover {
    background: var(--primary-gradient);
    color: white;
    border-color: transparent;
}

.btn-danger {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    color: white;
}

.btn-sm {
    padding: 0.5rem 1.25rem;
    font-size: 0.875rem;
}

.btn-lg {
    padding: 1.25rem 3rem;
    font-size: 1.125rem;
}

.btn-block {
    display: block;
    width: 100%;
}

/* Cards */
.card {
    background: var(--bg-card);
    backdrop-filter: blur(20px);
    border-radius: var(--border-radius-lg);
    box-shadow: var(--shadow-lg);
    border: 1px solid var(--glass-border);
    transition: var(--transition);
    animation: fadeInUp 0.6s ease;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
}

.card-header {
    padding: 2rem;
    background: var(--glass-bg);
    border-bottom: 1px solid var(--glass-border);
}

.card-body {
    padding: 2rem;
}

/* Forms */
.form-input, select.form-input, textarea.form-input {
    width: 100%;
    padding: 1rem 1.25rem;
    background: var(--glass-bg);
    backdrop-filter: blur(10px);
    border: 2px solid var(--glass-border);
    border-radius: var(--border-radius);
    font-size: 1rem;
    color: var(--text-primary);
    transition: var(--transition);
}

.form-input:focus {
    outline: none;
    border-color: var(--primary);
    background: rgba(99, 102, 241, 0.1);
    box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.1);
}

.form-label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 600;
    color: var(--text-secondary);
}

.required {
    color: var(--accent-pink);
}

.form-field {
    margin-bottom: 1.5rem;
}

.error-text {
    color: var(--accent-pink);
    font-size: 0.875rem;
    display: block;
    margin-top: 0.5rem;
}

.help-text {
    color: var(--text-tertiary);
    font-size: 0.875rem;
    margin-top: 0.25rem;
    display: block;
}

.form-grid-2 {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1.5rem;
}

/* Alerts */
.alert {
    padding: 1.25rem;
    border-radius: var(--border-radius);
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    border-left: 4px solid;
}

.alert-success {
    background: rgba(16, 185, 129, 0.1);
    border-color: var(--accent-green);
    color: var(--accent-green);
}

.alert-error {
    background: rgba(239, 68, 68, 0.1);
    border-color: var(--accent-pink);
    color: var(--accent-pink);
}

.alert-close {
    margin-left: auto;
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    color: currentColor;
}

/* Badges */
.badge {
    display: inline-block;
    padding: 0.35rem 1rem;
    font-size: 0.75rem;
    font-weight: 700;
    border-radius: 20px;
    text-transform: uppercase;
}

.badge-user {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

.badge-lgu {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    color: white;
}

/* Hero */
.hero {
    background: var(--primary-gradient);
    padding: 6rem 0;
    text-align: center;
    position: relative;
}

.hero-title {
    font-size: 4rem;
    color: white;
    -webkit-text-fill-color: white;
    margin-bottom: 1.5rem;
}

.hero-subtitle {
    font-size: 1.5rem;
    color: rgba(255, 255, 255, 0.95);
    margin-bottom: 2.5rem;
}

.hero-actions {
    display: flex;
    gap: 1.5rem;
    justify-content: center;
}

/* Auth Pages */
.auth-container {
    min-height: calc(100vh - 200px);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 4rem 0;
}

.auth-card {
    background: var(--bg-card);
    backdrop-filter: blur(20px);
    border-radius: var(--border-radius-lg);
    box-shadow: var(--shadow-lg);
    padding: 3rem;
    max-width: 600px;
    width: 100%;
    border: 1px solid var(--glass-border);
    animation: scaleIn 0.5s ease;
}

.auth-header {
    text-align: center;
    margin-bottom: 2.5rem;
}

.auth-header h1 {
    margin-bottom: 0.75rem;
}

.auth-footer {
    text-align: center;
    padding-top: 2rem;
    border-top: 1px solid var(--glass-border);
    margin-top: 2rem;
}

/* Main Content */
.main-content {
    flex: 1;
    padding: 2rem 0;
}

/* Footer */
.footer {
    background: var(--bg-secondary);
    border-top: 1px solid var(--glass-border);
    padding: 3rem 0;
    text-align: center;
    color: var(--text-secondary);
    margin-top: auto;
}

/* Messages */
.messages-container {
    position: fixed;
    top: 100px;
    right: 20px;
    z-index: 2000;
    max-width: 450px;
}

/* Page Header */
.page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 3rem;
    padding-bottom: 2rem;
    border-bottom: 2px solid var(--glass-border);
}

.page-subtitle {
    color: var(--text-secondary);
    margin-top: 0.5rem;
}

/* Features */
.features {
    padding: 6rem 0;
    background: var(--bg-secondary);
}

.section-title {
    text-align: center;
    font-size: 3rem;
    margin-bottom: 4rem;
}

.features-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 3rem;
}

.feature-card {
    text-align: center;
    padding: 3rem;
    border-radius: var(--border-radius-lg);
    background: var(--bg-card);
    border: 1px solid var(--glass-border);
    transition: var(--transition);
}

.feature-card:hover {
    transform: translateY(-10px);
    box-shadow: var(--shadow-glow);
}

.feature-icon {
    font-size: 4rem;
    margin-bottom: 1.5rem;
}

/* Categories */
.categories {
    padding: 6rem 0;
}

.categories-grid {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 2rem;
}

.category-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 2rem;
    background: var(--bg-card);
    border-radius: var(--border-radius-lg);
    border: 1px solid var(--glass-border);
    transition: var(--transition);
}

.category-item:hover {
    transform: translateY(-10px);
    box-shadow: var(--shadow-glow);
}

.category-icon {
    font-size: 3.5rem;
    margin-bottom: 1rem;
}

/* CTA */
.cta {
    background: var(--secondary-gradient);
    color: white;
    padding: 6rem 0;
    text-align: center;
}

.cta-content h2 {
    font-size: 3rem;
    color: white;
    -webkit-text-fill-color: white;
    margin-bottom: 1rem;
}

/* Responsive */
@media (max-width: 768px) {
    .navbar-menu {
        display: none;
        position: fixed;
        top: 70px;
        left: 0;
        right: 0;
        background: var(--bg-secondary);
        flex-direction: column;
        padding: 2rem;
    }
    
    .navbar-menu.active {
        display: flex;
    }
    
    .navbar-toggle {
        display: flex;
    }
    
    .hero-title {
        font-size: 2.5rem;
    }
    
    .features-grid {
        grid-template-columns: 1fr;
    }
    
    .categories-grid {
        grid-template-columns: repeat(2, 1fr);
    }
    
    .form-grid-2 {
        grid-template-columns: 1fr;
    }
}'''

print("\n2. Writing CSS file...")
css_file = css_dir / 'style.css'
css_file.write_text(modern_css, encoding='utf-8')
print(f"   ✓ Created: {css_file}")
print(f"   ✓ Size: {len(modern_css):,} characters")

# Create JS file
modern_js = '''// Modern JavaScript
document.addEventListener('DOMContentLoaded', function() {
    console.log('🎨 Modern design loaded!');
    
    // Alert auto-dismiss
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transform = 'translateX(100%)';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });
    
    // Image preview
    const imageInputs = document.querySelectorAll('input[type="file"]');
    imageInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file && file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    let preview = input.parentElement.querySelector('.image-preview');
                    if (!preview) {
                        preview = document.createElement('div');
                        preview.className = 'image-preview';
                        input.parentElement.appendChild(preview);
                    }
                    preview.innerHTML = `<img src="${e.target.result}" style="max-width: 300px; margin-top: 1rem; border-radius: 16px;">`;
                };
                reader.readAsDataURL(file);
            }
        });
    });
});

// Toggle mobile menu
function toggleMenu() {
    const menu = document.getElementById('navbarMenu');
    menu.classList.toggle('active');
}'''

print("\n3. Writing JS file...")
js_file = js_dir / 'main.js'
js_file.write_text(modern_js, encoding='utf-8')
print(f"   ✓ Created: {js_file}")

print("\n" + "=" * 80)
print("✅ STATIC FILES CREATED SUCCESSFULLY!")
print("=" * 80)

print(f"""
Created:
   ✓ {css_file}
   ✓ {js_file}
   ✓ Directories ready

File sizes:
   • CSS: {len(modern_css):,} characters
   • JS: {len(modern_js):,} characters

""")

print("=" * 80)
print("🔥 NOW DO THIS TO SEE THE NEW DESIGN:")
print("=" * 80)
print("""
1. STOP Django server (Ctrl+C)

2. CLEAR BROWSER CACHE COMPLETELY:
   • Chrome: Ctrl + Shift + Delete
   • Select "Cached images and files"
   • Time range: "All time"
   • Click "Clear data"

3. START server again:
   python manage.py runserver

4. Open in INCOGNITO/PRIVATE MODE:
   • Chrome: Ctrl + Shift + N
   • Go to: http://127.0.0.1:8000/

5. If STILL old design, do HARD REFRESH:
   • Ctrl + Shift + R (or Ctrl + F5)
   • Multiple times!

The design WILL change now! The cache was the problem!
""")

print("=" * 80)