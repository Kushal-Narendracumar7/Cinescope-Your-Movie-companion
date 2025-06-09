from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from accounts.models import CustomUser


User = get_user_model()  # Use the custom user model
class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser  # ✅ Use CustomUser instead of User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_mobile_no(self):
        mobile_no = self.cleaned_data.get('mobile_no')
        if CustomUser.objects.filter(mobile_no=mobile_no).exists():
            raise forms.ValidationError("This mobile number is already in use.")
        return mobile_no

class EditProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    class Meta:
        model = CustomUser
        fields = ["username", "email", "first_name", "last_name", "mobile_no", "gender", "nationality",'date_of_birth','favorite_genre','profile_picture']