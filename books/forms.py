from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()  # ✅ Dynamically get the custom User model

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={"placeholder": "Enter your email", "class": "form-control"})
    )

    class Meta:
        model = User  # ✅ Use the custom User model
        fields = ["username", "email", "password1", "password2"]

    def clean_email(self):
        """Ensure email is unique"""
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email


class CheckoutForm(forms.Form):
    full_name = forms.CharField(
        max_length=100, 
        label="Full Name", 
        widget=forms.TextInput(attrs={"placeholder": "John Doe", "class": "form-control"})
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "123 Main Street", "class": "form-control", "rows": 3})
    )
    city = forms.CharField(
        max_length=50, 
        label="City", 
        widget=forms.TextInput(attrs={"placeholder": "New York", "class": "form-control"})
    )
    zip_code = forms.CharField(
        max_length=10, 
        label="ZIP Code", 
        widget=forms.TextInput(attrs={"placeholder": "10001", "class": "form-control", "pattern": "[0-9]+"})
    )
    country = forms.CharField(
        max_length=50, 
        label="Country", 
        widget=forms.TextInput(attrs={"placeholder": "USA", "class": "form-control"})
    )
