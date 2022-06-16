from os import stat
from django.conf import settings
from django.urls import path
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static
from django.conf import settings

from app.models import Answer
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hottest/', views.hot_questions, name='hot'),
    path('newest/', views.new_questions, name='new'),
    path('auth/', views.auth, name='auth'),
    path('logout', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    path('register/', views.register, name='register'),
    path('ask/', views.ask_question, name='ask'),
    path('authorized/settings/', views.user_settings, name='settings'),
    path('view-question/<int:post_id>/', views.view_question, name='view-question'),
    # path('view-question/<int:post_id>', views.view_question, name='view-question'),
    path('<int:tag_id>', views.tag_question, name='tag')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
