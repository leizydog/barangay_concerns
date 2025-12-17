import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.template.loader import render_to_string
from django.test import RequestFactory
from apps.security_management.forms import UserLoginForm

print("=" * 60)
print("TESTING TEMPLATE RENDERING")
print("=" * 60)

# Create a fake request
factory = RequestFactory()
request = factory.get('/accounts/login/')

# Create form
form = UserLoginForm()

# Try to render the login template
print("\n1. Testing login.html rendering...")
try:
    context = {'form': form}
    rendered = render_to_string('security_management/pages/login.html', context)
    
    # Check if it's actually rendered or just raw code
    if '{% include' in rendered or '{% extends' in rendered:
        print("✗ TEMPLATE NOT RENDERED - Contains raw Django tags!")
        print("\nFirst 500 characters of output:")
        print(rendered[:500])
    else:
        print("✓ Template rendered successfully!")
        print(f"\nRendered output length: {len(rendered)} characters")
        print("\nFirst 200 characters:")
        print(rendered[:200])
        
except Exception as e:
    print(f"✗ Error rendering template: {e}")
    import traceback
    traceback.print_exc()

# Test if base.html exists and works
print("\n2. Testing base.html...")
try:
    rendered_base = render_to_string('base.html', {})
    if '{% block' in rendered_base:
        print("✗ base.html contains unrendered tags")
    else:
        print("✓ base.html renders correctly")
except Exception as e:
    print(f"✗ Error with base.html: {e}")

# Test organism directly
print("\n3. Testing auth_card.html directly...")
try:
    context = {
        'header_title': 'Test Title',
        'header_text': 'Test text',
        'form': form,
        'submit_text': 'Submit',
        'footer_text': 'Footer text',
        'footer_link_text': 'Link text',
        'footer_link_url': 'security_management:login'
    }
    rendered_card = render_to_string('security_management/organisms/auth_card.html', context)
    
    if '{% include' in rendered_card:
        print("✗ auth_card.html contains unrendered includes!")
        print("\nShowing raw content:")
        print(rendered_card[:500])
    else:
        print("✓ auth_card.html renders correctly")
        
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)