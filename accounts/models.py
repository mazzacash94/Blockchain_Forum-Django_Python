from django.db import models

# Create your models here.

# fornisce modello riportante le informazioni riguardanti nome utente ed ip

class Logging(models.Model):

    username  =   models.CharField(max_length=20)
    ip        =   models.CharField(max_length=20)

    def __str__(self):

        return self.username