from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

print("=" * 60)
print("CREATING WORKING ATOMIC DESIGN TEMPLATES")
print("=" * 60)

templates = {
    # ==================== ATOMS ====================
    'apps/security_management/templates/security_management/atoms/alert.html': '''<div class="alert alert-{{ type|default:'info' }}" role="alert">
    <span class="alert-icon">
        {% if type == 'success' %}✓{% elif type == 'error' %}✕{% elif type == 'warning' %}⚠{% else %}ℹ{% endif %}
    </span>
    <span class="alert-text">{{ message }}</span>
    <button class="alert-close" onclick="this.parentElement.remove()">×</button>
</div>''',

    'apps/security_management/templates/security_management/atoms/auth_header.html': '''<div class="auth-header">
    <h1>{{ title }}</h1>
    <p>{{ text }}</p>
</div>''',

    'apps/security_management/templates/security_management/atoms/button.html': '''<button type="{{ type|default:'button' }}" class="btn {{ class|default:'btn-secondary' }}">
    {{ text }}
</button>''',

    # ==================== MOLECULES ====================
    'apps/security_management/templates/security_management/molecules/auth_footer.html': '''<div class="auth-footer">
    <p>{{ text }} <a href="{% url link_url %}">{{ link_text }}</a></p>
</div>''',

    'apps/security_management/templates/security_management/molecules/form_field.html': '''<div class="form-field">
    <label for="{{ field.id_for_label }}" class="form-label">
        {{ field.label }}
        {% if field.field.required %}<span class="required">*</span>{% endif %}
    </label>
    {{ field }}
    {% if field.errors %}
        <div class="field-errors">
            {% for error in field.errors %}
                <span class="error-text">{{ error }}</span>
            {% endfor %}
        </div>
    {% endif %}
    {% if field.help_text %}
        <span class="help-text">{{ field.help_text|safe }}</span>
    {% endif %}
</div>''',

    'apps/security_management/templates/security_management/molecules/profile_detail.html': '''<div class="profile-detail-row">
    <span class="profile-label"><strong>{{ label }}:</strong></span>
    <span class="profile-value">{{ value|default:"N/A" }}</span>
</div>''',

    # ==================== ORGANISMS ====================
    'apps/security_management/templates/security_management/organisms/auth_card.html': '''<div class="auth-card">
    <div class="auth-header">
        <h1>{{ header_title }}</h1>
        <p>{{ header_text }}</p>
    </div>
    
    <form method="post" class="auth-form">
        {% csrf_token %}
        
        {% if form.non_field_errors %}
            <div class="alert alert-error">
                {{ form.non_field_errors }}
            </div>
        {% endif %}
        
        <div class="form-grid-2">
            {% for field in form %}
                <div class="form-field">
                    <label for="{{ field.id_for_label }}" class="form-label">
                        {{ field.label }}
                        {% if field.field.required %}<span class="required">*</span>{% endif %}
                    </label>
                    {{ field }}
                    {% if field.errors %}
                        <div class="field-errors">
                            {% for error in field.errors %}
                                <span class="error-text">{{ error }}</span>
                            {% endfor %}
                        </div>
                    {% endif %}
                    {% if field.help_text %}
                        <span class="help-text">{{ field.help_text|safe }}</span>
                    {% endif %}
                </div>
            {% endfor %}
        </div>
        
        <button type="submit" class="btn btn-primary btn-block">{{ submit_text }}</button>
    </form>
    
    <div class="auth-footer">
        <p>{{ footer_text }} <a href="{% url footer_link_url %}">{{ footer_link_text }}</a></p>
    </div>
</div>''',

    # ==================== PAGES ====================
    'apps/security_management/templates/security_management/pages/login.html': '''{% extends 'base.html' %}

{% block title %}Login - Barangay Concerns{% endblock %}

{% block content %}
<div class="auth-container">
    {% with header_title="Welcome Back" header_text="Login to report and track community concerns" submit_text="Login" footer_text="Don't have an account?" footer_link_text="Register here" footer_link_url="security_management:register" %}
        {% include 'security_management/organisms/auth_card.html' %}
    {% endwith %}
</div>
{% endblock %}''',

    'apps/security_management/templates/security_management/pages/register.html': '''{% extends 'base.html' %}

{% block title %}Register - Barangay Concerns{% endblock %}

{% block content %}
<div class="auth-container">
    {% with header_title="Create Account" header_text="Join us in building a better community" submit_text="Register" footer_text="Already have an account?" footer_link_text="Login here" footer_link_url="security_management:login" %}
        {% include 'security_management/organisms/auth_card.html' %}
    {% endwith %}
</div>
{% endblock %}''',

    'apps/security_management/templates/security_management/pages/profile.html': '''{% extends 'base.html' %}

{% block title %}User Profile - Barangay Concerns{% endblock %}

{% block content %}
<div class="container">
    <div class="page-header">
        <h1>User Profile</h1>
    </div>
    
    {% if user.is_authenticated %}
        <div class="card">
            <div class="card-body">
                <h2>Welcome, {{ user.username }}!</h2>
                <hr>

                <div class="profile-details">
                    {% with label="Username" value=user.username %}
                        {% include 'security_management/molecules/profile_detail.html' %}
                    {% endwith %}
                    
                    {% with label="Email" value=user.email %}
                        {% include 'security_management/molecules/profile_detail.html' %}
                    {% endwith %}
                    
                    {% with label="First Name" value=user.first_name %}
                        {% include 'security_management/molecules/profile_detail.html' %}
                    {% endwith %}
                    
                    {% with label="Last Name" value=user.last_name %}
                        {% include 'security_management/molecules/profile_detail.html' %}
                    {% endwith %}
                    
                    {% with label="Phone" value=user.phone_number %}
                        {% include 'security_management/molecules/profile_detail.html' %}
                    {% endwith %}
                    
                    {% with label="Barangay" value=user.barangay %}
                        {% include 'security_management/molecules/profile_detail.html' %}
                    {% endwith %}
                    
                    {% with label="Municipality" value=user.municipality %}
                        {% include 'security_management/molecules/profile_detail.html' %}
                    {% endwith %}
                    
                    <div class="profile-detail-row">
                        <span class="profile-label"><strong>Role:</strong></span>
                        <span class="profile-value">
                            <span class="badge badge-{{ user.role|lower }}">{{ user.get_role_display }}</span>
                        </span>
                    </div>
                </div>
                
                <div style="margin-top: 2rem;">
                    <a href="{% url 'concerns:list' %}" class="btn btn-primary">View Concerns</a>
                    <a href="{% url 'security_management:logout' %}" class="btn btn-outline">Logout</a>
                </div>
            </div>
        </div>
    {% else %}
        <div class="empty-state">
            <p>You need to be logged in to view this page.</p>
            <a href="{% url 'security_management:login' %}" class="btn btn-primary">Log In</a>
        </div>
    {% endif %}
</div>
{% endblock %}''',

    'apps/security_management/templates/security_management/pages/logged_out.html': '''{% extends 'base.html' %}

{% block title %}Logged Out - Barangay Concerns{% endblock %}

{% block content %}
<div class="auth-container">
    <div class="auth-card">
        {% with title="You have been logged out" text="Thank you for using our service. You can log back in anytime." %}
            {% include 'security_management/atoms/auth_header.html' %}
        {% endwith %}
        
        <div class="auth-footer" style="border-top: none; padding-top: 0;">
            <a href="{% url 'security_management:login' %}" class="btn btn-primary btn-block">Log In Again</a>
            <a href="{% url 'home' %}" class="btn btn-outline btn-block" style="margin-top: 0.5rem;">Go to Home</a>
        </div>
    </div>
</div>
{% endblock %}''',
}

print("\nCreating atomic design template files...")
created_count = 0
for file_path, content in templates.items():
    full_path = BASE_DIR / file_path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    full_path.write_text(content, encoding='utf-8')
    print(f"✓ Created: {file_path}")
    created_count += 1

print(f"\n✓ Created {created_count} template files!")

print("\n" + "=" * 60)
print("ATOMIC DESIGN STRUCTURE")
print("=" * 60)
print("""
Atoms (Basic building blocks):
  ✓ alert.html - Alert messages with icons
  ✓ auth_header.html - Header for auth pages
  ✓ button.html - Reusable button component

Molecules (Simple combinations):
  ✓ auth_footer.html - Footer with link
  ✓ form_field.html - Form field with label and errors
  ✓ profile_detail.html - Profile row detail

Organisms (Complex components):
  ✓ auth_card.html - Complete auth card with form

Pages (Full pages):
  ✓ login.html - Login page
  ✓ register.html - Registration page
  ✓ profile.html - User profile page
  ✓ logged_out.html - Logged out page
""")

print("=" * 60)
print("KEY IMPROVEMENTS")
print("=" * 60)
print("""
1. Using {% with %} blocks instead of complex 'with' parameters
2. All includes on single lines
3. No stray characters
4. Proper context passing
5. Reusable atomic components

The {% with %} tag creates a local scope for variables,
making them available to the included template without
the parsing issues of multi-line 'with' parameters.
""")

print("=" * 60)
print("NEXT STEPS")
print("=" * 60)
print("""
1. Run this script: python create_working_atomic.py
2. Restart Django server
3. Test login/register pages
4. All atomic design principles maintained!
""")
print("=" * 60)