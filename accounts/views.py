from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from django.contrib import messages
from django.http import HttpResponseServerError, JsonResponse
from django.contrib.auth.models import User
from .forms import registrationForm
from .models import Logging
from posts.models import Post
import logging

# Create your views here.

# crea un istanza del logger

logger = logging.getLogger(__name__)

# dizionario di configurazione del sistema di logging

logging.config.dictConfig({

    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '[%(asctime)s] %(levelname)s %(message)s', 'datefmt' : "%Y/%m/%d %H:%M:%S",
        },
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': '/tmp/debug.log'
        }
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        }
    }
})

# visualizza homepage del sito

def homepage(request):

    return render(request, 'index.html')

# consente accesso ad utente e modifica ip con cui si è accessi nel caso in cui sia diverso dal precedente riportandone le informazioni nella console tramite sistema di logging

def logIn(request):

    if request.method == 'POST':

       username = request.POST.get('username')
       password = request.POST.get('password')
       user = authenticate(request, username=username, password=password)

       if user is not None:

           currentUser = Logging.objects.get(username=user)

           if currentUser.ip == getIp(request):

                logger.info("".join([getIp(request), " : ", user.username, " logged in with the same ip of the last session!"]))
                login(request, user)
                return redirect("../")

           else:

                logger.warning("".join([getIp(request), " : ", user.username, " logged in with a different ip than last session!"]))
                currentUser.ip = getIp(request)
                currentUser.save()
                login(request, user)
                return redirect("../")

       else:

                messages.error(request, "Username o Password Errati... Riprova!")

    return render(request, 'login.html')

# consente a visitatore di registrarsi al sito memorizzandone l'ip e riportandone l'esito nella console tramite sistema di logging

def registration(request):

    if request.method == 'POST':

        form = registrationForm(request.POST)

        if form.is_valid():

            form.save()
            users=User.objects.order_by("-date_joined")
            last_user=users[0]
            Logging.objects.create(username=last_user, ip=getIp(request))
            logger.info("".join([getIp(request), " : ", request.POST.get("username"), " registrated succesfully!"]))
            return redirect('../')

        else:

            messages.error(request, 'Account Utente non Creato... Riprova!')

    else:

        form = registrationForm()

    return render(request, "registration.html", {'form':form})

# consente ad utente di effettuare il logout dal sito

def logout(request):

    user=request.user
    django_logout(request)
    logger.info("".join([getIp(request), " : ", user.username, " logged out"]))

    return redirect("../")

# consente ad utente di visualizzare le informazioni di profilo

def profile(request):

    user=request.user
    posts=len(Post.objects.filter(author=user))

    return render(request, "profile.html", {'user':user, "posts":posts})

# fornisce l'ip dell'utente collegato al sito

def getIp(request):

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:

        ip = x_forwarded_for.split(',')[-0]

    else:

        ip = request.META.get('REMOTE_ADDR')

    return ip

# fornisce risposta in Json riportante i dati dell'utente a cui è associato l'id e risposta in Http nel caso l'id non è associato a nessun utente registrato al sito

def userId(request,id):

    users = User.objects.all()

    for user in users:

        chosenUser=User.objects.get(username=user)
        chosenId=chosenUser.id

        if id == chosenId:

            profile = {

                'Id' : chosenId,
                'Username' : chosenUser.username,
                'Registration Date' : chosenUser.date_joined,

            }

            return JsonResponse(profile)

    return HttpResponseServerError("The specified ID doesn't belong to any user!")




