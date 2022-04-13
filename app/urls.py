from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('auth/', views.auth, name='auth'),
    path('register/', views.register, name='register'),
    path('authorized/', views.authorized_user, name='authorized'),
    path('authorized/ask/', views.ask_question, name='ask'),
    path('authorized/settings/', views.user_settings, name='settings')
]
