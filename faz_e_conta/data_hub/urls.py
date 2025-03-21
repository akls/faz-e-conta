from django.urls import path
from . import views
from .auto_gen_form_url import *
from .auto_gen_show_id_url import *

urlpatterns = [
    path('', views.index, name='index'),
    path('alunos/', views.show_students, name='show_students'),
    path('responsaveis_educativos/', views.show_responsaveis_educativos, name='show_responsaveis_educativos'),
]

urlpatterns = add_form_urlpatterns(urlpatterns)
urlpatterns = add_show_id_urlpatterns(urlpatterns)