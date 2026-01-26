# apps/concerns/forms.py
from django import forms
from .models import Concern, Comment

class ConcernForm(forms.ModelForm):
    class Meta:
        model = Concern
        fields = ['title', 'description', 'category', 'location', 
                  'barangay', 'municipality', 'latitude', 'longitude', 'image', 'is_anonymous', 'alias']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['image', 'latitude', 'longitude', 'is_anonymous']:
                field.widget.attrs['class'] = 'form-input'
        
        # Make location read-only since it will be auto-filled from map
        self.fields['location'].widget.attrs['readonly'] = 'readonly'
        self.fields['location'].required = False

class ConcernUpdateForm(forms.ModelForm):
    class Meta:
        model = Concern
        fields = ['title', 'description', 'category', 'location', 
                  'barangay', 'municipality', 'latitude', 'longitude', 
                  'status', 'priority', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Only LGU can change status and priority
        if user and not user.is_lgu():
            del self.fields['status']
            del self.fields['priority']
        
        for field_name, field in self.fields.items():
            if field_name not in ['image', 'latitude', 'longitude']:
                field.widget.attrs['class'] = 'form-input'
        
        # Make location read-only
        self.fields['location'].widget.attrs['readonly'] = 'readonly'
        self.fields['location'].required = False


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3, 
                'class': 'form-input', 
                'placeholder': 'Add a comment or update...'
            }),
        }
