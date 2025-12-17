from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

templates = {
    'templates/concerns/archive.html': '''{% extends 'base.html' %}

{% block title %}Archived Concerns{% endblock %}

{% block content %}
<div class="container">
    <div class="page-header">
        <div>
            <h1>📦 Archived Concerns</h1>
            <p class="page-subtitle">View and manage archived concerns</p>
        </div>
        <a href="{% url 'concerns:list' %}" class="btn btn-outline">
            ← Back to Active Concerns
        </a>
    </div>
    
    {% if concerns %}
        <div class="concerns-grid">
            {% for concern in concerns %}
                <div class="concern-card">
                    <div class="concern-card-header">
                        <span class="badge badge-{{ concern.category|lower }}">{{ concern.get_category_display }}</span>
                        <span class="badge" style="background: #64748b; color: white;">Archived</span>
                    </div>
                    <h3 class="concern-title">{{ concern.title }}</h3>
                    <p class="concern-location">📍 {{ concern.location }}, {{ concern.barangay }}</p>
                    <p class="concern-description">{{ concern.description|truncatewords:20 }}</p>
                    
                    <div class="concern-card-footer">
                        <span class="concern-date">Archived: {{ concern.archived_at|date:"M d, Y" }}</span>
                    </div>
                    
                    <div style="margin-top: 1rem; display: flex; gap: 0.5rem;">
                        <a href="{% url 'concerns:detail' concern.pk %}" class="btn btn-sm btn-primary">View</a>
                        <form method="post" action="{% url 'concerns:unarchive' concern.pk %}" style="display: inline;">
                            {% csrf_token %}
                            <button type="submit" class="btn btn-sm btn-outline">Restore</button>
                        </form>
                        <form method="post" action="{% url 'concerns:permanent_delete' concern.pk %}" style="display: inline;">
                            {% csrf_token %}
                            <button type="submit" class="btn btn-sm btn-danger" onclick="return confirm('Permanently delete? This cannot be undone!')">Delete Forever</button>
                        </form>
                    </div>
                </div>
            {% endfor %}
        </div>
    {% else %}
        <div class="empty-state">
            <p>No archived concerns found.</p>
            <a href="{% url 'concerns:list' %}" class="btn btn-primary">View Active Concerns</a>
        </div>
    {% endif %}
</div>
{% endblock %}''',

    'templates/concerns/unarchive.html': '''{% extends 'base.html' %}

{% block title %}Restore Concern{% endblock %}

{% block content %}
<div class="container">
    <div class="confirm-container">
        <div class="confirm-card">
            <h1>🔄 Restore Concern from Archive</h1>
            <p>Are you sure you want to restore this concern?</p>
            <div class="concern-preview">
                <h3>{{ concern.title }}</h3>
                <p>{{ concern.description|truncatewords:30 }}</p>
                <p><strong>Archived on:</strong> {{ concern.archived_at|date:"F d, Y H:i" }}</p>
                <p><strong>Archived by:</strong> {{ concern.archived_by.username }}</p>
            </div>
            <form method="post">
                {% csrf_token %}
                <div class="form-actions">
                    <button type="submit" class="btn btn-primary">Yes, Restore</button>
                    <a href="{% url 'concerns:archive_list' %}" class="btn btn-outline">Cancel</a>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}''',

    'templates/concerns/permanent_delete.html': '''{% extends 'base.html' %}

{% block title %}Permanent Delete{% endblock %}

{% block content %}
<div class="container">
    <div class="confirm-container">
        <div class="confirm-card">
            <h1 style="color: #ef4444;">⚠️ Permanent Deletion</h1>
            <p style="color: #ef4444; font-weight: bold;">This action CANNOT be undone!</p>
            <p>Are you sure you want to permanently delete this concern from the database?</p>
            <div class="concern-preview" style="border-left-color: #ef4444;">
                <h3>{{ concern.title }}</h3>
                <p>{{ concern.description|truncatewords:30 }}</p>
                <p><strong>Created:</strong> {{ concern.created_at|date:"F d, Y" }}</p>
                <p><strong>Reporter:</strong> {{ concern.reporter.username }}</p>
            </div>
            <form method="post">
                {% csrf_token %}
                <div class="form-actions">
                    <button type="submit" class="btn btn-danger" onclick="return confirm('Are you ABSOLUTELY sure? This CANNOT be undone!')">Yes, Delete Forever</button>
                    <a href="{% url 'concerns:archive_list' %}" class="btn btn-outline">Cancel</a>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}''',
}

print("=" * 80)
print("CREATING ARCHIVE TEMPLATES")
print("=" * 80)

for file_path, content in templates.items():
    full_path = BASE_DIR / file_path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    full_path.write_text(content, encoding='utf-8')
    print(f"✓ Created: {file_path}")

print("\n✓ All archive templates created!")
print("=" * 80)