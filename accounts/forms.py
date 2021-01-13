from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# fornisce form per registrazione al sito a disposizione dell'utente

class registrationForm(UserCreationForm):

    class Meta:

        model = User
        fields = ['username','email','password1','password2']