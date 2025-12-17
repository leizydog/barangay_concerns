import os

# Define the base directory for templates
BASE_DIR = 'templates/concerns'

# Ensure the base directory exists
os.makedirs(BASE_DIR, exist_ok=True)

# Dictionary of template files and their contents
templates = {
    'base.html': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Barangay Concerns{% endblock %}</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="{% static 'css/styles.css' %}">
    {% block head %}{% endblock %}
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container">
            <a class="navbar-brand" href="/">Barangay Concerns</a>
            <div class="collapse navbar-collapse">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item"><a class="nav-link" href="{% url 'concerns:list' %}">Concerns List</a></li>
                    <li class="nav-item"><a class="nav-link" href="{% url 'concerns:map' %}">Map View</a></li>
                </ul>
            </div>
        </div>
    </nav>
    <main class="container my-4">
        {% block content %}{% endblock %}
    </main>
</body>
</html>''',

    'list.html': '''{% extends 'base.html' %}
{% block title %}Concerns List{% endblock %}
{% block content %}
<h1>Concerns List</h1>
<p>List of all reported concerns will go here.</p>
{% endblock %}''',

    'create.html': '''{% extends 'base.html' %}
{% block title %}Report New Concern{% endblock %}
{% block content %}
<h1>Report a New Concern</h1>
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit" class="btn btn-primary">Submit</button>
</form>
{% endblock %}''',

    'map.html': '''<!-- templates/concerns/map.html -->
{% extends 'base.html' %}

{% block title %}Map View - Barangay Concerns{% endblock %}

{% block content %}
<div class="container">
    <div class="page-header">
        <div>
            <h1>🗺️ Concerns Map</h1>
            <p class="page-subtitle">Interactive map of all reported concerns</p>
        </div>
        <a href="{% url 'concerns:create' %}" class="btn btn-primary">
            + Report New Concern
        </a>
    </div>
    
    <!-- Map Filters -->
    <div class="map-filters">
        <form method="get" class="filters-form">
            <div class="filter-group">
                <select name="status" class="form-input" onchange="this.form.submit()">
                    <option value="">All Status</option>
                    <option value="PENDING" {% if status_filter == 'PENDING' %}selected{% endif %}>Pending</option>
                    <option value="IN_PROGRESS" {% if status_filter == 'IN_PROGRESS' %}selected{% endif %}>In Progress</option>
                    <option value="RESOLVED" {% if status_filter == 'RESOLVED' %}selected{% endif %}>Resolved</option>
                    <option value="CLOSED" {% if status_filter == 'CLOSED' %}selected{% endif %}>Closed</option>
                </select>
            </div>
            
            <div class="filter-group">
                <select name="category" class="form-input" onchange="this.form.submit()">
                    <option value="">All Categories</option>
                    <option value="FLOOD" {% if category_filter == 'FLOOD' %}selected{% endif %}>Flooding</option>
                    <option value="ROAD" {% if category_filter == 'ROAD' %}selected{% endif %}>Road Infrastructure</option>
                    <option value="WASTE" {% if category_filter == 'WASTE' %}selected{% endif %}>Waste Management</option>
                    <option value="ELECTRICITY" {% if category_filter == 'ELECTRICITY' %}selected{% endif %}>Electricity</option>
                    <option value="WATER" {% if category_filter == 'WATER' %}selected{% endif %}>Water Supply</option>
                    <option value="SAFETY" {% if category_filter == 'SAFETY' %}selected{% endif %}>Public Safety</option>
                    <option value="OTHER" {% if category_filter == 'OTHER' %}selected{% endif %}>Other</option>
                </select>
            </div>
            
            <a href="{% url 'concerns:map' %}" class="btn btn-outline">Clear Filters</a>
        </form>
    </div>
    
    <!-- Map Legend -->
    <div class="map-legend">
        <div class="legend-item">
            <span class="legend-marker" style="background: orange;"></span>
            <span>Pending</span>
        </div>
        <div class="legend-item">
            <span class="legend-marker" style="background: blue;"></span>
            <span>In Progress</span>
        </div>
        <div class="legend-item">
            <span class="legend-marker" style="background: green;"></span>
            <span>Resolved</span>
        </div>
        <div class="legend-item">
            <span class="legend-marker" style="background: gray;"></span>
            <span>Closed</span>
        </div>
    </div>
    
    <!-- Map Container -->
    <div id="concern-map" class="concern-map"></div>
</div>

<!-- Leaflet CSS -->
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />

<!-- Leaflet JS -->
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const map = L.map('concern-map').setView([14.5995, 120.9842], 13);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19
    }).addTo(map);
    
    fetch('{% url "concerns:map_data" %}?' + window.location.search.substring(1))
        .then(response => response.json())
        .then(data => {
            if (data.concerns.length === 0) {
                alert('No concerns with location data found.');
                return;
            }
            
            const bounds = [];
            
            data.concerns.forEach(concern => {
                const lat = concern.latitude;
                const lng = concern.longitude;
                bounds.push([lat, lng]);
                
                const iconHtml = `
                    <div class="custom-marker" style="background-color: ${concern.marker_color};">
                        <span style="font-size: 20px;">${concern.category_icon}</span>
                    </div>
                `;
                
                const customIcon = L.divIcon({
                    html: iconHtml,
                    className: 'custom-marker-wrapper',
                    iconSize: [40, 40],
                    iconAnchor: [20, 40],
                    popupAnchor: [0, -40]
                });
                
                const marker = L.marker([lat, lng], { icon: customIcon }).addTo(map);
                
                const popupContent = `
                    <div class="map-popup">
                        <h3>${concern.title}</h3>
                        <p><strong>Category:</strong> ${concern.category_display}</p>
                        <p><strong>Status:</strong> <span class="badge badge-status-${concern.status.toLowerCase()}">${concern.status_display}</span></p>
                        <p><strong>Location:</strong> ${concern.location}</p>
                        <p><strong>Barangay:</strong> ${concern.barangay}</p>
                        <p>${concern.description}</p>
                        <a href="/concerns/${concern.id}/" class="btn btn-sm btn-primary">View Details</a>
                    </div>
                `;
                
                marker.bindPopup(popupContent);
            });
            
            if (bounds.length > 0) {
                map.fitBounds(bounds, { padding: [50, 50] });
            }
        })
        .catch(error => {
            console.error('Error loading map data:', error);
            alert('Error loading concern locations.');
        });
});
</script>
{% endblock %}'''
}

# Create the files if they don't exist
for filename, content in templates.items():
    filepath = os.path.join(BASE_DIR, filename)
    if not os.path.exists(filepath):
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Created {filepath}")
    else:
        print(f"File already exists: {filepath}")

print("Template check complete.")
