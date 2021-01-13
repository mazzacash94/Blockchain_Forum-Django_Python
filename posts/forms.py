from django import forms
from .models import Post, Search

# fornisce form per pubblicazione di post a disposizione dell'utente

class post_form(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)

# fornisce form per inserimento di un testo a disposizione dell'utente

class search_form(forms.ModelForm):

    class Meta:
        model = Search
        fields = ('string',)