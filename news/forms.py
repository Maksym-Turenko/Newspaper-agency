from django.contrib.auth.forms import UserCreationForm
from news.models import Redactor

class RedactorCreationForm(UserCreationForm):
    class Meta:
        model = Redactor
        fields = ['username', 'years_of_experience', 'password1', 'password2']
