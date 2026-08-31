from django import forms
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
User = get_user_model()


# ########################################################
# Profile Update Form
# ########################################################
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "picture",
        ]

        widgets = {
            "first_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "First Name",
            }),
            "last_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Last Name",
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Email Address",
            }),
            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Phone Number",
            }),
            "picture": forms.ClearableFileInput(attrs={
                "class": "form-control",
            }),
        }
        

    # Optional: Email validation
    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This email is already in use.")

        return email
    
    
    
class UserAdminForm(forms.ModelForm):
    """
    Custom form for User model in admin:
    - password1 and password2 optional on edit
    - hash passwords automatically if new
    - styled with CSS
    """
    password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "vTextField",
                "style": "width:300px; border:1px solid #ccc; padding:5px; border-radius:4px;"
            }
        ),
        required=False,
        help_text="Leave blank if you don't want to change the password."
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "vTextField",
                "style": "width:300px; border:1px solid #ccc; padding:5px; border-radius:4px;"
            }
        ),
        required=False
    )

    class Meta:
        model = User
        fields = '__all__'

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 or password2:
            if password1 != password2:
                raise ValidationError("Passwords do not match.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password1")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user
    
    


# ########################################################
# CustomPasswordResetForm
# ########################################################

class CustomPasswordResetForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your registered email",
            "id": "email-input"
        })
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email not registered.")
        return email