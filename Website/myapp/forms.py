# myapp/forms.py

from django import forms
from .models import UserProfile  # Import the UserProfile model

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'email', 'encrypted_credit_card']
        widgets = {
            'encrypted_credit_card': forms.HiddenInput(),
        }

