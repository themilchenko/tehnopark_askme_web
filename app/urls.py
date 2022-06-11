from django.urls import path

from app.models import Answer
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hottest/', views.hot_questions, name='hot'),
    path('newest/', views.new_questions, name='new'),
    path('auth/', views.auth, name='auth'),
    path('register/', views.register, name='register'),
    path('authorized/', views.authorized_user, name='authorized'),
    path('authorized/ask/', views.ask_question, name='ask'),
    path('authorized/settings/', views.user_settings, name='settings'),
    path('view-question/<int:post_id>/', views.view_question, name='view-question'),
    path('<int:tag_id>', views.tag_question, name='tag')
]
