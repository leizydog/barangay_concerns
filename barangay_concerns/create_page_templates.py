from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

page_templates = {
    'templates/pages/home.html': '''{% extends 'base.html' %}

{% block title %}Home - Barangay Concerns{% endblock %}

{% block content %}
<div class="hero">
    <div class="container hero-content">
        <h1 class="hero-title">Community Concerns Platform</h1>
        <p class="hero-subtitle">
            Report and track community issues in your barangay. 
            Help us build a better, safer, and more responsive community.
        </p>
        
        {% if user.is_authenticated %}
            <div class="hero-actions">
                <a href="{% url 'concerns:list' %}" class="btn btn-primary btn-lg">Go to Dashboard</a>
                <a href="{% url 'concerns:create' %}" class="btn btn-outline btn-lg">Report Concern</a>
            </div>
        {% else %}
            <div class="hero-actions">
                <a href="{% url 'accounts:register' %}" class="btn btn-primary btn-lg">Get Started</a>
                <a href="{% url 'accounts:login' %}" class="btn btn-outline btn-lg">Login</a>
            </div>
        {% endif %}
    </div>
</div>

<section class="features">
    <div class="container">
        <h2 class="section-title">How It Works</h2>
        
        <div class="features-grid">
            <div class="feature-card">
                <div class="feature-icon">📝</div>
                <h3>Report Issues</h3>
                <p>Easily report community concerns like floods, road damage, or safety issues with photos and detailed descriptions.</p>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">👁️</div>
                <h3>Track Progress</h3>
                <p>Monitor the status of your reported concerns in real-time and receive updates from LGU officials.</p>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">✅</div>
                <h3>Get Results</h3>
                <p>See how your concerns are being addressed and contribute to making your community better.</p>
            </div>
        </div>
    </div>
</section>

<section class="categories">
    <div class="container">
        <h2 class="section-title">Report Categories</h2>
        
        <div class="categories-grid">
            <div class="category-item">
                <span class="category-icon">🌊</span>
                <span class="category-name">Flooding</span>
            </div>
            <div class="category-item">
                <span class="category-icon">🛣️</span>
                <span class="category-name">Road Infrastructure</span>
            </div>
            <div class="category-item">
                <span class="category-icon">🗑️</span>
                <span class="category-name">Waste Management</span>
            </div>
            <div class="category-item">
                <span class="category-icon">⚡</span>
                <span class="category-name">Electricity</span>
            </div>
            <div class="category-item">
                <span class="category-icon">💧</span>
                <span class="category-name">Water Supply</span>
            </div>
            <div class="category-item">
                <span class="category-icon">🚨</span>
                <span class="category-name">Public Safety</span>
            </div>
        </div>
    </div>
</section>

<section class="cta">
    <div class="container cta-content">
        <h2>Ready to Make a Difference?</h2>
        <p>Join thousands of citizens working together to improve our communities.</p>
        {% if not user.is_authenticated %}
        <a href="{% url 'accounts:register' %}" class="btn btn-primary btn-lg">Create Account</a>
        {% endif %}
    </div>
</section>
{% endblock %}''',

    'templates/concerns/list.html': '''{% extends 'base.html' %}

{% block title %}Concerns Dashboard{% endblock %}

{% block content %}
<div class="container">
    <div class="page-header">
        <div>
            <h1>Community Concerns</h1>
            <p class="page-subtitle">Track and manage barangay issues</p>
        </div>
        <a href="{% url 'concerns:create' %}" class="btn btn-primary">
            + Report New Concern
        </a>
    </div>
    
    {% include 'organisms/concern_list.html' %}
</div>
{% endblock %}''',

    'templates/concerns/detail.html': '''{% extends 'base.html' %}

{% block title %}{{ concern.title }} - Concerns{% endblock %}

{% block content %}
<div class="container">
    <div class="detail-header">
        <a href="{% url 'concerns:list' %}" class="btn btn-outline btn-sm">← Back to List</a>
        <div class="detail-actions">
            <a href="{% url 'concerns:update' concern.pk %}" class="btn btn-primary btn-sm">Edit</a>
            <form method="post" action="{% url 'concerns:delete' concern.pk %}" style="display: inline;">
                {% csrf_token %}
                <button type="submit" class="btn btn-danger btn-sm" onclick="return confirm('Are you sure?')">Delete</button>
            </form>
        </div>
    </div>
    
    <div class="concern-detail">
        <div class="concern-detail-header">
            <h1>{{ concern.title }}</h1>
            <div class="badges">
                <span class="badge badge-{{ concern.category|lower }}">{{ concern.get_category_display }}</span>
                <span class="badge badge-status-{{ concern.status|lower }}">{{ concern.get_status_display }}</span>
                <span class="badge badge-priority-{{ concern.priority|lower }}">{{ concern.get_priority_display }}</span>
            </div>
        </div>
        
        <div class="concern-detail-grid">
            <div class="concern-main">
                {% if concern.image %}
                <div class="concern-image">
                    <img src="{{ concern.image.url }}" alt="{{ concern.title }}">
                </div>
                {% endif %}
                
                <div class="concern-section">
                    <h3>Description</h3>
                    <p>{{ concern.description }}</p>
                </div>
                
                <div class="concern-section">
                    <h3>Location Details</h3>
                    <div class="info-grid">
                        <div class="info-item">
                            <span class="info-label">Location:</span>
                            <span class="info-value">{{ concern.location }}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">Barangay:</span>
                            <span class="info-value">{{ concern.barangay }}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">Municipality:</span>
                            <span class="info-value">{{ concern.municipality }}</span>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="concern-sidebar">
                <div class="sidebar-section">
                    <h3>Concern Information</h3>
                    <div class="info-list">
                        <div class="info-item">
                            <span class="info-label">Reported by:</span>
                            <span class="info-value">{{ concern.reporter.username }}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">Reported on:</span>
                            <span class="info-value">{{ concern.created_at|date:"F d, Y H:i" }}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">Last updated:</span>
                            <span class="info-value">{{ concern.updated_at|date:"F d, Y H:i" }}</span>
                        </div>
                        {% if concern.resolved_at %}
                        <div class="info-item">
                            <span class="info-label">Resolved on:</span>
                            <span class="info-value">{{ concern.resolved_at|date:"F d, Y H:i" }}</span>
                        </div>
                        {% endif %}
                        {% if concern.assigned_to %}
                        <div class="info-item">
                            <span class="info-label">Assigned to:</span>
                            <span class="info-value">{{ concern.assigned_to.username }}</span>
                        </div>
                        {% endif %}
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',

    'templates/concerns/create.html': '''{% extends 'base.html' %}

{% block title %}Report Concern{% endblock %}

{% block content %}
<div class="container">
    <div class="page-header">
        <div>
            <h1>Report a Concern</h1>
            <p class="page-subtitle">Help us improve our community</p>
        </div>
    </div>
    
    <div class="form-container">
        {% include 'organisms/concern_form.html' with submit_text="Submit Concern" %}
    </div>
</div>
{% endblock %}''',

    'templates/concerns/update.html': '''{% extends 'base.html' %}

{% block title %}Update Concern{% endblock %}

{% block content %}
<div class="container">
    <div class="page-header">
        <div>
            <h1>Update Concern</h1>
            <p class="page-subtitle">{{ concern.title }}</p>
        </div>
    </div>
    
    <div class="form-container">
        {% include 'organisms/concern_form.html' with submit_text="Update Concern" %}
    </div>
</div>
{% endblock %}''',

    'templates/concerns/delete.html': '''{% extends 'base.html' %}

{% block title %}Delete Concern{% endblock %}

{% block content %}
<div class="container">
    <div class="confirm-container">
        <div class="confirm-card">
            <h1>Confirm Deletion</h1>
            <p>Are you sure you want to delete this concern?</p>
            <div class="concern-preview">
                <h3>{{ concern.title }}</h3>
                <p>{{ concern.description|truncatewords:30 }}</p>
            </div>
            <form method="post">
                {% csrf_token %}
                <div class="form-actions">
                    <button type="submit" class="btn btn-danger">Yes, Delete</button>
                    <a href="{% url 'concerns:detail' concern.pk %}" class="btn btn-outline">Cancel</a>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}''',
}

print("=" * 60)
print("CREATING PAGE TEMPLATES")
print("=" * 60)

created_count = 0
for file_path, content in page_templates.items():
    full_path = BASE_DIR / file_path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    full_path.write_text(content, encoding='utf-8')
    print(f"✓ Created: {file_path}")
    created_count += 1

print(f"\n✓ Created {created_count} page template files successfully!")
print("=" * 60)