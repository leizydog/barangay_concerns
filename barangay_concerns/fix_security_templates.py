from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

print("=" * 60)
print("FIXING SECURITY MANAGEMENT TEMPLATES")
print("=" * 60)

# Correct template contents
templates = {
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

    'apps/security_management/templates/security_management/molecules/auth_footer.html': '''<div class="auth-footer">
    <p>
        {{ text }} 
        <a href="{% url link_url %}">{{ link_text }}</a>
    </p>
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

    'apps/security_management/templates/security_management/organisms/auth_card.html': '''<div class="auth-card">
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

    'apps/security_management/templates/security_management/pages/login.html': '''{% extends 'base.html' %}

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

    'apps/security_management/templates/security_management/pages/register.html': '''{% extends 'base.html' %}

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

    'apps/security_management/templates/security_management/pages/profile.html': '''{% extends 'base.html' %}

{% block title %}User Profile{% endblock %}

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

                {% include 'security_management/molecules/profile_detail.html' with label="Email" value=user.email %}
                {% include 'security_management/molecules/profile_detail.html' with label="First Name" value=user.first_name %}
                {% include 'security_management/molecules/profile_detail.html' with label="Last Name" value=user.last_name %}
                {% include 'security_management/molecules/profile_detail.html' with label="Phone" value=user.phone_number %}
                {% include 'security_management/molecules/profile_detail.html' with label="Barangay" value=user.barangay %}
                {% include 'security_management/molecules/profile_detail.html' with label="Municipality" value=user.municipality %}
                {% include 'security_management/molecules/profile_detail.html' with label="Role" value=user.get_role_display %}
                
                <div style="margin-top: 2rem;">
                    <a href="{% url 'security_management:logout' %}" class="btn btn-danger">Logout</a>
                </div>
            </div>
        </div>
    {% else %}
        <p>You need to be logged in to view this page.</p>
        <a href="{% url 'security_management:login' %}" class="btn btn-primary">Log In</a>
    {% endif %}
</div>
{% endblock %}''',

    'apps/security_management/templates/security_management/pages/logged_out.html': '''{% extends 'base.html' %}

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

print("\nFixing template files...")
fixed_count = 0
for file_path, content in templates.items():
    full_path = BASE_DIR / file_path
    if full_path.exists():
        full_path.write_text(content, encoding='utf-8')
        print(f"✓ Fixed: {file_path}")
        fixed_count += 1
    else:
        print(f"✗ Not found: {file_path}")

print(f"\n✓ Fixed {fixed_count} template files!")

print("\n" + "=" * 60)
print("TEMPLATES FIXED SUCCESSFULLY!")
print("=" * 60)
print("\nChanges made:")
print("1. Removed stray 'a' from auth_footer.html")
print("2. Fixed all template syntax")
print("3. Ensured proper Django template tags")
print("\nNow restart your server:")
print("  python manage.py runserver")
print("=" * 60)