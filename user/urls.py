from django.urls import path
from .views import Join, Login, Logout, Idcheck

urlpatterns = [
    path('join', Join.as_view()),
    path('login', Login.as_view()),
    path('logout', Logout.as_view()),
    path('idcheck', Idcheck.as_view()),
]
