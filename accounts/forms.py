from django import forms

class SubscriptionForm(forms.Form):
    email = forms.EmailField(
        label='Email Address',
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email Address',
            'class': 'form-control'
        })
    )   