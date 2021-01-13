from django.db import models
from django.contrib.auth.models import User
from api.utils import sendTransaction
import hashlib

# Create your models here.

# fornisce modello per la pubblicazione di post inclusa una funzione per memorizzarla su blockchain

class Post(models.Model):
    author  = models.ForeignKey(User, on_delete=models.CASCADE)
    title   = models.CharField(max_length=50)
    text    = models.TextField()
    date    = models.DateTimeField(auto_now_add=True,auto_now=False)
    hash    = models.CharField(max_length=32, default=None, null=True)
    txId    = models.CharField(max_length=66, default=None, null=True)

    def writeOnChain(self):

        self.hash = hashlib.sha256(self.text.encode('utf-8')).hexdigest()
        self.txId = sendTransaction(self.hash)
        self.save()

    def __str__(self):

        return self.title

# fornisce modello per l'inserimento di un testo

class Search(models.Model):

    string = models.TextField()

    def __str__(self):

        return self.string