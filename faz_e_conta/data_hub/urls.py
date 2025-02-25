from django.urls import path
from . import views
from .url_tools import *

urlpatterns = [
    path('', views.show_students, name='show_students'),
    path('<int:aluno_id>/', views.show_student, name='show_student'),
]

urlpatterns = add_urlpatterns(urlpatterns)