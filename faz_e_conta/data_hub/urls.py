from django.urls import path
from . import views
from .form_url import *
from .show_id_url import *

urlpatterns = [
    path('', views.show_students, name='index'),
    path('view_students/', views.show_students, name='show_students'),
    path('student/<int:aluno_id>/', views.show_student, name='show_student'),
]

urlpatterns = add_form_urlpatterns(urlpatterns)
urlpatterns = add_show_id_urlpatterns(urlpatterns)