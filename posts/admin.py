from django.contrib import admin
from .models import Post

# Register your models here.

# fornisce un modello nell'interfaccia admin con cui si possono filtrare i post in base all'autore così da visualizzarne quanti ne sono stati pubblicati da ognuno

class PostAdmin(admin.ModelAdmin):

    list_display  = ["title","date"]
    search_fields = ["title","text"]
    list_filter   = ["author"]

admin.site.register(Post,PostAdmin)

