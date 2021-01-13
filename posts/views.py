from django.shortcuts import render, redirect
from .forms import post_form, search_form
from .models import Post
from django.utils import timezone
from django.contrib import messages
from django.http import JsonResponse
from datetime import timedelta, datetime
from django.contrib.auth.decorators import login_required


# Create your views here.

# permette visualizzazione dei post in ordine decrescente di pubblicazione solo se hai effettuato il login

def home(request):
    return render(request, "index.html")

@login_required()
def forum(request):
    posts = Post.objects.order_by('-date')

    return render(request, 'forum.html', {'posts' : posts})

# permette pubblicazione di un post e lo memorizza automaticamente sulla blockchain solo se hai effettuato il login

@login_required()
def newPost(request):
    form = post_form(request.POST)

    if request.method == "POST":

        if form.is_valid():

            text_verify = request.POST.get("text")

            if "hack" in text_verify:

                messages.error(request, "You can't use the word hack!")

            else:

                post = form.save(commit=False)
                post.author = request.user
                post.date = timezone.now()
                post.save()
                lastPost = Post.objects.order_by("-date")
                postChain = lastPost[0]
                postChain.writeOnChain()
                return redirect('forum')

        else:

            form = post_form()

    return render(request, 'addPost.html', {'form': form})


# prende in input tramite una richiesta GET la stringa inserita, verifica se è presente all'interno dei post e riporta il numero di volte in cui essa è contenuta

def stringSearch(request):
    if request.method == "GET":

        form = search_form(request.GET)
        word = request.GET.get("string")
        posts = Post.objects.all()

        contatore = 0

        if form.is_valid():

            for post in posts:

                if word in post.text.lower():
                    contatore += 1

            if contatore > 1:

                messages.info(request, f"The string appears {contatore} times among the published posts!")

            elif contatore == 1:

                messages.info(request, f"The string appears {contatore} time among the published posts!")

            else:

                messages.info(request, f"The string doesn't appear among the published posts!")

    return render(request, 'search.html', {'form': form, 'contatore': contatore})


# fornisce una risposta in Json contenente le informazioni dei post pubblicati nell'ultima ora

def lastHour(request):
    info = []
    last_hour = datetime.now() - timedelta(hours=1)
    posts = Post.objects.filter(date__gte=last_hour).order_by('-date')

    for post in posts:
        author_string = str(post.author)
        info.append(
            {
                'Autore': author_string,
                'Titolo': post.title,
                'Contenuto': post.text,
                'Data di Pubblicazione': post.date,
                'Hash': post.hash,
                'TxId': post.txId,
            }
        )

    return JsonResponse(info, safe=False)


