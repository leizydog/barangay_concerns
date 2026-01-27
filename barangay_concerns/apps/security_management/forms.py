# apps/security_management/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 
                  'phone_number', 'barangay', 'municipality', 
                  'password1', 'password2']
        # Removed 'role' from fields - users can only register as USER
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-input'
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'USER'  # Force all registrations to be regular users
        if commit:
            user.save()
        return user

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-input'
        self.fields['password'].widget.attrs['class'] = 'form-input'

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile_image', 'alias', 'first_name', 'last_name', 'phone_number', 
                  'region', 'province', 'city', 'municipality', 'barangay']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-input'
        
        # Add help text for alias
        self.fields['alias'].help_text = "This name will be shown publicly. If left blank, a random one will be generated."