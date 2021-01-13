from django.urls import path
from . import views

urlpatterns = [

    path ('login'                  ,  views.logIn          , name='login'         ),
    path ('registration'     ,  views.registration   , name='registration'  ),
    path ('logout'           ,  views.logout         , name='logout'        ),
    path ('profile'          ,  views.profile        , name="profile"       ),
    path ('user/<int:id>/'  ,  views.userId         , name='id_utente'     ),

]