from pathlib import Path
import shutil

BASE_DIR = Path(__file__).resolve().parent

print("=" * 60)
print("FIXING SECURITY MANAGEMENT TEMPLATES")
print("=" * 60)

# Create directory structure
template_dirs = [
    'templates/security_management',
    'templates/security_management/atoms',
    'templates/security_management/molecules',
    'templates/security_management/organisms',
    'templates/security_management/pages',
]

for dir_path in template_dirs:
    full_path = BASE_DIR / dir_path
    full_path.mkdir(parents=True, exist_ok=True)
    print(f"✓ Created: {dir_path}")

# Template contents
templates = {
    'templates/security_management/atoms/alert.html': '''<div class="alert alert-{{ type|default:'info' }}">
    {{ message }}
</div>''',

    'templates/security_management/atoms/auth_header.html': '''<div class="auth-header">
    <h1>{{ title }}</h1>
    <p>{{ text }}</p>
</div>''',

    'templates/security_management/atoms/button.html': '''<button type="{{ type|default:'button' }}" class="btn {{ class|default:'btn-secondary' }}">
    {{ text }}
</button>''',

    'templates/security_management/molecules/auth_footer.html': '''<div class="auth-footer">
    <p>
        {{ text }} 
        <a href="{% url link_url %}">{{ link_text }}</a>
    </p>
</div>''',

    'templates/security_management/molecules/form_field.html': '''<div class="form-field">
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

    'templates/security_management/molecules/profile_detail.html': '''<div class="profile-detail-row">
    <span class="profile-label"><strong>{{ label }}:</strong></span>
    <span class="profile-value">{{ value|default:"N/A" }}</span>
</div>''',

    'templates/security_management/organisms/auth_card.html': '''<div class="auth-card">
    {% include 'security_management/atoms/auth_header.html' with title=header_title text=header_text %}
    
    <form method="post" class="auth-form">
        {% csrf_token %}
        
        {% if form.non_field_errors %}
            <div class="alert alert-error">
                {{ form.non_field_errors }}
            </div>
        {% endif %}
        
        <div class="form-grid-2">
            {% for field in form %}
                {% include 'security_management/molecules/form_field.html' with field=field %}
            {% endfor %}
        </div>
        
        <button type="submit" class="btn btn-primary btn-block">{{ submit_text }}</button>
    </form>
    
    {% include 'security_management/molecules/auth_footer.html' with 
        text=footer_text 
        link_text=footer_link_text 
        link_url=footer_link_url 
    %}
</div>''',

    'templates/security_management/pages/login.html': '''{% extends 'base.html' %}

{% block title %}Login - Barangay Concerns{% endblock %}

{% block content %}
<div class="auth-container">
    {% include 'security_management/organisms/auth_card.html' with 
        header_title="Welcome Back"
        header_text="Login to report and track community concerns"
        form=form
        submit_text="Login"
        footer_text="Don't have an account?"
        footer_link_text="Register here"
        footer_link_url="security_management:register" 
    %}
</div>
{% endblock %}''',

    'templates/security_management/pages/register.html': '''{% extends 'base.html' %}

{% block title %}Register - Barangay Concerns{% endblock %}

{% block content %}
<div class="auth-container">
    {% include 'security_management/organisms/auth_card.html' with 
        header_title="Create Account"
        header_text="Join us in building a better community"
        form=form
        submit_text="Register"
        footer_text="Already have an account?"
        footer_link_text="Login here"
        footer_link_url="security_management:login" 
    %}
</div>
{% endblock %}''',

    'templates/security_management/pages/profile.html': '''{% extends 'base.html' %}

{% block title %}User Profile{% endblock %}

{% block content %}
<div class="container">
    <div class="page-header">
        <h1>User Profile</h1>
    </div>
    
    {% if user.is_authenticated %}
        <div class="profile-card">
            <h2>Welcome, {{ user.username }}!</h2>
            <hr>

            {% include 'security_management/molecules/profile_detail.html' with label="Email" value=user.email %}
            {% include 'security_management/molecules/profile_detail.html' with label="First Name" value=user.first_name %}
            {% include 'security_management/molecules/profile_detail.html' with label="Last Name" value=user.last_name %}
            {% include 'security_management/molecules/profile_detail.html' with label="Phone" value=user.phone_number %}
            {% include 'security_management/molecules/profile_detail.html' with label="Barangay" value=user.barangay %}
            {% include 'security_management/molecules/profile_detail.html' with label="Municipality" value=user.municipality %}
            {% include 'security_management/molecules/profile_detail.html' with label="Role" value=user.get_role_display %}
            
            <div class="profile-actions">
                <a href="{% url 'security_management:logout' %}" class="btn btn-danger">Logout</a>
            </div>
        </div>
    {% else %}
        <p>You need to be logged in to view this page.</p>
        <a href="{% url 'security_management:login' %}" class="btn btn-primary">Log In</a>
    {% endif %}
</div>
{% endblock %}''',

    'templates/security_management/pages/logged_out.html': '''{% extends 'base.html' %}

{% block title %}Logged Out{% endblock %}

{% block content %}
<div class="auth-container">
    <div class="auth-card">
        <div class="auth-header">
            <h1>You have been logged out</h1>
            <p>Thank you for using our service.</p>
        </div>
        <div class="auth-footer">
            <a href="{% url 'security_management:login' %}" class="btn btn-primary btn-block">Log In Again</a>
        </div>
    </div>
</div>
{% endblock %}''',
}

print("\nCreating template files...")
for file_path, content in templates.items():
    full_path = BASE_DIR / file_path
    full_path.write_text(content, encoding='utf-8')
    print(f"✓ Created: {file_path}")

print("\n" + "=" * 60)
print("TEMPLATES CREATED SUCCESSFULLY!")
print("=" * 60)
print("\nNext steps:")
print("1. Update config/settings.py (replace apps.accounts with apps.security_management)")
print("2. Update config/urls.py")
print("3. Update templates/organisms/navbar.html")
print("4. Run: python manage.py makemigrations")
print("5. Run: python manage.py migrate")
print("6. Run: python manage.py runserver")
print("=" * 60)